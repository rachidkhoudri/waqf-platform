"""
إعدادات وثوابت منصة 'وقف تاك' (WaqfTech)
متوافقة تماماً مع القانون الجزائري للأوقاف رقم 25-06 الصادر بتاريخ 23 محرم 1447هـ الموافق 19 يوليو 2025م
(الجريدة الرسمية رقم 47 المؤرخة في 22 يوليو 2025)
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # معلومات المنصة
    PLATFORM_NAME: str = "منصة وقف تاك (WaqfTech)"
    PLATFORM_VERSION: str = "2.0.0"
    JURISDICTION: str = "الجمهورية الجزائرية الديمقراطية الشعبية"
    LAW_REFERENCE: str = "القانون رقم 25-06 المؤرخ في 23 محرم عام 1447 الموافق 19 يوليو 2025 المتعلق بالأوقاف (الجريدة الرسمية رقم 47)"
    
    # العملة والمالية
    CURRENCY: str = "DZD"  # الدينار الجزائري
    CURRENCY_AR: str = "د.ج"
    DEFAULT_MIN_WAQF_AMOUNT: float = 5000.0  # الحد الأدنى للإيداع الوقفي 5,000 د.ج
    
    # قرارات السيناريو
    INDEPENDENT_WAQF_ACCOUNTS: bool = True  # لكل واقف وقف مستقل بحساباته وسجلاته
    ALLOW_TEMPORARY_WAQF: bool = True      # قبول الوقف المؤقت وفق المادة 22
    ALLOW_PERPETUAL_WAQF: bool = True      # قبول الوقف المؤبد وفق المادة 22
    ALLOW_INDIVIDUAL_FUNDERS: bool = True  # قبول تمويل الأفراد جنباً إلى جنب مع الوقف
    
    # الحوكمة ونسب التوزيع
    DEFAULT_NAZIR_FEE_PERCENTAGE: float = 10.0   # نسبة أجرة الناظر (10% من الأرباح المحققة) قابلة للتعديل بقرار رسمي
    DEFAULT_RESERVE_FUND_PERCENTAGE: float = 5.0 # نسبة صندوق الاحتياطي الوقفي لمواجهة مخاطر الاستثمار
    COOLING_OFF_PERIOD_HOURS: int = 72          # فترة التراجع القانونية للواقف (72 ساعة)
    
    # الأمان وقاعدة البيانات
    SECRET_KEY: str = os.getenv("SECRET_KEY", "waqftech-secret-key-dz-2025-algeria-baraka-islamic-fintech")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # أسبوع واحد
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./waqftech.db")
    
    # إعدادات الامتثال ومكافحة غسل الأموال (قانون 05-01 المعدل والمتمم والمادة 15 و 109 من قانون 25-06)
    AML_STRICT_MODE: bool = True
    MAX_UNVERIFIED_ACTIONS: int = 0  # لا يُسمح بأي إجراء مالي قبل التحقق الكامل KYC
    
    class Config:
        case_sensitive = True

settings = Settings()

# الفئات الوقفية الثمانية المعتمدة
WAQF_CATEGORIES = {
    "education": {
        "id": "education",
        "name": "وقف على العلم",
        "description": "مدارس، جامعات، مراكز بحثية، منح دراسية، ومخابر الابتكار",
        "icon": "academic-cap"
    },
    "health": {
        "id": "health",
        "name": "وقف على الصحة",
        "description": "مستشفيات، عيادات خيرية، أجهزة طبية، حملات وقائية وعلاجية",
        "icon": "heart"
    },
    "environment": {
        "id": "environment",
        "name": "وقف على البيئة",
        "description": "مشاريع تشجير ومكافحة التصحر، طاقات متجددة، حماية الموارد المائية",
        "icon": "globe-alt"
    },
    "family_childhood": {
        "id": "family_childhood",
        "name": "وقف على رعاية الأسرة والطفولة",
        "description": "مراكز تأهيل أسري، دعم الأمهات، برامج حماية وتنمية الطفولة",
        "icon": "user-group"
    },
    "quran_sunnah": {
        "id": "quran_sunnah",
        "name": "وقف على خدمة القرآن والسنة",
        "description": "مدارس قرآنية وزوايا، طباعة المصاحف، مسابقات وبرامج الحديث النبوي",
        "icon": "book-open"
    },
    "orphans": {
        "id": "orphans",
        "name": "وقف على اليتامى",
        "description": "كفالة معيشية وتعليمية، تأهيل مهني، ورعاية شاملة للأيتام وذويهم",
        "icon": "shield-check"
    },
    "mosques": {
        "id": "mosques",
        "name": "وقف لرعاية المساجد",
        "description": "بناء وصيانة بيوت الله، تجهيزات الطاقة النظيفة، أنشطة دعوية ومكتبات",
        "icon": "building-library"
    },
    "community": {
        "id": "community",
        "name": "وقف لخدمة المجتمع",
        "description": "مشاريع تنموية شاملة، إغاثة الكوارث، تكافل اجتماعي وقروض حسنة",
        "icon": "hand-raised"
    }
}

# القطاعات الاستثمارية الخمسة
INVESTMENT_SECTORS = {
    "industrial": {"name": "صناعي", "description": "الصناعات التحويلية، الحرفية، والإنتاج التقني والصيدلاني"},
    "commercial": {"name": "تجاري", "description": "سلاسل التوريد، التوزيع، التجارة المحلية وتصدير المنتجات الوطنية"},
    "agricultural": {"name": "زراعي", "description": "الإنتاج النباتي والحيواني، الصناعات الغذائية، واستصلاح الأراضي"},
    "services": {"name": "خدمي", "description": "التعليم والتدريب، الرعاية الصحية، الخدمات اللوجستية وتكنولوجيا المعلومات"},
    "infrastructure": {"name": "بنية تحتية", "description": "الطاقة المستدامة، محطات التحلية، شبكات الري والمرافق المستدامة"}
}

# الصيغ التمويلية الإسلامية السبع المعتمدة في القانون 25-06
ISLAMIC_FINANCING_FORMULAS = {
    "musharaka": {
        "name": "المشاركة",
        "legal_article": "المادة 78 من القانون 25-06",
        "nature": "عقد يبرم للمشاركة في رأس المال والربح",
        "return_source": "حصة شائعة متفق عليها من صافي الربح الفعلي",
        "loss_bearer": "يتحمل كل شريك الخسارة بقدر حصته في رأس المال فقط",
        "category": "partnership"
    },
    "mudaraba": {
        "name": "المضاربة (القراض)",
        "legal_article": "المادة 81 من القانون 25-06",
        "nature": "رأس مال من جهة التمويل وعمل وخبرة من رائد الأعمال",
        "return_source": "نسبة مئوية محددة من الأرباح المحققة",
        "loss_bearer": "الخسارة المالية على رب المال والجهد على المضارب ما لم يثبت تعدٍّ أو تقصير",
        "category": "partnership"
    },
    "murabaha": {
        "name": "المرابحة للآمر بالشراء",
        "legal_article": "المادة 82 من القانون 25-06",
        "nature": "تمليك السلعة للمستفيد بتكلفتها مع هامش ربح معلوم مسبقاً",
        "return_source": "هامش الربح التعاقدي المعلوم فوق سعر التكلفة",
        "loss_bearer": "التزام المشتري بالسداد مع توفير ضمانات وكفالات مشروعة",
        "category": "debt_trade"
    },
    "salam": {
        "name": "السَّلَم",
        "legal_article": "المادة 83 من القانون 25-06",
        "nature": "شراء سلعة موصوفة في الذمة بثمن عاجل وتسليم آجل",
        "return_source": "فارق القيمة السوقية عند بيع السلعة المستلمة أو تسويقها بموازاة",
        "loss_bearer": "الممول يتحمل مخاطر السلعة بعد استلامها مع اشتراط ضمانات التسليم",
        "category": "debt_trade"
    },
    "istisna": {
        "name": "الاستصناع",
        "legal_article": "المادة 75 من القانون 25-06",
        "nature": "عقد تصنيع أو إنشاء سلعة/أصل بمواصفات متفق عليها وسعر محدد",
        "return_source": "الفارق التعاقدي بين تكلفة الاستصناع وسعر البيع الآجل أو المنفذ",
        "loss_bearer": "حسب مراحل الإنجاز ودفعات الجداول التشغيلية",
        "category": "manufacturing"
    },
    "ijarah": {
        "name": "الإجارة المنتهية بالتمليك أو التشغيلية",
        "legal_article": "المادة 70 من القانون 25-06",
        "nature": "تمكين المستأجر من منفعة أصل موقوف أو استثماري نظير بدل إيجار معلوم",
        "return_source": "بدل الإيجار الدوري المنتظم",
        "loss_bearer": "المؤجر يتحمل هلاك العين الأساسية والمستأجر يتحمل الصيانة التشغيلية والتعدي",
        "category": "leasing"
    },
    "muzaraa": {
        "name": "المزارعة والمساقاة",
        "legal_article": "المادتان 71 و 72 من القانون 25-06",
        "nature": "تسليم أرض زراعية أو غراس قصد استغلالها مقابل حصة شائعة من المحصول",
        "return_source": "نسبة مئوية شائعة من ناتج المحصول الزراعي",
        "loss_bearer": "يتحمل كل طرف ما قدمه (الممول فقد جزء الغلة والعامل ضياع جهده) في الجوائح الطبيعية",
        "category": "agricultural"
    }
}

