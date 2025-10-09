# TMC Inventory

**TMC Inventory** — это веб-приложение для учёта и управления товарно-материальными ценностями (ТМЦ) в организации. Проект реализован на FastAPI (backend) и Vue 3 (frontend).

## Возможности

- Авторизация и регистрация пользователей (с ролями администратора)
- CRUD-операции для ТМЦ (создание, просмотр, редактирование, удаление)
- Учёт локаций и ответственных лиц
- Поиск и фильтрация по статусу, локации, ответственному
- Современный интерфейс на Vue 3
- Swagger-документация для API

## Структура проекта

```
tmc-inventory/
├── backend/
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── auth.py
│       ├── routers/
│       └── ...
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   └── api/
│   └── nginx.conf
└── README.md
```

## Быстрый старт

### Backend (FastAPI)

1. Перейдите в папку `backend/app`
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3. Запустите сервер:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
4. Swagger-документация будет доступна по адресу: [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend (Vue 3)

1. Перейдите в папку `frontend`
2. Установите зависимости:
    ```bash
    npm install
    ```
3. Запустите dev-сервер:
    ```bash
    npm run dev
    ```
4. Приложение будет доступно по адресу: [http://localhost:5173](http://localhost:5173)

### Проксирование API

- Для production используйте nginx с конфигом из `frontend/nginx.conf` для проксирования запросов `/api` на backend.

## Переменные окружения

- `JWT_SECRET` — секрет для генерации токенов
- `PEPPER` — дополнительная строка для хэширования паролей

## Лицензия

MIT

---

**Авторы:**  
VyavhesLove
2025
