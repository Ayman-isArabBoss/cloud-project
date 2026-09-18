# Task Manager REST API

مشروع تعليمي هندسي يطبق معمارية REST API لإدارة المهام وتحديثها من تطبيق أحادي إلى خدمات مصغرة معزولة باستخدام FastAPI وPostgreSQL وNginx وDocker Compose.

## 1. Project Description (وصف المشروع)
تطبيق متطور لإدارة المهام يعتمد على فصل المكونات البرمجية لتسهيل التوسع وتحسين الأداء، حيث تم تحويل النظام بالكامل إلى بيئة حاويات معزولة تضمن الأمان واستمرارية البيانات.

## 2. المعمارية (System Architecture Diagram)
```text
Client :8080 → Nginx (Reverse Proxy) → API (internal :8000) → PostgreSQL → named volume db-data
```
الخدمة الوحيدة التي تنشر منفذًا على الجهاز هي Nginx. لا يوجد منفذ مضيف مباشر للـ API أو قاعدة البيانات لضمان العزل الأمني الكامل.

## 3. التقنيات المستخدمة (Technologies Used)
- **Backend:** Python 3.12-slim / FastAPI
- **Database:** PostgreSQL 16-alpine
- **Reverse Proxy:** Nginx 1.27-alpine
- **Orchestration:** Docker Engine & Docker Compose v2
- **Version Control:** Git & GitHub

## 4. هيكل المجلدات (Repository Directory Structure)
```text
cloud-project/
├── .env.example
├── .gitignore
├── compose.yaml
├── README.md
├── api/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       └── main.py
└── nginx/
    └── nginx.conf
```

## 5. المتطلبات (Prerequisites)
- Docker Desktop مع Docker Compose v2 مفعّل.
- محرر الأكواد PyCharm (Community أو Professional).
- أداة curl أو Postman للاختبار.

## 6. أمر التشغيل بخطوة واحدة (One-Step Deployment Command)
من جذر المشروع، شغّل الأمر التالي لبناء وتشغيل النظام بالكامل في الخلفية:
```bash
docker compose up -d --build
```

## 7. المسارات وتوثيق الـ API (REST API Endpoints)
افتح الـ API عبر الرابط الموحد للبوابة: `http://localhost:8080`.

| Method | Path | الوصف |
|---|---|---|
| GET | `/health` | فحص جاهزية الخدمة داخلياً |
| GET | `/api/tasks` | عرض كافة المهام من قاعدة البيانات |
| GET | `/api/tasks/{id}` | عرض تفاصيل مهمة محددة |
| POST | `/api/tasks` | إنشاء مهمة جديدة (JSON Payload) |
| PUT | `/api/tasks/{id}` | تعديل بيانات مهمة موجودة |
| DELETE | `/api/tasks/{id}` | حذف مهمة نهائياً من النظام |

مثال لإنشاء مهمة عبر الـ CLI:
```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Docker","description":"Finish the course project","completed":false}'
```

## 8. التحقق من العزل والاستمرارية (Isolation & Persistence Evidence)
للتحقق من حجب منافذ الـ API داخلياً:
```bash
docker compose ps
docker compose port api 8000
```
*(يجب ألا يعرض الأمر الأخير أي منفذ منشور للمستضيف الخارجي)*

لإثبات حفظ واستمرارية البيانات بعد إعادة التشغيل:
```bash
# أنشئ سجلًا أولًا باستخدام طلب POST ثم نفذ:
docker compose down
docker compose up -d
curl http://localhost:8080/api/tasks
```
تبقى البيانات محفوظة داخل الـ `db-data` لأن `docker compose down` يحافظ على الـ Named Volumes، بينما الأمر المخرب `docker compose down -v` يقوم بحذفها وتدمير السجلات.

## 9. معلومات السجل الرقمي (OCI-Compliant Registry Information)
الصور البرمجية الخاصة بالمشروع مرفوعة ومتاحة للعموم على السجل الرقمي:
- **رابط المستودع:** `aymanamin5000/task-manager-api`
- **أمر السحب المباشر:** `docker pull aymanamin5000/task-manager-api:v1.0.0`

## 10. أعضاء الفريق والمساهمات (Team Members & Contributions)
- **أيمن أمين الخليدي (Ayman-isArabBoss):** قام ببناء كود الـ API، كتابة ملف الـ Dockerfile بممارسات الأمان، إعداد الـ Reverse Proxy والـ Compose، وإتمام الرفع والتكامل على GitHub وDocker Hub.

## 11. الإصدار الحالي (Current Version)
- **Version Tag:** `v1.0.0`
- **Latest Build:** `latest`

## 12. الأمان وضوابط الحماية
- الـ API يعمل داخل شبكة Docker معزولة تماماً بدون host port.
- الصورة مبنية من نسخة خفيفة `python:3.12-slim` لحظر الثغرات.
- الحاوية تعمل بمستخدم آمن وغير جذر `appuser`.
- ملف إعدادات Nginx مركب بصلاحية القراءة فقط `read_only: true`.
