# CRM система

CRM-система, состоящая из отдельных микросервисов, разделённых по зонам ответственности:
- API Gateway: REST-интерфейс, авторизация, маршрутизация запросов к микросервисам
- Customer Service: управление клиентами (CRUD)
- Order Service: создание заказов

# Запуск сервисов

1. Настройте postgreSQL локально
```bash
git clone https://github.com/Anubisworkingexperience/crm-system.git
cd crm-system/api_gateway
psql -U postgres
```

```sql
CREATE DATABASE crm_db;
CREATE USER crm_user WITH PASSWORD 'crm_password';
GRANT ALL PRIVILEGES ON DATABASE crm_db TO crm_user;
\q
```

2. Создайте и активируйте venv
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости
```bash
pip install -r requirements.txt
```

4. Создайте .env файл
```bash
touch .env
cp .env.example .env
```

5. Настройте переменные окружения
```bash
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>
JWT_SECRET=<your_secret_jwt_token>
```
jwt токен можно сгенерировать так:

```bash
openssl rand -hex 32
```

6. Запустите backend сервер
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
7. Запустите frontend сервер
```bash
cd ../frontend
python -m http.server 5500
```
