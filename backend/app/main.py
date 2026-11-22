"""
الملف الرئيسي لتشغيل منصة 'وقف تاك' (WaqfTech)
متوافقة مع القانون الجزائري للأوقاف 25-06 لسنة 2025
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

from app.config import settings, WAQF_CATEGORIES, INVESTMENT_SECTORS, ISLAMIC_FINANCING_FORMULAS
from app.database import engine, Base, SessionLocal
from app.api import auth, waqf, projects, funding, returns, governance

# إنشاء جداول قاعدة البيانات فورياً
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # بذر بيانات تجريبية أولية مطابقة للقانون الجزائري لتسهيل التصفح الفوري
    seed_initial_data()
    yield

app = FastAPI(
    title=settings.PLATFORM_NAME,
    description="المنصة الوقفية الاستثمارية المعتمدة وفق القانون الجزائري رقم 25-06 الصادر بتاريخ 23 محرم 1447هـ الموافق 19 يوليو 2025م",
    version=settings.PLATFORM_VERSION,
    lifespan=lifespan
)

# تمكين CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط المجلدات الساكنة والقوالب
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")

if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# تضمين مسارات الـ API
app.include_router(auth.router)
app.include_router(waqf.router)
app.include_router(projects.router)
app.include_router(funding.router)
app.include_router(returns.router)
app.include_router(governance.router)

# ----------------- مسارات صفحات الويب التفاعلية (UI) -----------------

@app.get("/", response_class=HTMLResponse, summary="الصفحة الرئيسية للمنصة")
def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={
        "platform_name": settings.PLATFORM_NAME,
        "law_ref": settings.LAW_REFERENCE,
        "currency": settings.CURRENCY_AR,
        "categories": WAQF_CATEGORIES,
        "sectors": INVESTMENT_SECTORS,
        "formulas": ISLAMIC_FINANCING_FORMULAS
    })

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"platform_name": settings.PLATFORM_NAME})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"platform_name": settings.PLATFORM_NAME})

@app.get("/dashboard/waqif", response_class=HTMLResponse)
def waqif_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard_waqif.html", context={
        "platform_name": settings.PLATFORM_NAME,
        "categories": WAQF_CATEGORIES,
        "cooling_off_hours": settings.COOLING_OFF_PERIOD_HOURS,
        "currency": settings.CURRENCY_AR
    })

@app.get("/dashboard/project", response_class=HTMLResponse)
def project_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard_project.html", context={
        "platform_name": settings.PLATFORM_NAME,
        "sectors": INVESTMENT_SECTORS,
        "formulas": ISLAMIC_FINANCING_FORMULAS,
        "currency": settings.CURRENCY_AR
    })

@app.get("/dashboard/funder", response_class=HTMLResponse)
def funder_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard_funder.html", context={
        "platform_name": settings.PLATFORM_NAME,
        "sectors": INVESTMENT_SECTORS,
        "formulas": ISLAMIC_FINANCING_FORMULAS,
        "currency": settings.CURRENCY_AR
    })

@app.get("/dashboard/sharia", response_class=HTMLResponse)
def sharia_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard_sharia.html", context={
        "platform_name": settings.PLATFORM_NAME
    })

@app.get("/dashboard/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard_admin.html", context={
        "platform_name": settings.PLATFORM_NAME,
        "currency": settings.CURRENCY_AR
    })

@app.get("/transparency", response_class=HTMLResponse)
def transparency_page(request: Request):
    return templates.TemplateResponse(request=request, name="transparency.html", context={
        "platform_name": settings.PLATFORM_NAME,
        "law_ref": settings.LAW_REFERENCE,
        "categories": WAQF_CATEGORIES,
        "sectors": INVESTMENT_SECTORS,
        "formulas": ISLAMIC_FINANCING_FORMULAS
    })

# ----------------- دالة بذر البيانات الأولية -----------------
def seed_initial_data():
    db = SessionLocal()
    try:
        from app.models.user import User
        from app.models.project import Project, ProjectMilestone
        from app.models.audit import ShariaAuditReport
        from app.security import hash_password
        from datetime import datetime

        if db.query(User).count() == 0:
            # 1. إنشاء حساب ناظر الوقف (الإدارة)
            admin = User(
                full_name="إدارة منصة وقف تاك (الناظر المعتمد)",
                phone="0550000001",
                email="admin@waqftech.dz",
                hashed_password=hash_password("admin123456"),
                is_active=True,
                is_phone_verified=True,
                kyc_status="APPROVED",
                is_admin=True
            )
            # 2. عضو الهيئة الشرعية المستقلة
            sharia_member = User(
                full_name="د. عبد الرحمن الجزائري (رئيس الهيئة الشرعية المستقلة)",
                phone="0550000002",
                email="sharia@waqftech.dz",
                hashed_password=hash_password("sharia123456"),
                is_active=True,
                is_phone_verified=True,
                kyc_status="APPROVED",
                is_sharia_board=True
            )
            # 3. حساب واقف تجريبي
            waqif_demo = User(
                full_name="الحاج البشير الإبراهيمي (واقف)",
                phone="0550000003",
                email="waqif@waqftech.dz",
                hashed_password=hash_password("waqif123456"),
                is_active=True,
                is_phone_verified=True,
                kyc_status="APPROVED",
                is_waqif=True,
                aml_declaration_accepted=True,
                aml_source_of_funds="مدخرات شخصية ناتجة عن نشاط تجاري مشروع"
            )
            # 4. حساب ممول فردي تجريبي
            funder_demo = User(
                full_name="كريم بلقاسم (مستثمر ممول)",
                phone="0550000004",
                email="funder@waqftech.dz",
                hashed_password=hash_password("funder123456"),
                is_active=True,
                is_phone_verified=True,
                kyc_status="APPROVED",
                is_funder=True,
                funder_risk_profile="MEDIUM",
                funder_max_limit=1500000.0
            )
            # 5. حساب رائد أعمال (صاحب مشروع)
            project_owner_demo = User(
                full_name="أحمد زبانا (صاحب مشروع أغذية بيولوجية)",
                phone="0550000005",
                email="entrepreneur@waqftech.dz",
                hashed_password=hash_password("owner123456"),
                is_active=True,
                is_phone_verified=True,
                kyc_status="APPROVED",
                is_project_owner=True,
                company_name="شركة الواحات للصناعات الزراعية ش.ذ.م.م",
                commercial_register_num="16/00-123456B24",
                tax_id_num="002416001234567"
            )
            # 6. حساب جهة مستفيدة معتمدة
            charity_demo = User(
                full_name="جمعية البر لرعاية الأيتام والتعليم",
                phone="0550000006",
                email="charity@waqftech.dz",
                hashed_password=hash_password("charity123456"),
                is_active=True,
                is_phone_verified=True,
                kyc_status="APPROVED",
                is_beneficiary=True,
                organization_name="جمعية البر لرعاية الأيتام - فرع الجزائر",
                legal_approval_number="اعتماد ولائي رقم 1445/2024",
                bank_account_rip="00100 12345 6789012345 67",
                beneficiary_category="orphans",
                is_vetted_beneficiary=True
            )

            db.add_all([admin, sharia_member, waqif_demo, funder_demo, project_owner_demo, charity_demo])
            db.commit()

            # إنشاء مشاريع نموذجية معتمدة عبر الصيغ الإسلامية والقطاعات
            prj1 = Project(
                owner_id=project_owner_demo.id,
                project_code="PRJ-AGR-2025-001",
                title="توسيع مزارع النخيل وإنتاج التمور البيولوجية بصيغة المزارعة والمساقاة",
                description="مشروع زراعي متكامل في ولاية بسكرة يهدف إلى غرس 1,000 نخلة دقلة نور واستصلاح 20 هكتاراً بتقنيات الري بالتنقيط والطاقة الشمسية.",
                sector="agricultural",
                islamic_formula="muzaraa",
                requested_amount=3000000.0,
                funded_amount=1500000.0,
                duration_months=18,
                expected_return_rate=14.5,
                risk_grade="LOW",
                status="APPROVED_FOR_FUNDING",
                sharia_status="APPROVED",
                sharia_opinion_text="المشروع معتمد شرعياً بصيغة المزارعة والمساقاة وفق المادتين 71 و 72 من القانون 25-06، مع عدالة قسمة الغلة.",
                sharia_scholar_signature="د. عبد الرحمن الجزائري",
                guarantees_description="رهن حيازي للأرض الزراعية والعتاد الآلي"
            )

            prj2 = Project(
                owner_id=project_owner_demo.id,
                project_code="PRJ-IND-2025-002",
                title="خط إنتاج المستلزمات الطبية المعقمة بصيغة الاستصناع",
                description="تصنيع وتجهيز غرف نظيفة ومعدات طبية موجهة للمستشفيات والمراكز الصحية الوطنية لتقليص فاتورة الاستيراد.",
                sector="industrial",
                islamic_formula="istisna",
                requested_amount=5000000.0,
                funded_amount=2000000.0,
                duration_months=12,
                expected_return_rate=16.0,
                risk_grade="MEDIUM",
                status="APPROVED_FOR_FUNDING",
                sharia_status="APPROVED",
                sharia_opinion_text="معتمد بصيغة الاستصناع وفق المادة 75 من القانون 25-06 مع جدول دفعات تسليم معتمد.",
                sharia_scholar_signature="د. عبد الرحمن الجزائري",
                guarantees_description="كفالة بنكية ورهن الآلات الصناعية"
            )

            prj3 = Project(
                owner_id=project_owner_demo.id,
                project_code="PRJ-SRV-2025-003",
                title="تجهيز مركز فحص وتشخيص طبي متطور بصيغة الإجارة",
                description="اقتناء أجهزة أشعة ورنين مغناطيسي وتأجيرها لعيادة خيرية وخدمية بأجرة دورية منتظمة تضمن تدفق عوائد مستقرة.",
                sector="services",
                islamic_formula="ijarah",
                requested_amount=4000000.0,
                funded_amount=4000000.0,
                duration_months=24,
                expected_return_rate=12.0,
                risk_grade="LOW",
                status="IN_EXECUTION",
                sharia_status="APPROVED",
                sharia_opinion_text="مطابق لأحكام عقد الإجارة الوارد في المادة 70 من القانون 25-06.",
                sharia_scholar_signature="د. عبد الرحمن الجزائري",
                execution_progress_pct=50.0,
                guarantees_description="ملكية المعدات مسجلة باسم الناظر طيلة فترة الإيجار"
            )

            db.add_all([prj1, prj2, prj3])
            db.commit()

            # تقرير هيئة الرقابة الشرعية الافتتاحي
            sharia_rep = ShariaAuditReport(
                report_title="تقرير الاعتماد الشرعي لمنصة وقف تاك وصيغ الاستثمار المعتمدة",
                quarter="الربع الثالث 2025",
                compliance_verdict="FULLY_COMPLIANT",
                auditor_names="الهيئة الشرعية المستقلة للأوقاف والاستثمار الإسلامي",
                summary_findings="تمت مراجعة العقود النموذجية للوقف المستقل وعقود التمويل بالصيغ السبع، والتأكد من مطابقتها لنصوص القانون الجزائري رقم 25-06 (الفصل العاشر) وللمعايير الشرعية الدولية.",
                recommendations="الاستمرار في إلغاء ضمان رأس المال والتأكيد على المتابعة الميدانية للإنفاق عبر حسابات الضمان المنفصلة.",
                is_published=True
            )
            db.add(sharia_rep)
            db.commit()
    finally:
        db.close()
