# Task Manager REST API

مشروع تعليمي يطبق REST API لإدارة المهام باستخدام FastAPI وPostgreSQL وNginx وDocker Compose.

## المعمارية

```text
Client :8080 → Nginx → API (internal :8000) → PostgreSQL → named volume db-data
```

الخدمة الوحيدة التي تنشر منفذًا على الجهاز هي Nginx. لا يوجد منفذ مضيف مباشر للـ API أو قاعدة البيانات.

## المتطلبات

- Docker Desktop مع Docker Compose v2
- PyCharm Community أو Professional
- curl أو Postman للاختبار (اختياري)

## فتح المشروع في PyCharm

1. فك ضغط المشروع.
2. افتح PyCharm واختر **Open**.
3. اختر مجلد المشروع الذي يحتوي مباشرة على الملف `compose.yaml`.
4. افتح **View → Tool Windows → Terminal**.
5. شغّل Docker Desktop قبل تنفيذ أوامر Docker.

PyCharm يستخدم لفتح وتعديل ملفات Python، بينما Docker Desktop يشغّل خدمات API وPostgreSQL وNginx. لا تشغّل `api/app/main.py` مباشرة في البداية؛ شغّل النظام من Terminal باستخدام Docker Compose.

## إعداد Python في PyCharm (اختياري)

يمكنك تثبيت Python 3.12 Interpreter في PyCharm لميزات المحرر مثل الإكمال التلقائي، لكن تشغيل المشروع الأساسي لا يحتاج تثبيت PostgreSQL أو Nginx على الجهاز؛ كلاهما يعمل داخل Docker.

إذا طلب PyCharm تثبيت المكتبات للتعرف على الكود، استخدم `api/requirements.txt`. لا تغيّر `DATABASE_URL` إلى `localhost` عند تشغيل Docker؛ داخل Compose اسم قاعدة البيانات هو `database`.

## التشغيل

من جذر المشروع:

```bash
docker compose config
docker compose up -d --build
docker compose ps
```

افتح API عبر `http://localhost:8080`.

## المسارات

| Method | Path | الوصف |
|---|---|---|
| GET | `/health` | فحص الخدمة |
| GET | `/api/tasks` | عرض المهام |
| GET | `/api/tasks/{id}` | عرض مهمة |
| POST | `/api/tasks` | إنشاء مهمة |
| PUT | `/api/tasks/{id}` | تعديل مهمة |
| DELETE | `/api/tasks/{id}` | حذف مهمة |

مثال إنشاء مهمة:

```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Docker","description":"Finish the course project","completed":false}'
```

## التحقق من العزل والاستمرارية

```bash
docker compose ps
docker compose port api 8000
```

يجب ألا يعرض الأمر منفذًا منشورًا للـ API.

لإثبات حفظ البيانات:

```bash
# أنشئ سجلًا أولًا ثم نفذ:
docker compose down
docker compose up -d
curl http://localhost:8080/api/tasks
```

يبقى `db-data` لأن `docker compose down` لا يحذف named volumes. أما `docker compose down -v` فيحذف volume وقد يمسح البيانات.

## إيقاف المشروع

```bash
docker compose logs
docker compose down
```

## الأمان

- API يعمل داخل شبكة Docker ولا يملك host port.
- صورة API مبنية من `python:3.12-slim`.
- التطبيق يعمل بالمستخدم غير root `appuser`.
- إعداد Nginx مركب بصلاحية قراءة فقط.
- الإصدارات مثبتة في `requirements.txt`.
