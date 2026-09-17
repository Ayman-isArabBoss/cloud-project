# تشغيل المشروع من PyCharm

## المطلوب

- PyCharm
- Docker Desktop يعمل
- مجلد المشروع مفتوح في PyCharm

## فتح المشروع

1. فك ضغط `cloud-project.zip`.
2. افتح PyCharm واختر **Open**.
3. اختر مجلد `cloud-project` نفسه، وليس مجلد `api` فقط.
4. تأكد أن الملف `compose.yaml` ظاهر في شجرة الملفات.

## تشغيل المشروع

افتح Terminal من داخل PyCharm عبر **View → Tool Windows → Terminal**، ثم نفذ الأوامر التالية من جذر المشروع:

```powershell
docker compose config
docker compose up -d --build
docker compose ps
```

يجب أن تظهر الخدمات `nginx` و`api` و`database`.

## اختبار سريع

```powershell
Invoke-RestMethod http://localhost:8080/health
Invoke-RestMethod http://localhost:8080/api/tasks
```

النتيجة المتوقعة لفحص الصحة:

```json
{"status":"ok"}
```

## إنشاء مهمة

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8080/api/tasks `
  -ContentType "application/json" `
  -Body '{"title":"First task","description":"Test project","completed":false}'
```

## عرض سجلات الخدمات

```powershell
docker compose logs api
docker compose logs nginx
docker compose logs database
```

## إيقاف المشروع

```powershell
docker compose down
```

لا تستخدم `docker compose down -v` أثناء الاختبار العادي، لأنه يحذف Volume قاعدة البيانات وقد يحذف السجلات المحفوظة.

## ملاحظات

- PyCharm يحرر الكود، وDocker Desktop يشغّل الحاويات.
- لا تشغّل `main.py` مباشرة في البداية.
- لا تحتاج تثبيت PostgreSQL أو Nginx منفصلين.
- لا تغيّر اسم المضيف `database` إلى `localhost` داخل إعداد Docker.
- إذا ظهر خطأ، انسخ النص كاملًا من Terminal.
