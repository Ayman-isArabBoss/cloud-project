# Testing Commands

```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/tasks

curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"First task","description":"Test persistence","completed":false}'

curl http://localhost:8080/api/tasks/1

curl -X PUT http://localhost:8080/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated task","description":"Updated description","completed":true}'

curl -i -X DELETE http://localhost:8080/api/tasks/1
curl -i http://localhost:8080/api/tasks/99999
curl -i -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"description":"Missing title"}'
```

Persistence test:

```bash
docker compose down
docker compose up -d
curl http://localhost:8080/api/tasks
```
