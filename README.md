# Audio Upload Service

FastAPI-сервис для загрузки аудиофайлов с авторизацией через Яндекс.

## Запуск без Docker

1. Склонируйте проект:

```bash
git clone https://github.com/ekTeZy/FastAPI-Files.git
cd FastAPI-Files
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Скопируйте файл с переменными:

```bash
cp .env.example .env
```

И заполните его своими данными.

5. Примените Alembic миграции:

```bash
alembic upgrade head
```

6. Запустите FastAPI:

```bash
uvicorn main:app --reload
```

## Запуск с Docker (optional)

- Скопируйте `.env.example` в `.env`
- Заполните вручную

```bash
docker-compose up --build
```

## Нюансы

- `.env` не хранится в git, используйте `.env.example`
- После запуска перейдите на `/auth/yandex` для отладки OAuth
- После авторизации вы получите JWT для доступа к API

