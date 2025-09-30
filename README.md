# Cashflow – управление движением денежных средств (ДДС)

Веб-приложение для учёта и анализа движения денежных средств.
Позволяет добавлять, редактировать и удалять записи, управлять справочниками (типы, категории, подкатегории, статусы), 
фильтровать данные и просматривать их в удобной форме.

### Технологии
- Python 3.11+
- Django
- SQLite
- Bootstrap

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Alex-XO/cashflow.git
cd cashflow
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# или .venv\Scripts\activate  # Windows PowerShell
```

### 3. Установить зависимости

```bash
pip install -r requirements.lock
```

### 4. Настроить переменные окружения

Скопируйте пример конфига и подставьте свои значения (SECRET_KEY)

```bash
cp .env.sample .env
```

### 5. Применить миграции и загрузить фикстуры

```bash
python manage.py migrate
python manage.py loaddata catalog/fixtures/initial_catalog.json
```

### Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите логин, e-mail и пароль 

### 6. Запустить сервер разработки

```bash
python manage.py runserver
```

После этого приложение будет доступно по адресу: http://127.0.0.1:8000/

## Тесты

Запуск всех тестов:

```bash
python manage.py test
```