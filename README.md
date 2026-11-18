# منصة تسيير الساعات الإضافية للأساتذة الجامعيين

منصة ويب متكاملة لإدارة الساعات الإضافية للأساتذة الجامعيين في الجزائر، تدعم العمليات الكاملة من تسجيل الأساتذة وإدارة العقود وتتبع الساعات الإضافية مع تقارير مفصلة.

## 🎯 الميزات الرئيسية

### إدارة الأساتذة
- ✅ تسجيل الأساتذة مع جميع البيانات المطلوبة (الهوية، الأكاديمية، الإدارية، المالية)
- ✅ دعم جميع الحقول المطلوبة: الاسم، اللقب، تاريخ الميلاد، الشهادة، الرتبة، الصفة، النشاط المارس
- ✅ إدارة السنوات الجامعية، الأسداس، المقاييس، أنواع التدريس (TD, TP, محاضرات)
- ✅ تتبع الساعات: المرخصة، الأسبوعية، عدد الأسابيع، الإجمالية، المسموح بها
- ✅ تواريخ العقود: البداية، نهاية الثلاثي، بداية س2، النهاية
- ✅ المعلومات الإدارية: القسم، الكلية، الحساب البريدي، العنوان، الهاتف، الوزارة، المؤسسة الأصلية
- ✅ المعرفات الرسمية: رقم الضمان الاجتماعي، رقم التعريف الوطني
- ✅ نظام فلترة وبحث متقدم

### إدارة العقود
- ✅ إنشاء وتعديل العقود مع ربطها بالأساتذة
- ✅ إدارة أنواع التدريس، الساعات، التواريخ
- ✅ نظام اعتماد للعقود (معلق/معتمد)
- ✅ تتبع حالة العقد (نشط/ملغي)

### الساعات الإضافية
- ✅ تسجيل الساعات الإضافية مرتبطة بالعقود
- ✅ نظام اعتماد للساعات (معلق/معتمد)
- ✅ تقارير تفصيلية بالساعات المنفذة

### التقارير والتصدير
- ✅ تصدير البيانات إلى Excel (أساتذة، عقود، ساعات)
- ✅ تقارير PDF فردية لكل أستاذ
- ✅ لوحة تحكم إحصائية تفاعلية

### الأمان والصلاحيات
- ✅ مصادقة JWT مع Access/Refresh tokens
- ✅ أدوار متعددة: مدير، رئيس مصلحة، رئيس قسم، أستاذ، موارد بشرية
- ✅ حماية المسارات حسب الصلاحيات

## 🛠️ التقنيات المستخدمة

### Backend
- **FastAPI** - إطار عمل Python حديث وسريع
- **PostgreSQL** - قاعدة بيانات علاقاتية قوية
- **SQLAlchemy 2.0** - ORM حديث مع دعم async
- **Alembic** - إدارة ترحيل قاعدة البيانات
- **Pydantic v2** - التحقق من البيانات والتسلسل
- **python-jose** - إدارة JWT
- **passlib** - تشفير كلمات المرور
- **pandas/openpyxl** - تصدير Excel
- **reportlab** - توليد PDF

### Frontend
- **React 18** مع TypeScript
- **Vite** - أداة بناء سريعة
- **Tailwind CSS** - إطار عمل CSS utility-first
- **React Router v6** - التوجيه
- **React Hook Form + Zod** - إدارة النماذج والتحقق
- **TanStack Table** - جداول متقدمة
- **Recharts** - الرسوم البيانية
- **Zustand** - إدارة الحالة
- **React Hot Toast** - الإشعارات
- **Lucide React** - الأيقونات

### البنية التحتية
- **Docker & Docker Compose** - الحاويات
- **Nginx** - خادم ويب/Reverse Proxy (للإنتاج)
- **GitHub Actions** - CI/CD

## 📋 المتطلبات

- Docker 20.10+
- Docker Compose 2.0+
- 4 GB RAM على الأقل
- 10 GB مساحة قرص

## 🚀 التشغيل السريع

### 1. استنساخ المشروع
```bash
git clone <repository-url>
cd overtime-platform
```

### 2. إعداد متغيرات البيئة
```bash
cp .env.example .env
# تحرير ملف .env وتعديل القيم الحساسة
```

### 3. التشغيل باستخدام Docker Compose
```bash
# بناء وتشغيل جميع الخدمات
docker-compose up -d --build

# متابعة السجلات
docker-compose logs -f

# إيقاف الخدمات
docker-compose down
```

### 4. الوصول للتطبيق
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432 (postgres/postgres)

### 5. تهيئة قاعدة البيانات
```bash
# تشغيل سكريبت التهيئة (ينشئ مستخدم admin وبيانات أولية)
docker-compose exec backend python init_db.py
```

**بيانات الدخول الافتراضية:**
- **البريد**: admin@univ.dz
- **كلمة المرور**: admin123

## 📁 هيكل المشروع

```
overtime-platform/
├── backend/
│   ├── app/
│   │   ├── api/           # مسارات API
│   │   ├── core/          # الإعدادات، الأمان، قاعدة البيانات
│   │   ├── models/        # نماذج SQLAlchemy
│   │   ├── schemas/       # مخططات Pydantic
│   │   ├── services/      # منطق العمل
│   │   ├── utils/         # أدوات مساعدة
│   │   └── tasks/         # مهام خلفية (Celery)
│   ├── alembic/           # ترحيلات قاعدة البيانات
│   ├── tests/             # اختبارات
│   ├── requirements.txt
│   ├── Dockerfile
│   └── init_db.py
├── frontend/
│   ├── src/
│   │   ├── components/    # مكونات قابلة لإعادة الاستخدام
│   │   ├── pages/         # صفحات التطبيق
│   │   ├── layouts/       # تخطيطات الصفحات
│   │   ├── hooks/         # خطافات مخصصة
│   │   ├── services/      # استدعاءات API
│   │   ├── store/         # إدارة الحالة (Zustand)
│   │   ├── types/         # أنواع TypeScript
│   │   └── utils/         # أدوات مساعدة
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 التطوير المحلي

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp ../.env.example .env
# تعديل .env
python init_db.py
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp ../.env.example .env.local
# تعديل VITE_API_URL إذا لزم الأمر
npm run dev
```

