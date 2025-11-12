## Shop Project

Учебный интернет-магазин на Django. В этом репозитории на каждом уроке добавляются новые фичи.

### Запуск локально

1. Python 3.11+
2. Создать окружение и установить зависимости:

```bash
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Миграции и запуск:

```bash
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Домашняя страница: `/` или `/home/`

Страница контактов: `/contacts/`

### GitFlow

- Основные ветки: `main`, `develop`
- Домашние задания — отдельные ветки от `develop` с PR в `develop`
- В репозитории настроен `.gitignore`


