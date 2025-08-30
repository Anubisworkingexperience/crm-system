# CRM система

CRM-система, состоящая из отдельных микросервисов, разделённых по зонам ответственности:
- API Gateway: REST-интерфейс, авторизация, маршрутизация запросов к микросервисам
- Customer Service: управление клиентами (CRUD)
- Order Service: создание заказов

Коммуникация между API Gateway и микросервисами через gRPC.

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

4. Настройте переменные окружения для api_gateway
```bash
touch .env
cp .env.example .env
# Введите свои данные
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>
JWT_SECRET=<your_secret_jwt_token>
```
jwt токен можно сгенерировать так:

```bash
openssl rand -hex 32
```

5. Сгенерируйте код клиентов из proto файлов
Proto файл - файл с расширением .proto в директории app/proto

Из api_gateway:
```bash
python3 -m grpc_tools.protoc -I./app/proto --python_out=./app/proto --grpc_python_out=./app/proto app/proto/customer.proto app/proto/order.proto
```
Из customer_service:
```bash
cd ../customer_service
python3 -m grpc_tools.protoc -I./app/proto --python_out=./app/proto --grpc_python_out=./app/proto app/proto/customer.proto
```
Из order_service:
```bash
cd ../order_service
python3 -m grpc_tools.protoc -I./app/proto --python_out=./app/proto --grpc_python_out=./app/proto app/proto/order.proto
```

6. Запустите backend сервер
```bash
cd ../api_gateway
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
7. Запустите frontend сервер
```bash
cd ../frontend
source venv/bin/activate
python3 -m http.server 5500
```

8. Настройте переменные окружения для Customer Service
```bash
cd ../customer_service
touch .env
cp .env.example .env
# Введите свои данные
DATABASE_URL=postgresql+psycopg2://<username>:<password>@<host>:<port>/<database_name>
```

9. Запустите Customer Service
```bash
source venv/bin/activate
python3 app/server.py
```

10. Запустите Order Service
```bash
cd ../order_service
source venv/bin/activate
python3 app/server.py
```