### تشغيل الاختبارات
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run lint
```

## 📊 API Endpoints الرئيسية

### المصادقة
```
POST   /api/v1/auth/login          # تسجيل الدخول
POST   /api/v1/auth/register       # تسجيل مستخدم جديد
POST   /api/v1/auth/refresh        # تجديد токен
```

### الأساتذة
```
GET    /api/v1/teachers            # قائمة الأساتذة (مع فلترة وترقيم)
POST   /api/v1/teachers            # إضافة أستاذ جديد
GET    /api/v1/teachers/{id}       # تفاصيل أستاذ
PUT    /api/v1/teachers/{id}       # تعديل أستاذ
DELETE /api/v1/teachers/{id}       # حذف أستاذ
GET    /api/v1/teachers/{id}/contracts   # عقود الأستاذ
GET    /api/v1/teachers/{id}/overtime    # ساعات إضافية الأستاذ
GET    /api/v1/teachers/export/excel     # تصدير Excel
GET    /api/v1/teachers/{id}/report/pdf  # تقرير PDF
```

### العقود
```
GET    /api/v1/contracts           # قائمة العقود
POST   /api/v1/contracts           # إنشاء عقد جديد
GET    /api/v1/contracts/{id}      # تفاصيل عقد
PUT    /api/v1/contracts/{id}      # تعديل عقد
POST   /api/v1/contracts/{id}/approve    # اعتماد عقد
GET    /api/v1/contracts/export/excel    # تصدير Excel
```

### الساعات الإضافية
```
GET    /api/v1/overtime            # قائمة السجلات
POST   /api/v1/overtime            # إضافة سجل جديد
GET    /api/v1/overtime/teacher/{id}     # سجلات أستاذ
GET    /api/v1/overtime/contract/{id}    # سجلات عقد
PUT    /api/v1/overtime/{id}       # تعديل سجل
POST   /api/v1/overtime/{id}/approve     # اعتماد سجل
```

### لوحة التحكم
```
GET    /api/v1/dashboard/stats     # إحصائيات شاملة
```

### الإعدادات الأكاديمية
```
GET    /api/v1/enums/ranks         # قائمة الرتب
GET    /api/v1/enums/qualities     # قائمة الصفات
GET    /api/v1/enums/wilayas       # قائمة الولايات
GET    /api/v1/enums/degrees       # قائمة الشهادات
GET    /api/v1/enums/teaching-types # أنواع التدريس
GET    /api/v1/enums/semesters     # الأسداس
GET    /api/v1/enums/academic-years # السنوات الجامعية
GET    /api/v1/enums/statuses      # الحالات
```

## 🔐 متغيرات البيئة الحرجة

| المتغير | الوصف | مطلوب |
|----------|---------|-------|
| `SECRET_KEY` | مفتاح توقيع JWT (32+ حرف) | ✅ |
| `DATABASE_URL` | رابط قاعدة البيانات PostgreSQL | ✅ |
| `BACKEND_CORS_ORIGINS` | أصول المسموحة لـ CORS | ✅ |
| `SMTP_*` | إعدادات البريد الإلكتروني | ❌ |
| `CIB_MERCHANT_ID` | معرف التاجر CIB (الجزائر) | ❌ |

## 📦 النشر للإنتاج

### 1. إعداد الخادم
```bash
# تثبيت Docker و Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

### 2. إعداد SSL (Let's Encrypt)
```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.dz
```

### 3. إعداد Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.dz;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.dz;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.dz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.dz/privkey.pem;
    
    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. متغيرات البيئة للإنتاج
```bash
# .env.production
DEBUG=false
SECRET_KEY=your-very-long-random-secret-key-here
DATABASE_URL=postgresql://user:strong-password@db:5432/overtime_db
BACKEND_CORS_ORIGINS=["https://yourdomain.dz"]
```

### 4. النشر
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## 🧪 الاختبار

```bash
# تشغيل جميع الاختبارات
docker-compose exec backend pytest -v

# اختبارات مع التغطية
docker-compose exec backend pytest --cov=app --cov-report=html

# اختبارات الواجهة الأمامية
docker-compose exec frontend npm run lint
```

## 📝 الترخيص

هذا المشروع مخصص للاستخدام المؤسسي في الجامعات الجزائرية. يتطلب مراجعة قانونية وشرعية قبل التشغيل الفعلي.

## 🤝 المساهمة

1. Fork المشروع
2. إنشاء فرع للميزة (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للفرع (`git push origin feature/amazing-feature`)
4. فتح Pull Request

## 📞 الدعم

للاستفسارات التقنية:
- **البريد الإلكتروني**: support@overtime.dz
- **التوثيق**: /docs
- **API Docs**: /docs (Swagger UI)

---

**ملاحظة هامة**: هذا النظام يتطلب مراجعة من هيئة شرعية ومستشار قانوني مختص في القانون الجزائري قبل اعتماده للاستخدام الرسمي، خصوصاً فيما يتعلق بقواعد الوقف، العقود، والتوزيع المالي.