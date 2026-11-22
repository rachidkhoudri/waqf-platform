"""
محرك الحسابات المالية للصيغ الاستثمارية الإسلامية السبع
وفقاً لأحكام القانون الجزائري للأوقاف 25-06 (الفصل العاشر) والمعايير الشرعية (AAOIFI)
بدون ضمان رأس المال، مع قواعد توزيع الأرباح وتطبيق أجرة الناظر (10%) وصندوق الاحتياطي.
"""
from typing import Dict, Any
from app.config import settings

class IslamicFormulaEngine:
    @staticmethod
    def calculate_settlement(
        formula: str,
        total_project_capital: float,
        waqf_capital: float,
        individual_funder_capital: float,
        owner_capital: float,
        gross_revenue: float,
        direct_expenses: float,
        agreed_profit_sharing_ratio: float, # مثلاً 0.60 لحملة رأس المال و 0.40 لرب العمل
        has_misconduct: bool = False,
        nazir_fee_rate: float = None,
        reserve_fund_rate: float = None
    ) -> Dict[str, Any]:
        """
        حساب التسوية المالية وتوزيع العوائد أو الخسائر بحسب الصيغة التعاقدية
        """
        if nazir_fee_rate is None:
            nazir_fee_rate = settings.DEFAULT_NAZIR_FEE_PERCENTAGE / 100.0
        if reserve_fund_rate is None:
            reserve_fund_rate = settings.DEFAULT_RESERVE_FUND_PERCENTAGE / 100.0

        net_operating = gross_revenue - direct_expenses
        total_funders_capital = waqf_capital + individual_funder_capital
        total_capital = total_funders_capital + owner_capital

        result = {
            "formula": formula,
            "gross_revenue": gross_revenue,
            "direct_expenses": direct_expenses,
            "net_operating": net_operating,
            "is_loss": net_operating < 0,
            "owner_share": 0.0,
            "total_funders_share": 0.0,
            "individual_funders_share": 0.0,
            "waqf_gross_share": 0.0,
            "reserve_fund_deduction": 0.0,
            "nazir_fee_deduction": 0.0,
            "waqf_net_for_beneficiaries": 0.0,
            "loss_borne_by_waqf": 0.0,
            "loss_borne_by_funders": 0.0,
            "loss_borne_by_owner": 0.0,
            "summary_ar": ""
        }

        # -------------------------------------------------------------
        # 1. صيغة المشاركة (Musharaka - المادة 78 من القانون 25-06)
        # -------------------------------------------------------------
        if formula == "musharaka":
            if net_operating >= 0:
                # الربح يوزع حسب النسبة المتفق عليها في العقد
                funders_profit = round(net_operating * agreed_profit_sharing_ratio, 2)
                owner_profit = round(net_operating * (1.0 - agreed_profit_sharing_ratio), 2)
                
                result["owner_share"] = owner_profit
                result["total_funders_share"] = funders_profit
                
                # توزيع حصة الممولين بنسبة رأس مال كل منهم
                if total_funders_capital > 0:
                    waqf_ratio = waqf_capital / total_funders_capital
                    result["waqf_gross_share"] = round(funders_profit * waqf_ratio, 2)
                    result["individual_funders_share"] = round(funders_profit * (1.0 - waqf_ratio), 2)
            else:
                # الخسارة في المشاركة تكون بحسب حصة كل طرف في رأس المال حصراً
                loss = abs(net_operating)
                waqf_loss_ratio = waqf_capital / total_capital if total_capital > 0 else 0
                funder_loss_ratio = individual_funder_capital / total_capital if total_capital > 0 else 0
                owner_loss_ratio = owner_capital / total_capital if total_capital > 0 else 0
                
                result["loss_borne_by_waqf"] = loss * waqf_loss_ratio
                result["loss_borne_by_funders"] = loss * funder_loss_ratio
                result["loss_borne_by_owner"] = loss * owner_loss_ratio
                result["summary_ar"] = "تحمل كل شريك نصيبه من الخسارة بحسب حصته في رأس المال عملاً بأحكام المادة 78."

        # -------------------------------------------------------------
        # 2. صيغة المضاربة / القراض (Mudaraba - المادة 81 من القانون 25-06)
        # -------------------------------------------------------------
        elif formula == "mudaraba":
            if net_operating >= 0:
                # الربح يوزع بالنسبة المتفق عليها (مال مقابل عمل)
                funders_profit = net_operating * agreed_profit_sharing_ratio
                owner_profit = net_operating * (1.0 - agreed_profit_sharing_ratio)
                
                result["owner_share"] = owner_profit
                result["total_funders_share"] = funders_profit
                
                if total_funders_capital > 0:
                    waqf_ratio = waqf_capital / total_funders_capital
                    result["waqf_gross_share"] = funders_profit * waqf_ratio
                    result["individual_funders_share"] = funders_profit * (1.0 - waqf_ratio)
            else:
                loss = abs(net_operating)
                if has_misconduct:
                    # عند ثبوت التعدي أو التقسيط يتحمل المضارب (صاحب المشروع) كامل الخسارة
                    result["loss_borne_by_owner"] = loss
                    result["summary_ar"] = "ثبت تعدٍّ أو تفريط من المضارب؛ فيضمن الخسارة بالكامل لصالح أرباب المال."
                else:
                    # بدون تعدٍّ: يتحمل رب المال الخسارة المالية ويخسر المضارب جهده وعمله
                    if total_funders_capital > 0:
                        waqf_ratio = waqf_capital / total_funders_capital
                        result["loss_borne_by_waqf"] = loss * waqf_ratio
                        result["loss_borne_by_funders"] = loss * (1.0 - waqf_ratio)
                    result["summary_ar"] = "تحمل أرباب المال الخسارة المالية وخسر المضارب جهده بدون ضمان لرأس المال (المادة 81)."

        # -------------------------------------------------------------
        # 3. صيغة المرابحة (Murabaha - المادة 82 من القانون 25-06)
        # -------------------------------------------------------------
        elif formula == "murabaha":
            # في المرابحة، العائد هو هامش الربح المتفق عليه في العقد
            profit_margin = net_operating  # الفرق بين التكلفة وثمن البيع الآجل
            if profit_margin > 0:
                result["total_funders_share"] = profit_margin
                result["owner_share"] = 0.0  # المشتري اشترى السلعة واستلمها
                if total_funders_capital > 0:
                    waqf_ratio = waqf_capital / total_funders_capital
                    result["waqf_gross_share"] = profit_margin * waqf_ratio
                    result["individual_funders_share"] = profit_margin * (1.0 - waqf_ratio)
            else:
                result["loss_borne_by_waqf"] = abs(net_operating) * (waqf_capital / total_funders_capital if total_funders_capital > 0 else 1)

        # -------------------------------------------------------------
        # 4. صيغة السَّلَم (Salam - المادة 83 من القانون 25-06)
        # -------------------------------------------------------------
        elif formula == "salam":
            # بيع السلعة المسلمة وفارق القيمة السوقية
            if net_operating >= 0:
                result["total_funders_share"] = net_operating
                if total_funders_capital > 0:
                    waqf_ratio = waqf_capital / total_funders_capital
                    result["waqf_gross_share"] = net_operating * waqf_ratio
                    result["individual_funders_share"] = net_operating * (1.0 - waqf_ratio)
            else:
                loss = abs(net_operating)
                waqf_ratio = waqf_capital / total_funders_capital if total_funders_capital > 0 else 1
                result["loss_borne_by_waqf"] = loss * waqf_ratio
                result["loss_borne_by_funders"] = loss * (1.0 - waqf_ratio)

        # -------------------------------------------------------------
        # 5. صيغة الاستصناع والمقاولة (Istisna'a - المادة 75 من القانون 25-06)
        # -------------------------------------------------------------
        elif formula == "istisna":
            if net_operating >= 0:
                # الفارق التعاقدي بين تكلفة الاستصناع وسعر البيع
                result["total_funders_share"] = net_operating * agreed_profit_sharing_ratio
                result["owner_share"] = net_operating * (1.0 - agreed_profit_sharing_ratio)
                if total_funders_capital > 0:
                    waqf_ratio = waqf_capital / total_funders_capital
                    result["waqf_gross_share"] = result["total_funders_share"] * waqf_ratio
                    result["individual_funders_share"] = result["total_funders_share"] * (1.0 - waqf_ratio)
            else:
                loss = abs(net_operating)
                result["loss_borne_by_waqf"] = loss * (waqf_capital / total_funders_capital if total_funders_capital > 0 else 1)

        # -------------------------------------------------------------
        # 6. صيغة الإجارة (Ijarah - المادة 70 من القانون 25-06)
        # -------------------------------------------------------------
        elif formula == "ijarah":
            # بدل الإيجار الدوري المنتظم بعد خصم تكاليف الصيانة الأساسية
            if net_operating >= 0:
                result["total_funders_share"] = net_operating
                if total_funders_capital > 0:
                    waqf_ratio = waqf_capital / total_funders_capital
                    result["waqf_gross_share"] = net_operating * waqf_ratio
                    result["individual_funders_share"] = net_operating * (1.0 - waqf_ratio)
            else:
                # في حالة هلاك العين المؤجرة دون تعدٍّ يتحمل المالك الخسارة
                result["loss_borne_by_waqf"] = abs(net_operating)

        # -------------------------------------------------------------
        # 7. صيغة المزارعة والمساقاة (Muzara'a - المادتان 71 و 72 من القانون 25-06)
        # -------------------------------------------------------------
        elif formula == "muzaraa":
            if net_operating >= 0:
                # حصة شائعة من ناتج المحصول
                result["total_funders_share"] = net_operating * agreed_profit_sharing_ratio
                result["owner_share"] = net_operating * (1.0 - agreed_profit_sharing_ratio)
                if total_funders_capital > 0:
                    waqf_ratio = waqf_capital / total_funders_capital
                    result["waqf_gross_share"] = result["total_funders_share"] * waqf_ratio
                    result["individual_funders_share"] = result["total_funders_share"] * (1.0 - waqf_ratio)
            else:
                loss = abs(net_operating)
                # الجوائح والآفات الطبيعية يتحملها كل طرف في ما قدمه (الممول فقد الغلة والعامل جهده)
                result["loss_borne_by_waqf"] = loss * (waqf_capital / total_funders_capital if total_funders_capital > 0 else 1)

        # -------------------------------------------------------------
        # توزيع حصة المحفظة الوقفية بعد الاستقطاعات القانونية:
        # 1. صندوق الاحتياطي الوقفي (لمواجهة المخاطر)
        # 2. أجرة الناظر (10% المحددة لصالح المنصة كناظر)
        # 3. الصافي المتبقي يوزع على الجهات المستفيدة فقط
        # -------------------------------------------------------------
        if result["waqf_gross_share"] > 0:
            reserve = result["waqf_gross_share"] * reserve_fund_rate
            nazir_fee = (result["waqf_gross_share"] - reserve) * nazir_fee_rate
            net_for_beneficiaries = result["waqf_gross_share"] - reserve - nazir_fee

            result["reserve_fund_deduction"] = round(reserve, 2)
            result["nazir_fee_deduction"] = round(nazir_fee, 2)
            result["waqf_net_for_beneficiaries"] = round(net_for_beneficiaries, 2)
            result["summary_ar"] = (
                f"تم احتساب العوائد بصيغة {formula}: "
                f"إجمالي أرباح الوقف {result['waqf_gross_share']:,.2f} د.ج، "
                f"استقطاع صندوق الاحتياطي ({reserve_fund_rate*100}%) = {reserve:,.2f} د.ج، "
                f"أجرة الناظر ({nazir_fee_rate*100}%) = {nazir_fee:,.2f} د.ج، "
                f"الصافي المخصص للجهات المستفيدة = {net_for_beneficiaries:,.2f} د.ج."
            )
        
        return result
