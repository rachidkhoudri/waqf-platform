"""
خدمات إدارة المشاريع، المراجعة الفنية والشرعية، مراحل الإنجاز، والتمويل
"""
from datetime import datetime
import uuid
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.config import settings, INVESTMENT_SECTORS, ISLAMIC_FINANCING_FORMULAS
from app.models.user import User
from app.models.project import Project, ProjectMilestone
from app.models.funding import ProjectFunding
from app.models.waqf import WaqfFund
from app.models.notification import Notification
from app.services.contract_generator import ContractGenerator

class ProjectService:
    @staticmethod
    def submit_project(
        db: Session,
        owner: User,
        title: str,
        description: str,
        sector: str, # industrial, commercial, agricultural, services, infrastructure
        islamic_formula: str, # musharaka, mudaraba, murabaha, salam, istisna, ijarah, muzaraa
        requested_amount: float,
        duration_months: int,
        expected_return_rate: float,
        expected_return_min: Optional[float] = None,
        expected_return_max: Optional[float] = None,
        guarantees: str = "",
        milestones_data: List[Dict] = None
    ) -> Project:
        """
        تقديم طلب تمويل مشروع جديد (المرحلة 7)
        """
        if sector not in INVESTMENT_SECTORS:
            raise ValueError(f"القطاع الاستثماري غير صالح. الخيارات المتاحة: {list(INVESTMENT_SECTORS.keys())}")
        if islamic_formula not in ISLAMIC_FINANCING_FORMULAS:
            raise ValueError(f"الصيغة التمويلية غير صالحة. الخيارات المتاحة: {list(ISLAMIC_FINANCING_FORMULAS.keys())}")

        project_code = f"PRJ-{sector[:3].upper()}-{datetime.utcnow().year}-{uuid.uuid4().hex[:6].upper()}"

        project = Project(
            owner_id=owner.id,
            project_code=project_code,
            title=title,
            description=description,
            sector=sector,
            islamic_formula=islamic_formula,
            requested_amount=requested_amount,
            funded_amount=0.0,
            duration_months=duration_months,
            expected_return_rate=expected_return_rate,
            expected_return_min=expected_return_min or (expected_return_rate * 0.8),
            expected_return_max=expected_return_max or (expected_return_rate * 1.2),
            guarantees_description=guarantees,
            status="SUBMITTED",
            risk_grade="MEDIUM",
            sharia_status="PENDING"
        )
        db.add(project)
        db.flush()

        # إضافة مراحل الإنجاز والصرف (Milestones)
        if milestones_data:
            for idx, m in enumerate(milestones_data):
                ms = ProjectMilestone(
                    project_id=project.id,
                    milestone_number=idx + 1,
                    title=m.get("title", f"المرحلة {idx+1}"),
                    description=m.get("description", ""),
                    target_progress_pct=m.get("target_progress_pct", 100.0),
                    disbursement_amount=m.get("disbursement_amount", requested_amount),
                    status="PENDING"
                )
                db.add(ms)
        else:
            # افتراضياً مرحلتان (50% عند البدء و 50% عند الإنجاز النصفي)
            db.add(ProjectMilestone(
                project_id=project.id,
                milestone_number=1,
                title="الدفعة التشغيلية الأولى بعد استيفاء الضمانات",
                description="شراء المواد الأولية أو الآلات حسب الصيغة",
                target_progress_pct=20.0,
                disbursement_amount=requested_amount * 0.5,
                status="PENDING"
            ))
            db.add(ProjectMilestone(
                project_id=project.id,
                milestone_number=2,
                title="الدفعة التشغيلية الثانية",
                description="اكتمال خط الإنتاج وبدء التسويق الفعلي",
                target_progress_pct=60.0,
                disbursement_amount=requested_amount * 0.5,
                status="PENDING"
            ))

        notification = Notification(
            user_id=owner.id,
            title="تم استلام طلب التمويل",
            message=f"تم استلام طلب تمويل مشروع '{title}' برمز ({project_code}). سيتم دراسته فنياً ثم عرضه على الهيئة الشرعية.",
            notification_type="INFO"
        )
        db.add(notification)

        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def approve_sharia_review(
        db: Session,
        project_id: int,
        sharia_scholar_name: str,
        is_approved: bool,
        notes: str,
        assigned_risk_grade: str = "MEDIUM"
    ) -> Project:
        """
        قرار الهيئة الشرعية المستقلة وتصنيف المخاطر (المرحلة 8)
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("المشروع غير موجود")

        if is_approved:
            project.sharia_status = "APPROVED"
            project.status = "APPROVED_FOR_FUNDING" # يطرح في الفرص الاستثمارية للممولين والوقف
            project.risk_grade = assigned_risk_grade
            project.sharia_decision_date = datetime.utcnow()
            project.sharia_scholar_signature = sharia_scholar_name
            project.sharia_opinion_text = notes or "المشروع متوافق مع أحكام الشريعة الإسلامية ومطابق لمعايير الاستثمار الوقفي."

            # إشعار صاحب المشروع
            db.add(Notification(
                user_id=project.owner_id,
                title="موافقة الهيئة الشرعية واعتماد المشروع",
                message=f"تمت إجازة مشروع '{project.title}' شرعياً وطرحه رسمياً للاستثمار والتمويل في المنصة.",
                notification_type="SUCCESS"
            ))
        else:
            project.sharia_status = "REJECTED"
            project.status = "REJECTED"
            project.rejection_reason = notes or "عدم توافق النشاط أو بنود التعاقد مع الضوابط الشرعية."
            
            db.add(Notification(
                user_id=project.owner_id,
                title="قرار الهيئة الشرعية بشأن المشروع",
                message=f"نعتذر، لم تجز الهيئة الشرعية مشروع '{project.title}'. السبب: {project.rejection_reason}",
                notification_type="WARNING"
            ))

        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def fund_project_with_waqf(
        db: Session,
        project_id: int,
        waqf_fund_id: int,
        allocation_amount: float
    ) -> ProjectFunding:
        """
        تخصيص تمويل من المحفظة الوقفية المستقلة لمشروع معتمد (المرحلة 10 و 11)
        مع احترام حدود التنويع والسيولة
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        waqf_fund = db.query(WaqfFund).filter(WaqfFund.id == waqf_fund_id).first()
        
        if not project or project.status not in ["APPROVED_FOR_FUNDING", "PARTIALLY_FUNDED"]:
            raise ValueError("المشروع غير مؤهل أو غير مطروح للتمويل حالياً")
        if not waqf_fund or waqf_fund.uninvested_cash < allocation_amount:
            raise ValueError("رصيد السيولة غير المستثمرة في هذا الوقف غير كافٍ")
        if (project.funded_amount + allocation_amount) > project.requested_amount:
            raise ValueError("المبلغ المخصص يتجاوز السقف الإجمالي المطلوب للمشروع")

        # خصم من سيولة الوقف وإضافته للمستثمر
        waqf_fund.uninvested_cash -= allocation_amount
        waqf_fund.current_invested_amount += allocation_amount
        project.funded_amount += allocation_amount
        
        if project.funded_amount >= project.requested_amount:
            project.status = "FUNDED"

        escrow_acc = f"ESCROW-WAQF-{project.project_code}-{uuid.uuid4().hex[:6].upper()}"
        contract_info = ContractGenerator.generate_funding_contract(
            funder_name=f"محفظة {waqf_fund.waqf_title} ({waqf_fund.waqf_code})",
            project_title=project.title,
            sector=project.sector,
            islamic_formula=project.islamic_formula,
            amount=allocation_amount,
            agreed_profit_pct=project.expected_return_rate,
            escrow_account=escrow_acc
        )

        funding = ProjectFunding(
            project_id=project.id,
            funding_source="WAQF",
            waqf_fund_id=waqf_fund.id,
            amount=allocation_amount,
            agreed_profit_share_pct=project.expected_return_rate,
            contract_number=contract_info["contract_number"],
            contract_signed=True,
            contract_signed_at=datetime.utcnow(),
            contract_text_ar=contract_info["contract_text"],
            escrow_account_num=escrow_acc,
            status="IN_ESCROW"
        )
        db.add(funding)

        # إشعار الواقف
        db.add(Notification(
            user_id=waqf_fund.waqif_id,
            title="استثمار جزء من وقفك في مشروع تنموي",
            message=f"تم استثمار مبلغ {allocation_amount:,.2f} د.ج من وقفك في مشروع '{project.title}' بصيغة {project.islamic_formula}.",
            notification_type="INFO"
        ))

        db.commit()
        db.refresh(funding)
        return funding

    @staticmethod
    def fund_project_with_individual(
        db: Session,
        project_id: int,
        funder: User,
        amount: float
    ) -> ProjectFunding:
        """
        تمويل مشروع من طرف ممول فردي (بماله الخاص - المرحلة 10 و 11)
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project or project.status not in ["APPROVED_FOR_FUNDING", "PARTIALLY_FUNDED"]:
            raise ValueError("المشروع غير مطروح للتمويل حالياً")
        if amount > funder.funder_max_limit:
            raise ValueError(f"المبلغ يتجاوز الحد الأقصى المصرح به لملفك الاستثماري ({funder.funder_max_limit:,.2f} د.ج)")
        if (project.funded_amount + amount) > project.requested_amount:
            raise ValueError("المبلغ يتجاوز المتبقي من حجم تمويل المشروع")

        project.funded_amount += amount
        if project.funded_amount >= project.requested_amount:
            project.status = "FUNDED"

        escrow_acc = f"ESCROW-FND-{project.project_code}-{uuid.uuid4().hex[:6].upper()}"
        contract_info = ContractGenerator.generate_funding_contract(
            funder_name=funder.full_name,
            project_title=project.title,
            sector=project.sector,
            islamic_formula=project.islamic_formula,
            amount=amount,
            agreed_profit_pct=project.expected_return_rate,
            escrow_account=escrow_acc
        )

        funding = ProjectFunding(
            project_id=project.id,
            funding_source="INDIVIDUAL",
            funder_id=funder.id,
            amount=amount,
            agreed_profit_share_pct=project.expected_return_rate,
            contract_number=contract_info["contract_number"],
            contract_signed=True,
            contract_signed_at=datetime.utcnow(),
            contract_text_ar=contract_info["contract_text"],
            escrow_account_num=escrow_acc,
            status="IN_ESCROW"
        )
        db.add(funding)

        db.add(Notification(
            user_id=funder.id,
            title="تم توقيع عقد التمويل بنجاح",
            message=f"تم تمويل مشروع '{project.title}' بمبلغ {amount:,.2f} د.ج وإيداع المبلغ في حساب الضمان.",
            notification_type="SUCCESS"
        ))

        db.commit()
        db.refresh(funding)
        return funding
