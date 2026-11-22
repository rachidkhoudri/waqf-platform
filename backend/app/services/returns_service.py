"""
خدمات تسوية المشاريع وتوزيع العوائد وحصص المستفيدين وأجرة الناظر (المرحلة 12 و 13)
"""
from datetime import datetime
import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.config import settings
from app.models.project import Project
from app.models.funding import ProjectFunding
from app.models.returns import ProjectSettlement, BeneficiaryDisbursement
from app.models.waqf import WaqfFund, WaqfCondition
from app.models.audit import ReserveFundLedger
from app.models.notification import Notification
from app.services.islamic_formulas import IslamicFormulaEngine

class ReturnsService:
    @staticmethod
    def execute_project_settlement(
        db: Session,
        project_id: int,
        gross_revenue: float,
        direct_expenses: float,
        auditor_name: str,
        has_misconduct: bool = False,
        audit_notes: str = ""
    ) -> ProjectSettlement:
        """
        تنفيذ تسوية العوائد المالية للمشروع وتوزيع الأرباح على الممولين والمحفظة الوقفية والجهات المستفيدة
        مع استقطاع صندوق الاحتياطي وأجرة الناظر (10%).
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("المشروع غير موجود")
        if project.is_returns_distributed:
            raise ValueError("تمت تسوية هذا المشروع وتوزيع عوائده مسبقاً")

        # جمع مبالغ التمويل من سجلات التمويل
        fundings = db.query(ProjectFunding).filter(ProjectFunding.project_id == project.id).all()
        waqf_capital = sum([f.amount for f in fundings if f.funding_source == "WAQF"])
        individual_capital = sum([f.amount for f in fundings if f.funding_source == "INDIVIDUAL"])
        total_funded = waqf_capital + individual_capital
        
        # في المشاركة: حصة صاحب المشروع
        owner_capital = max(0.0, project.requested_amount - total_funded) if project.islamic_formula == "musharaka" else 0.0

        # احتساب التوزيع وفق محرك الصيغ الإسلامية السبع
        calc = IslamicFormulaEngine.calculate_settlement(
            formula=project.islamic_formula,
            total_project_capital=project.requested_amount,
            waqf_capital=waqf_capital,
            individual_funder_capital=individual_capital,
            owner_capital=owner_capital,
            gross_revenue=gross_revenue,
            direct_expenses=direct_expenses,
            agreed_profit_sharing_ratio=project.expected_return_rate / 100.0,
            has_misconduct=has_misconduct,
            nazir_fee_rate=settings.DEFAULT_NAZIR_FEE_PERCENTAGE / 100.0,
            reserve_fund_rate=settings.DEFAULT_RESERVE_FUND_PERCENTAGE / 100.0
        )

        # إنشاء سجل التسوية
        settlement = ProjectSettlement(
            project_id=project.id,
            settlement_date=datetime.utcnow(),
            gross_revenue=gross_revenue,
            direct_expenses=direct_expenses,
            net_operating_result=calc["net_operating"],
            is_loss=calc["is_loss"],
            loss_explanation=calc["summary_ar"] if calc["is_loss"] else None,
            has_owner_misconduct=has_misconduct,
            project_owner_share=calc["owner_share"],
            total_funders_profit=calc["total_funders_share"],
            individual_funders_share=calc["individual_funders_share"],
            waqf_gross_profit=calc["waqf_gross_share"],
            reserve_fund_deduction=calc["reserve_fund_deduction"],
            nazir_fee_deduction=calc["nazir_fee_deduction"],
            waqf_net_for_beneficiaries=calc["waqf_net_for_beneficiaries"],
            status="DISTRIBUTED",
            audited_by=auditor_name,
            audit_notes=audit_notes or calc["summary_ar"]
        )
        db.add(settlement)
        db.flush()

        # قيد في صندوق الاحتياطي الوقفي (إذا كانت هناك أرباح)
        if calc["reserve_fund_deduction"] > 0:
            db.add(ReserveFundLedger(
                project_id=project.id,
                transaction_type="INFLOW",
                amount=calc["reserve_fund_deduction"],
                balance_after=calc["reserve_fund_deduction"], # تراكمي
                notes=f"تغذية صندوق الاحتياطي بنسبة {settings.DEFAULT_RESERVE_FUND_PERCENTAGE}% من أرباح مشروع {project.title}"
            ))

        # تحديث محافظ الأوقاف المشاركة وتوزيع الريع على مستحقيها وفق شرط كل واقف
        for f in fundings:
            if f.funding_source == "WAQF" and f.waqf_fund_id:
                waqf_fund = db.query(WaqfFund).filter(WaqfFund.id == f.waqf_fund_id).first()
                if waqf_fund:
                    # إعادة أصل الوقف إلى السيولة المتاحة في وقفه المستقل (لا يصرف)
                    returned_corpus = f.amount
                    if calc["is_loss"] and not has_misconduct:
                        # في حالة الخسارة يتحمل نصيبه
                        loss_share = calc["loss_borne_by_waqf"] * (f.amount / waqf_capital if waqf_capital > 0 else 1)
                        returned_corpus = max(0.0, f.amount - loss_share)
                    
                    waqf_fund.current_invested_amount = max(0.0, waqf_fund.current_invested_amount - f.amount)
                    waqf_fund.uninvested_cash += returned_corpus

                    # حساب حصة هذا الوقف من صافي الربح المخصص للمستفيدين
                    if waqf_capital > 0 and calc["waqf_net_for_beneficiaries"] > 0:
                        fund_share_of_net = calc["waqf_net_for_beneficiaries"] * (f.amount / waqf_capital)
                        waqf_fund.total_returns_earned += fund_share_of_net
                        waqf_fund.total_returns_distributed += fund_share_of_net

                        # توزيع الأرباح على الجهات المستفيدة المحددة في شروط هذا الوقف بالذات
                        conditions = db.query(WaqfCondition).filter(WaqfCondition.waqf_fund_id == waqf_fund.id).all()
                        for cond in conditions:
                            disb_amount = fund_share_of_net * (cond.percentage / 100.0)
                            disbursement = BeneficiaryDisbursement(
                                settlement_id=settlement.id,
                                waqf_fund_id=waqf_fund.id,
                                category_id=cond.category_id,
                                beneficiary_user_id=cond.specific_beneficiary_id,
                                amount=disb_amount,
                                disbursement_method="BANK_TRANSFER",
                                transaction_ref=f"DISB-{uuid.uuid4().hex[:8].upper()}",
                                status="TRANSFERRED"
                            )
                            db.add(disbursement)

                        # إشعار الواقف بتفاصيل الأرباح ومصارفها
                        db.add(Notification(
                            user_id=waqf_fund.waqif_id,
                            title="تحقيق وتوزيع أرباح وقفك المستقل",
                            message=(
                                f"الحمد لله، حقق وقفك '{waqf_fund.waqf_title}' عائداً صافياً قدره {fund_share_of_net:,.2f} د.ج "
                                f"من مشروع '{project.title}'، وتم تحويل العوائد فوراً للجهات المستفيدة وفق شرطك."
                            ),
                            notification_type="PROFIT_DISTRIBUTION",
                            action_url="/dashboard/waqif"
                        ))

            elif f.funding_source == "INDIVIDUAL" and f.funder_id:
                # إشعار الممول الفردي وإيداع حصته في محفظته
                if individual_capital > 0 and calc["individual_funders_share"] > 0:
                    funder_share = calc["individual_funders_share"] * (f.amount / individual_capital)
                    db.add(Notification(
                        user_id=f.funder_id,
                        title="إيداع عوائد استثمارك في المشروع",
                        message=f"تم إيداع حصتك من أرباح مشروع '{project.title}' البالغة {funder_share:,.2f} د.ج في حسابك الاستثماري.",
                        notification_type="PROFIT_DISTRIBUTION",
                        action_url="/dashboard/funder"
                    ))

        # تحديث حالة المشروع
        project.status = "COMPLETED"
        project.is_returns_distributed = True
        project.execution_progress_pct = 100.0

        # إشعار صاحب المشروع
        db.add(Notification(
            user_id=project.owner_id,
            title="اكتمال تسوية المشروع واعتماد الأرباح",
            message=f"تمت التسوية المالية لمشروعك '{project.title}' بنجاح، وبلغت حصتك من الأرباح {calc['owner_share']:,.2f} د.ج.",
            notification_type="SUCCESS"
        ))

        db.commit()
        db.refresh(settlement)
        return settlement

