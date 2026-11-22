"""
خدمات إدارة الأوقاف المستقلة، الإيداع، فترة التراجع (72 ساعة)، والشهادات
"""
from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user import User
from app.models.waqf import WaqfFund, WaqfDeposit, WaqfCondition, WaqfContract
from app.models.notification import Notification
from app.services.contract_generator import ContractGenerator

class WaqfService:
    @staticmethod
    def create_independent_waqf(
        db: Session,
        waqif: User,
        waqf_title: str,
        amount: float,
        payment_method: str, # CIB_CARD, EDAHABIA, BANK_TRANSFER
        waqf_type: str = "PERPETUAL", # PERPETUAL, TEMPORARY
        temporary_months: Optional[int] = None,
        temporary_destination: Optional[str] = None,
        conditions_data: List[Dict] = None,
        risk_preference: str = "CONSERVATIVE",
        client_ip: str = "127.0.0.1"
    ) -> WaqfFund:
        """
        إنشاء وقف نقدي مستقل وتوثيق العقد وبدء فترة المراجعة (72 ساعة)
        """
        if amount < settings.DEFAULT_MIN_WAQF_AMOUNT:
            raise ValueError(f"الحد الأدنى للوقف هو {settings.DEFAULT_MIN_WAQF_AMOUNT:,.2f} {settings.CURRENCY_AR}")

        # التحقق من مجموع نسب الشروط (يجب أن تساوي 100%)
        if conditions_data:
            total_pct = sum([c.get("percentage", 0) for c in conditions_data])
            if abs(total_pct - 100.0) > 0.01:
                raise ValueError(f"مجموع نسب توزيع الوقف يجب أن يساوي 100% (المجموع الحالي: {total_pct}%)")
        else:
            # افتراضياً وقف لخدمة المجتمع
            conditions_data = [{"category_id": "community", "percentage": 100.0, "additional_conditions": "وجوه البر العامة"}]

        # توليد رمز الوقف المستقل
        waqf_code = f"WQF-DZ-{datetime.utcnow().year}-{uuid.uuid4().hex[:6].upper()}"
        cooling_off_expires = datetime.utcnow() + timedelta(hours=settings.COOLING_OFF_PERIOD_HOURS)

        # 1. إنشاء سجل الوقف المستقل
        waqf_fund = WaqfFund(
            waqif_id=waqif.id,
            waqf_code=waqf_code,
            waqf_title=waqf_title,
            waqf_type=waqf_type,
            temporary_duration_months=temporary_months,
            temporary_end_date=datetime.utcnow() + timedelta(days=temporary_months*30) if temporary_months else None,
            temporary_capital_destination=temporary_destination,
            capital_corpus=amount,
            uninvested_cash=amount,
            current_invested_amount=0.0,
            status="PENDING_COOLING_OFF",
            cooling_off_expires_at=cooling_off_expires,
            can_withdraw_now=True,
            risk_preference=risk_preference,
            cy_pres_accepted=True
        )
        db.add(waqf_fund)
        db.flush()

        # 2. إنشاء سجل الإيداع المالي
        deposit = WaqfDeposit(
            waqf_fund_id=waqf_fund.id,
            waqif_id=waqif.id,
            amount=amount,
            payment_method=payment_method,
            transaction_ref=f"TXN-{uuid.uuid4().hex[:10].upper()}",
            payment_status="SUCCESS"
        )
        db.add(deposit)

        # 3. تسجيل شروط الوقف والجهات المستفيدة
        for cond in conditions_data:
            condition_record = WaqfCondition(
                waqf_fund_id=waqf_fund.id,
                category_id=cond.get("category_id"),
                specific_beneficiary_id=cond.get("specific_beneficiary_id"),
                percentage=cond.get("percentage", 100.0),
                geographic_scope=cond.get("geographic_scope"),
                target_demographic=cond.get("target_demographic"),
                custom_condition_notes=cond.get("custom_condition_notes")
            )
            db.add(condition_record)

        # 4. توليد العقد والشهادة الرقمية وتوقيع العقد إلكترونياً
        contract_info = ContractGenerator.generate_waqf_contract(
            waqif_name=waqif.full_name,
            waqif_id_number=waqif.kyc_id_number or "مفحوص ومثبت بالملف",
            waqif_address="الجزائر",
            waqf_title=waqf_title,
            waqf_code=waqf_code,
            amount=amount,
            waqf_type=waqf_type,
            temporary_months=temporary_months,
            temporary_destination=temporary_destination,
            conditions=conditions_data,
            risk_preference=risk_preference
        )

        contract = WaqfContract(
            waqf_fund_id=waqf_fund.id,
            waqif_id=waqif.id,
            contract_number=contract_info["contract_number"],
            contract_title=f"عقد إنشاء {waqf_title}",
            contract_text_ar=contract_info["contract_text"],
            signed_electronically=True,
            signed_at=datetime.utcnow(),
            signer_ip_address=client_ip,
            certificate_code=contract_info["certificate_code"]
        )
        db.add(contract)

        # 5. إشعار الواقف
        notification = Notification(
            user_id=waqif.id,
            title="تم إيداع الوقف وتوقيع العقد بنجاح",
            message=f"تم تسجيل وقفك المستقل '{waqf_title}' برمز ({waqf_code}) ومبلغ {amount:,.2f} د.ج. لديك مهلة تراجع مدتها 72 ساعة.",
            notification_type="SUCCESS",
            action_url=f"/dashboard/waqif"
        )
        db.add(notification)

        db.commit()
        db.refresh(waqf_fund)
        return waqf_fund

    @staticmethod
    def check_and_update_cooling_off(db: Session, waqf_fund: WaqfFund) -> WaqfFund:
        """
        التحقق من انتهاء فترة الـ 72 ساعة وجعل الوقف لازماً
        """
        if waqf_fund.status == "PENDING_COOLING_OFF":
            if datetime.utcnow() >= waqf_fund.cooling_off_expires_at:
                waqf_fund.status = "ACTIVE"
                waqf_fund.can_withdraw_now = False
                db.commit()
                db.refresh(waqf_fund)
        return waqf_fund

    @staticmethod
    def withdraw_cooling_off(db: Session, waqf_fund_id: int, waqif_id: int) -> Dict[str, Any]:
        """
        سحب المبلغ وإلغاء الوقف خلال فترة الـ 72 ساعة (حماية الواقف)
        """
        waqf = db.query(WaqfFund).filter(WaqfFund.id == waqf_fund_id, WaqfFund.waqif_id == waqif_id).first()
        if not waqf:
            raise ValueError("الوقف غير موجود أو لا تملك صلاحية عليه")
        
        if datetime.utcnow() > waqf.cooling_off_expires_at or waqf.status != "PENDING_COOLING_OFF":
            raise ValueError("انقضت مهلة التراجع (72 ساعة) وأصبح الوقف لازماً وناجزاً قانوناً عملاً بالمادة 19.")

        refund_amount = waqf.capital_corpus
        waqf.status = "CANCELLED_COOLING_OFF"
        waqf.can_withdraw_now = False
        waqf.capital_corpus = 0.0
        waqf.uninvested_cash = 0.0

        # تسجيل استرجاع الإيداع
        deposit = db.query(WaqfDeposit).filter(WaqfDeposit.waqf_fund_id == waqf.id).first()
        if deposit:
            deposit.payment_status = "REFUNDED"
            deposit.is_refunded_cooling_off = True

        notification = Notification(
            user_id=waqif_id,
            title="تم إلغاء الوقف واسترجاع المبلغ بنجاح",
            message=f"بناءً على طلبك خلال فترة التراجع (72 ساعة)، تم استرجاع مبلغ {refund_amount:,.2f} د.ج إلى وسيلة الدفع الخاصة بك.",
            notification_type="INFO"
        )
        db.add(notification)
        db.commit()

        return {
            "success": True,
            "refund_amount": refund_amount,
            "message": "تم سحب المبلغ وإلغاء الوقف بنجاح خلال فترة السماح."
        }
