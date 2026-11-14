# Полное методическое руководство по проекту «Design.pro» на Django (TUTORIAL 4)
# Комплексный курс по практическим работам: ПР №2.1, ПР №2.2, ПР №2.3

> **Назначение документа:**  
> Данное руководство представляет собой полную версию фундаментального учебного пособия **TUTORIAL 2**, полностью реорганизованную **по автономным секциям практических работ (ПР №2.1, ПР №2.2, ПР №2.3)** в точном соответствии с регламентом учебной практики и демонстрационного экзамена.  
> В документ включены **100% материалов из TUTORIAL 2 без сокращений**: полный теоретический разбор паттерна MVT, жизненный цикл HTTP-запроса, построчный анализ `settings.py`, пошаговые команды инициализации, полный код всех 8 модулей бэкенда, полный сплошной код всех 9 шаблонов HTML/DTL и стилей CSS, а также **все 25 вопросов и эталонных ответов для защиты**.  
> Дополнительно каждая секция практической работы снабжена **готовым шаблоном официального отчета** и **профильной подборкой экзаменационных вопросов**.

---

## 🧭 Навигация по секциям руководства:

| Секция | Тема модуля | Содержание и ключевые задачи |
| :--- | :--- | :--- |
| [**Секция 0**](#секция-0-общесистемный-фундамент-архитектура-и-первоначальная-настройка-проекта) | **Общесистемный фундамент** | MVT vs MVC, HTTP-цикл, анализ ТЗ, окружение Python 3.12, детальный разбор и код `settings.py`, медиа-хранилище, базовый каркас `base.html` и стили |
| [**Секция 1**](#секция-1-практическая-работа-21-реализация-функционала-гостя) | **ПР №2.1. Функционал гостя** | 1. Главная страница (счетчик + 4 работы)<br>2. Регистрация (валидация ФИО, логина, ПДн, подсветка ошибок `is-invalid`)<br>3. Вход в систему (ролевой редирект)<br>📄 *Готовый отчет по ПР 2.1*<br>🎓 *Вопросы и ответы для защиты ПР 2.1* |
| [**Секция 2**](#секция-2-практическая-работа-22-реализация-функционала-зарегистрированного-пользователя) | **ПР №2.2. Функционал пользователя** | 1. Выход из системы (Logout)<br>2. Создание заявки (валидация плана до 2 Мб)<br>3. Просмотр своих заявок (фильтры)<br>4. Безопасное удаление своей новой заявки<br>📄 *Готовый отчет по ПР 2.2*<br>🎓 *Вопросы и ответы для защиты ПР 2.2* |
| [**Секция 3**](#секция-3-практическая-работа-23-реализация-функционала-администратора) | **ПР №2.3. Функционал администратора** | 1. Разграничение прав (`@user_passes_test(is_admin)`)<br>2. Смена статуса «В работу» (с комментарием)<br>3. Смена статуса «Выполнено» (с файлом дизайна до 5 Мб)<br>4. Управление категориями и каскадное удаление заявок (`CASCADE`)<br>📄 *Готовый отчет по ПР 2.3*<br>🎓 *Вопросы и ответы для защиты ПР 2.3* |
| [**Секция 4**](#секция-4-автоматизированное-тестирование-запуск-проекта-и-полный-сводный-топ-25-вопросов) | **Сквозная аттестация и экзамен** | Полный код и разбор 6 тестов (`tests.py`), инструкция по запуску на порту 8089, таблица демо-аккаунтов, **Полный сводный ТОП-25 вопросов для экзамена**, чек-лист сдачи |

---

## 📂 Быстрые ссылки на исходные файлы проекта:
- ⚙️ Конфигурация ядра: [design_studio/settings.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/design_studio/settings.py)
- 🗄 Модели БД: [catalog/models.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/models.py)
- 📝 Формы и серверная валидация: [catalog/forms.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/forms.py)
- 🧠 Представления (Views): [catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/views.py)
- 🧭 Маршрутизация приложения: [catalog/urls.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/urls.py)
- 🌐 Главные маршруты проекта: [design_studio/urls.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/design_studio/urls.py)
- 🛡 Админка Django: [catalog/admin.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/admin.py)
- 🧪 Модульные тесты: [catalog/tests.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/tests.py)

---
# Секция 0. Общесистемный фундамент, архитектура и первоначальная настройка проекта

## 1. Теоретический фундамент: Архитектура Django и паттерн MVT

Веб-фреймворк Django реализует архитектурный паттерн **MVT (Model-View-Template)**, являющийся модификацией классического **MVC (Model-View-Controller)**:

```
 Пользователь (Браузер)
      │ ▲
      │ │ 6. Итоговый HTTP-ответ (HTML + CSS)
      ▼ │
┌────────────────────────────────────────────────────────┐
│                        DJANGO                          │
│                                                        │
│  1. WSGI / ASGI Handler                                │
│     Точка входа, преобразует сетевой поток в объект    │
│     запроса HttpRequest                                │
│            │                                           │
│            ▼                                           │
│  2. MIDDLEWARE (Слой промежуточной обработки)          │
│     Сессии, безопасность, аутентификация, CSRF-защита  │
│            │                                           │
│            ▼                                           │
│  3. URLconf (urls.py)                                  │
│     Диспетчер маршрутов: сопоставляет URL с View       │
│            │                                           │
│            ▼                                           │
│  4. View (views.py) ── [Контроллер бизнес-логики]      │
│            │                             ▲             │
│            │ Запрос данных               │ Данные      │
│            ▼                             │             │
│     Model (models.py) ◄──────────────────┘             │
│     Django ORM (Object-Relational Mapping) ── SQLite   │
│            │                                           │
│            │ Передача контекста                        │
│            ▼                                           │
│  5. Template Engine (templates/*.html)                 │
│     Рендеринг HTML с подстановкой переменных (DTL)     │
└────────────────────────────────────────────────────────┘
```

### Сравнение терминологии Django и MVC:
| Компонент в Django | Аналог в классическом MVC | Роль и назначение в проекте |
| :--- | :--- | :--- |
| **Model** (`models.py`) | **Model** | Схема данных, таблицы БД, валидаторы на уровне сущностей, ORM-запросы. |
| **View** (`views.py`) | **Controller** | Принимает запрос, проверяет права доступа, обрабатывает формы, обращается к моделям, решает, какой ответ вернуть. |
| **Template** (`templates/`) | **View** | Пользовательский интерфейс: чистый HTML с вкраплениями языка тегов DTL. |

### Полный жизненный цикл HTTP-запроса:
1. Пользователь в браузере вводит `http://localhost:8089/cabinet/` и нажимает Enter.
2. Веб-сервер получает TCP-пакет и передает его в WSGI-обработчик Django (`wsgi.py`).
3. Запрос проходит сквозь цепочку **Middleware** (промежуточных слоев):
   - `SessionMiddleware`: считывает cookie сессии и прикрепляет к запросу хранилище данных `request.session`.
   - `AuthenticationMiddleware`: по ID из сессии находит пользователя в базе данных и сохраняет его в `request.user`.
   - `CsrfViewMiddleware`: проверяет наличие и валидность токена безопасности при POST-запросах.
4. **URLconf** (`design_studio/urls.py` ➔ `catalog/urls.py`) по регулярному выражению находит совпадение с маршрутом `cabinet/` и вызывает функцию `cabinet_view(request)`.
5. Декоратор `@login_required` проверяет `request.user.is_authenticated`. Если пользователь гость — возвращает редирект на `/login/`.
6. Функция `cabinet_view` запрашивает данные через Django ORM:
   ```python
   user_apps = Application.objects.filter(user=request.user).order_by('-created_at')
   ```
7. ORM транслирует Python-код в SQL-запрос `SELECT * FROM catalog_application WHERE user_id = ... ORDER BY created_at DESC;`.
8. Функция вызывает `render(request, 'catalog/cabinet.html', context)`.
9. Движок DTL объединяет HTML-шаблон с контекстом (списком заявок) и собирает финальный HTML-документ.
10. WSGI-сервер возвращает браузеру ответ со статусом `200 OK` и заголовком `Content-Type: text/html`.

---

---

## 2. Анализ Технического Задания и системное проектирование

### Предметная область:
Дизайн-студия **«Design.pro»** занимается проектированием и оформлением интерьеров жилых помещений. Заказчики загружают планы и фото помещений, а сотрудники дизайн-студии берут их в работу и прикрепляют готовые дизайн-проекты.

### Ролевая модель:
```
           ┌──────────────┐
           │     ГОСТЬ    │
           └──────┬───────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│ Вход на сайт │    │ Регистрация  │
└──────┬───────┘    └──────┬───────┘
       │                   │
       └─────────┬─────────┘
                 ▼
    ┌──────────────────────────┐
    │ АВТОРИЗОВАННЫЙ КЛИЕНТ    │
    ├──────────────────────────┤
    │ • Просмотр своих заявок  │
    │ • Фильтрация по статусам │
    │ • Создание новой заявки  │
    │ • Удаление заявки (Новая)│
    │ • Выход из аккаунта      │
    └────────────┬─────────────┘
                 │
                 ▼ (при наличии флага is_staff / is_superuser)
    ┌──────────────────────────┐
    │      АДМИНИСТРАТОР       │
    ├──────────────────────────┤
    │ • Панель /admin-panel/   │
    │ • Админка /superadmin    │
    │ • Смена статуса заявки   │
    │ • Управление категориями │
    └──────────────────────────┘
```

### Конечный автомат (State Machine) заявки:
Каждая заявка может находиться строго в одном из 3 статусов:
```
                   ┌─────────────────┐
                   │  [1] «Новая»    │ (создается клиентом автоматически)
                   └────────┬────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
(действие админа с комментарием)    (действие админа с файлом дизайна)
            │                               │
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│ [2] «Принято в работу»│       │   [3] «Выполнено»     │
└───────────────────────┘       └───────────────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
              [СМЕНА СТАТУСА ЗАБЛОКИРОВАНА]
            (удаление клиенту также запрещено)
```

---

---

## 3. Шаг 1. Подготовка окружения и запуск проекта с нуля

Проект расположен в третьей папке: `C:\Users\fer\PycharmProjects\YP_Django_3`.

```powershell
# 1. Создание папки и переход в нее
mkdir C:\Users\fer\PycharmProjects\YP_Django_3
cd C:\Users\fer\PycharmProjects\YP_Django_3

# 2. Создание виртуального окружения Python 3.12
python -m venv .venv

# 3. Активация окружения в PowerShell
.\.venv\Scripts\Activate.ps1

# 4. Установка Django и Pillow (для работы с картинками)
python -m pip install --upgrade pip
pip install django pillow

# 5. Инициализация проекта и приложения
django-admin startproject design_studio C:\Users\fer\PycharmProjects\YP_Django_3\design_studio
cd design_studio
python manage.py startapp catalog
```

---

---

## 4. Шаг 2. Конфигурация ядра (`settings.py`) — детальный разбор

Файл: [design_studio/settings.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/design_studio/settings.py).

### Разбор настроек:

```python
from pathlib import Path

# BASE_DIR — абсолютный путь к папке проекта (C:\Users\fer\PycharmProjects\YP_Django_3\design_studio)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY — криптографическая соль для подписания cookies, сессий и CSRF-токенов
SECRET_KEY = 'django-insecure-design-pro-study-key-2026'

# DEBUG = True включает подробную отладочную страницу при ошибках (только для разработки!)
DEBUG = True

# ALLOWED_HOSTS = ['*'] разрешает подключаться по localhost, 127.0.0.1 и любому IP
ALLOWED_HOSTS = ['*']

# Регистрация стандартных подсистем и нашего приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog.apps.CatalogConfig',  # Подключаем наше приложение студии
]

# Указываем Django использовать нашу расширенную модель пользователя вместо стандартной
AUTH_USER_MODEL = 'catalog.User'

# Промежуточное ПО (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Управление сессиями
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',             # Защита от CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Прикрепление user к request
    'django.contrib.messages.middleware.MessageMiddleware', # Всплывающие уведомления
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'design_studio.urls'

# Конфигурация шаблонизатора DTL
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Указываем глобальную папку templates в корне проекта
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True, # Искать шаблоны и внутри каталогов приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Переменная {{ request }}
                'django.contrib.auth.context_processors.auth', # Переменная {{ user }}
                'django.contrib.messages.context_processors.messages', # Переменная {{ messages }}
                'django.template.context_processors.media',   # Переменная {{ MEDIA_URL }}
            ],
        },
    },
]

# База данных: используем встраиваемую реляционную СУБД SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Язык интерфейса и часовой пояс
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Статика разработчика (CSS, JS)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Медиафайлы пользователей (загружаемые фото планов и готовых дизайнов)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Маршруты для перенаправлений аутентификации
LOGIN_URL = 'login'              # Куда перенаправлять неавторизованного
LOGIN_REDIRECT_URL = 'cabinet'   # Куда направить после успешного входа
LOGOUT_REDIRECT_URL = 'index'    # Куда направить после выхода
```

---

---

### Полный сплошной код файла конфигурации `design_studio/settings.py`:
Файл: [design_studio/settings.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/design_studio/settings.py)

### 1. `design_studio/settings.py` (Полный код):
```python
"""
Django settings for design_studio project.
Design Studio «Design.pro»
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-design-pro-secret-key-study-portal-2026'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog.apps.CatalogConfig',
]

AUTH_USER_MODEL = 'catalog.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'design_studio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'design_studio.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 3,
        }
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (Uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'cabinet'
LOGOUT_REDIRECT_URL = 'index'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

```

---

## 5. Шаг 3. Архитектура хранилища `media`: почему `photos/` и `designs/`

```
media/
├── photos/    <-- Планы помещений и фото комнат от клиентов (до 2 Мб)
└── designs/   <-- Готовые дизайн-проекты и визуализации от администратора
```

### Глубокое обоснование для руководителя/преподавателя:
1. **Принцип единственной ответственности (Separation of Concerns):**  
   Файлы заказчиков (технические планы, чертежи БТИ, фото без отделки) и файлы студии (3D-визуализации, эскизы) — это концептуально разные данные. Смешивать их в одной общей папке — грубая архитектурная ошибка.
2. **Почему не использована разбивка по датам (`upload_to='photos/%Y/%m/'`):**  
   В операционных системах Linux на каждую папку выделяется структура индексных дескрипторов (`inodes`). Когда в одной папке накапливается свыше 50 000 файлов, поиск файла файловой системой замедляется. Поэтому высоконагруженные порталы (Авито, Ozon) дробят файлы по годам и месяцам.  
   В студенческом проекте или демонстрационном экзамене важнее всего **наглядность и простота проверки**. Структура `photos/` и `designs/` исключает блуждание по пустым папкам с годами и днями: преподаватель сразу видит входящие файлы в `photos/` и результаты в `designs/`.

---

---

## 7. Шаг 5. Миграции и создание учетных записей

### Что делают команды миграций:
```powershell
# 1. Анализирует models.py и создает файл миграции
python manage.py makemigrations

# 2. Читает файлы миграций и выполняет SQL-запросы в db.sqlite3
python manage.py migrate
```

### Создание учетных записей по ТЗ:
В базе данных `db.sqlite3` уже созданы учетные записи:
- **Администратор:** логин `admin`, пароль `admin` (установлены флаги `is_staff = True`, `is_superuser = True`).
- **Клиент (демо):** логин `ivanov`, пароль `ivanov123`.

---

---

### Корневая маршрутизация проекта (`design_studio/urls.py`)
Файл: [design_studio/urls.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/design_studio/urls.py)

### 6. `design_studio/urls.py` (Полный код):
```python
"""
URL configuration for design_studio project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

# Настройка заголовков стандартной панели Django
admin.site.site_header = 'Design.pro — Панель управления'
admin.site.site_title = 'Design.pro Администратор'
admin.site.index_title = 'Управление базой данных Design.pro'

urlpatterns = [
    # По ТЗ: Административная панель должна быть доступна по адресу: http://localhost:8089/superadmin
    path('superadmin/', admin.site.urls),
    path('admin/', RedirectView.as_view(url='/superadmin/', permanent=False)),

    # Основное приложение каталога студии
    path('', include('catalog.urls')),
]

# Обслуживание медиа-файлов и статики в режиме разработки (DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')

```

---

### Архитектурный фундамент шаблонизатора Django (DTL)
### 10.1. Архитектурный фундамент: как Django находит и рендерит шаблоны

В файле [settings.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/design_studio/settings.py) шаблонизатор настроен следующим образом:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Приоритетный поиск в корневой папке templates
        'APP_DIRS': True,                  # Вторичный поиск внутри каждого приложения
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]
```

#### Роль Context Processors (Контекстных процессоров):
Контекстный процессор — это Python-функция, которая автоматически добавляет определенные глобальные переменные в словарь контекста каждого шаблона. Благодаря им разработчику не нужно вручную прописывать эти переменные в каждом вызове `render()`:
1. `django.contrib.auth.context_processors.auth`: автоматически внедряет переменную `{{ user }}`. Позволяет в любом месте любого шаблона проверять `{% if user.is_authenticated %}` или `{% if user.is_staff %}`.
2. `django.contrib.messages.context_processors.messages`: автоматически внедряет переменную `{{ messages }}` для вывода всплывающих flash-уведомлений об успешных операциях или ошибках.
3. `django.template.context_processors.request`: внедряет объект текущего запроса `{{ request }}`. Используется для проверки активной страницы: `{% if request.resolver_match.url_name == 'index' %}`.
4. `django.template.context_processors.media`: внедряет переменную `{{ MEDIA_URL }}` (`/media/`) для корректной генерации путей к загруженным изображениям.

---

### 10.2. Паттерн наследования шаблонов (Template Inheritance)

Django использует двухуровневое наследование шаблонов. Вместо копирования тегов `<html>`, `<head>`, навигационной панели и подвала на каждой странице, создается единый скелет — [base.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/base.html).

```
               ┌─────────────────────────────────────────┐
               │              base.html                  │
               │  • DOCTYPE, <head>, Bootstrap 5 CSS     │
               │  • Общая навигационная панель (navbar)   │
               │  • Блок flash-сообщений (messages)      │
               │                                         │
               │  ┌───────────────────────────────────┐  │
               │  │   {% block content %}{% endblock %}│  │  <-- «Посадочное место» для дочерних страниц
               │  └───────────────────────────────────┘  │
               │                                         │
               │  • Общий подвал (footer)                │
               │  • Bootstrap 5 JS Bundle                │
               └────────────────────┬────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│  index.html  │             │ cabinet.html │             │admin_panel...│
│{% extends    │             │{% extends    │             │{% extends    │
│  'base.html' │             │  'base.html' │             │  'base.html' │
│      %}      │             │      %}      │             │      %}      │
└──────────────┘             └──────────────┘             └──────────────┘
```

#### Ключевые теги DTL при наследовании:
- `{% extends 'base.html' %}` — **Обязательно первая строка** дочернего шаблона. Указывает движку DTL, что данный шаблон расширяет базовый макет.
- `{% block content %} ... {% endblock %}` — объявляет переопределяемую область. Дочерний шаблон наполняет этот блок своим уникальным HTML-кодом, а весь остальной каркас берется из `base.html`.
- `{% block title %} ... {% endblock %}` — позволяет каждой странице динамически задавать свой уникальный заголовок во вкладке браузера (`<title>`).

---

### 10.3. Защита от атак и безопасность в шаблонах

В каждом шаблоне проекта соблюдены строгие правила безопасности:
1. **Защита от CSRF (Cross-Site Request Forgery):**  
   Внутри каждой формы `<form method="post">` первой строкой идет тег `{% csrf_token %}`. Он генерирует скрытое поле `<input type="hidden" name="csrfmiddlewaretoken" value="...">`. При отправке формы middleware сверяет токен с cookie пользователя. Если токен отсутствует или подделан, Django вернет `403 Forbidden`.
2. **Автоматическое экранирование (Auto-escaping):**  
   Все переменные, выводимые через двойные фигурные скобки `{{ variable }}`, автоматически экранируются движком DTL. Если злоумышленник попытается ввести в поле названия заявки `<script>alert('XSS')</script>`, Django превратит символы в безопасные HTML-сущности `&lt;script&gt;`, полностью предотвращая XSS-атаки.
3. **Безопасная генерация URL (`{% url 'name' %}`):**  
   Ни в одном шаблоне нет захардкоженных путей вида `<a href="/cabinet/">`. Всегда используется тег `{% url 'cabinet' %}`. Это гарантирует, что если маршрут в `urls.py` изменится, ссылки во всем проекте обновятся автоматически.

---

---

### Базовый каркас пользовательского интерфейса
#### 1. [templates/base.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/base.html) — Базовый скелет и навигация
- **Светлая легкая тема:** Навбар `navbar-light bg-white border-bottom` обеспечивает легкий современный вид без тяжелых темных заливок.
- **Условный рендеринг пунктов меню:**
  - Гость видит: «Главная», кнопки «Вход» и «Регистрация».
  - Клиент видит: «Мои заявки», «+ Создать заявку», имя пользователя и кнопку «Выход».
  - Администратор видит: пункт «Панель управления» и прямую ссылку «Superadmin» на `/superadmin`.
- **Вывод Flash-сообщений (`messages`):**  
  Цикл `{% for message in messages %}` выводит уведомления фреймворка `django.contrib.messages` с соответствующими классами Bootstrap (`alert-success`, `alert-danger`, `alert-info`).
- **Липкий футер (Sticky Footer):**  
  Контейнер `body` имеет классы `d-flex flex-column min-vh-100`, а `main` — класс `flex-grow-1`. Благодаря этому футер всегда прижат к низу экрана, даже если на странице мало содержимого.

#### Полный код `templates/base.html` (Базовый каркас):
Файл: [templates/base.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/base.html)

### 1. `templates/base.html` (Базовый каркас):
```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Design.pro — Студия дизайна интерьеров{% endblock %}</title>
    <!-- Bootstrap 5 CSS (чистый, легкий интерфейс) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body class="d-flex flex-column min-vh-100 bg-white text-dark">

    <!-- Легкое, понятное меню навигации -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top py-2">
        <div class="container">
            <a class="navbar-brand fw-bold fs-4 text-dark d-flex align-items-center gap-1" href="{% url 'index' %}">
                <i class="bi bi-house-door text-primary"></i> Design<span class="text-primary">.pro</span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navMenu">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link {% if request.resolver_match.url_name == 'index' %}active fw-semibold text-primary{% endif %}" href="{% url 'index' %}">Главная</a>
                    </li>
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link {% if request.resolver_match.url_name == 'cabinet' %}active fw-semibold text-primary{% endif %}" href="{% url 'cabinet' %}">Мои заявки</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if request.resolver_match.url_name == 'application-create' %}active fw-semibold text-primary{% endif %}" href="{% url 'application-create' %}">+ Создать заявку</a>
                        </li>
                        {% if user.is_staff or user.is_superuser %}
                            <li class="nav-item">
                                <a class="nav-link text-warning-emphasis {% if request.resolver_match.url_name == 'admin_panel' %}active fw-semibold{% endif %}" href="{% url 'admin_panel' %}">Панель управления</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link text-secondary" href="/superadmin/" target="_blank">Superadmin</a>
                            </li>
                        {% endif %}
                    {% endif %}
                </ul>

                <div class="d-flex align-items-center gap-2">
                    {% if user.is_authenticated %}
                        <span class="navbar-text me-2 small text-muted">
                            <i class="bi bi-person"></i> {{ user.username }}{% if user.fio %} ({{ user.fio }}){% endif %}
                        </span>
                        <a href="{% url 'logout' %}" class="btn btn-outline-danger btn-sm">Выход</a>
                    {% else %}
                        <a href="{% url 'login' %}" class="btn btn-outline-primary btn-sm px-3">Вход</a>
                        <a href="{% url 'register' %}" class="btn btn-primary btn-sm px-3">Регистрация</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>

    <!-- Сообщения (успех, ошибка, предупреждение) -->
    <div class="container mt-3">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{% if message.tags == 'error' %}danger{% else %}{{ message.tags }}{% endif %} alert-dismissible fade show py-2 small" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close py-2" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
    </div>

    <!-- Основной контент -->
    <main class="flex-grow-1 py-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Простой подвал -->
    <footer class="border-top py-3 mt-auto bg-light text-muted small">
        <div class="container d-flex flex-wrap justify-content-between align-items-center">
            <span>© 2026 Студия дизайна интерьеров <strong>Design.pro</strong></span>
            <span>Порт: <strong>8089</strong> | Админка: <a href="/superadmin" class="text-decoration-none">/superadmin</a></span>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

```

#### Полный код `static/css/style.css` (Минималистичные стили):
Файл: [static/css/style.css](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/static/css/style.css)

### 9. `static/css/style.css` (Минималистичные стили):
```css
/* Минималистичные стили для легковесного интерфейса Design.pro */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #212529;
}

.table th {
    font-weight: 600;
}

.object-fit-cover {
    object-fit: cover;
}

.invalid-feedback {
    display: block;
    font-size: 0.8rem;
}

```

---
# Секция 1. Практическая работа №2.1. Реализация функционала гостя

## 1.1. Постановка задачи и регламент ПР №2.1
В рамках практической работы №2.1 реализуется функционал для неавторизованного посетителя интернет-портала:
1. **Просмотр главной страницы:**
   - Отображение динамического счетчика количества заявок в статусе «Принято в работу».
   - Вывод карточек **не более 4 последних выполненных работ** (статус «Выполнено») с эффектом интерактивной смены фото готового дизайна при наведении курсора / переключении.
2. **Регистрация нового пользователя:**
   - Серверная валидация: ФИО (только кириллица, дефис, пробелы), логин (латиница и дефис, уникальный), email, пароли (совпадение), обязательное согласие на обработку персональных данных.
   - Подсветка невалидных полей красным цветом (класс `is-invalid`) и вывод описания ошибки под полем.
   - Автоматическая авторизация сразу после успешной регистрации.
3. **Вход в личный кабинет по логину и паролю:**
   - Аутентификация через Django Auth.
   - Ролевая маршрутизация: клиент направляется в Личный кабинет (`/cabinet/`), администратор — в Панель управления (`/admin-panel/`).
   - Поддержка безопасного возврата на запрашиваемую страницу через параметр `?next=`.

---

## 1.2. Теория и архитектура гостевого функционала

### Механика рендеринга форм и серверной подсветки ошибок:
### 10.4. Механика рендеринга форм и серверной подсветки ошибок

В проекте реализована строгая серверная валидация. Если пользователь допустил ошибку при регистрации или создании заявки, страница не сбрасывается, а подсвечивает ошибочные поля:

#### Как это работает в кодовой связке:
1. **Во View (`views.py`):**  
   При ошибке валидации форма передается в шаблон с объектом ошибок:
   ```python
   form = UserRegistrationForm(request.POST)
   if not form.is_valid():
       return render(request, 'registration/register.html', {'form': form})
   ```
2. **В шаблоне (`register.html`):**  
   Шаблон проверяет наличие ошибок у конкретного поля через `{% if form.fio.errors %}`:
   ```html
   <input type="text"
          name="{{ form.fio.html_name }}"
          value="{{ form.fio.value|default:'' }}"
          class="form-control {% if form.fio.errors %}is-invalid{% endif %}"
          required>
   {% if form.fio.errors %}
       <div class="invalid-feedback d-block">
           {% for error in form.fio.errors %}{{ error }}{% endfor %}
       </div>
   {% endif %}
   ```
   - Класс Bootstrap `is-invalid` окрашивает границу поля в **красный цвет**.
   - Блок `invalid-feedback` выводит точный текст ошибки («ФИО может содержать только кириллические буквы, дефис и пробелы»).
   - Выражение `value="{{ form.fio.value|default:'' }}"` сохраняет ранее введенный текст, чтобы пользователю не приходилось заполнять всю форму заново.

3. **Загрузка файлов (`enctype="multipart/form-data"`):**  
   В формах создания заявки [application_form.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/application_form.html) и завершения дизайна [admin_panel.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/admin_panel.html) обязательно указан атрибут:
   ```html
   <form method="post" enctype="multipart/form-data">
   ```
   Без `enctype="multipart/form-data"` браузер передаст на сервер только имя файла в виде строки, а само бинарное тело изображения не попадет в `request.FILES`, и файл не сохранится.

---

### Безопасность паролей (PBKDF2):
Пароли никогда не сохраняются в открытом виде. В методе `save()` формы вызывается `user.set_password()`, который хэширует пароль алгоритмом **PBKDF2 с SHA-256** и добавлением уникальной криптографической соли.

---

## 1.3. Пошаговая реализация бэкенда для ПР №2.1

### 1. Кастомная модель пользователя (`User`)
Файл: [catalog/models.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/models.py)
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    fio = models.CharField(
        max_length=150,
        verbose_name='ФИО',
        help_text='ФИО (только кириллические буквы, дефис и пробелы)'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} ({self.fio if self.fio else self.get_full_name()})'
```

### 2. Формы регистрации и авторизации (`catalog/forms.py`)
Из файла [catalog/forms.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/forms.py):
- `UserRegistrationForm`: реализует методы `clean_fio()`, `clean_username()`, `clean()` для паролей и валидацию согласия на ПДн.
- `UserLoginForm`: реализует аутентификацию через `authenticate(username=..., password=...)`.

### 3. Контроллеры гостевого функционала (`catalog/views.py`)
Файл: [catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/views.py)
- `index(request)`: вычисляет счетчик `Application.objects.filter(status=Application.STATUS_IN_PROGRESS).count()` и срез 4-х последних выполненных работ `completed_apps = Application.objects.filter(status=Application.STATUS_COMPLETED).select_related('category').order_by('-created_at')[:4]`.
- `register_view(request)`: сохраняет пользователя, вызывает `login(request, user)` и перенаправляет в кабинет.
- `login_view(request)`: аутентифицирует пользователя и перенаправляет в зависимости от флагов `is_staff` / `is_superuser`.

### 4. Маршрутизация URL (`catalog/urls.py`)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]
```

---

## 1.4. Пошаговый разбор и полный код шаблонов ПР №2.1

### 1. Главная страница (`templates/index.html`)
#### 2. [templates/index.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/index.html) — Главная страница
- **Информационный блок Hero:** Легкий блок со сведениями о студии и динамическими кнопками (для гостя — «Регистрация» и «Вход», для клиента — «Создать заявку» и «Мои заявки»).
- **Счетчик по ТЗ:**  
  В правом блоке крупно выводится число `{{ in_progress_count }}` — количество заявок в статусе «Принято в работу».
- **Сетка из 4 последних выполненных работ:**  
  Используется `row row-cols-1 row-cols-sm-2 row-cols-md-4 g-3`.  
  Карточка отображает:
  - Фотографию дизайна `{{ app.design_image.url }}` или исходный план `{{ app.photo.url }}` с классом `object-fit-cover`.
  - Бейдж категории `{{ app.category.name }}`.
  - Название заявки `{{ app.title }}` с защитой от переполнения (`text-truncate`).
  - Описание заявки с обрезкой по высоте (`-webkit-line-clamp: 2`).
  - Дату добавления `{{ app.created_at|date:"d.m.Y H:i" }}`.

#### Полный код `templates/index.html`:
Файл: [templates/index.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/index.html)

### 2. `templates/index.html` (Главная страница):
```html
{% extends 'base.html' %}

{% block title %}Главная — Design.pro{% endblock %}

{% block content %}
<div class="container">

    <!-- Простой информационный блок -->
    <div class="p-4 p-md-5 mb-4 bg-light rounded-3 border">
        <div class="row align-items-center">
            <div class="col-md-8">
                <h1 class="h2 fw-bold text-dark mb-2">Студия интерьеров «Design.pro»</h1>
                <p class="text-secondary mb-3">
                    Проектирование и создание вариантов оформления интерьеров жилых помещений. Загрузите план вашего помещения, и дизайнеры подготовят индивидуальный проект.
                </p>
                <div class="d-flex gap-2">
                    {% if user.is_authenticated %}
                        <a href="{% url 'application-create' %}" class="btn btn-primary">Создать заявку</a>
                        <a href="{% url 'cabinet' %}" class="btn btn-outline-secondary">Мои заявки</a>
                    {% else %}
                        <a href="{% url 'register' %}" class="btn btn-primary">Регистрация</a>
                        <a href="{% url 'login' %}" class="btn btn-outline-primary">Вход в кабинет</a>
                    {% endif %}
                </div>
            </div>

            <!-- Счетчик по ТЗ: Количество заявок в статусе "Принято в работу" -->
            <div class="col-md-4 mt-3 mt-md-0 text-center">
                <div class="p-3 bg-white border rounded-3 shadow-sm">
                    <div class="text-muted small text-uppercase fw-semibold">Заявок в работе прямо сейчас</div>
                    <div class="display-4 fw-bold text-primary my-1" id="in-progress-counter">{{ in_progress_count }}</div>
                    <div class="text-muted small">В статусе «Принято в работу»</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Раздел: Последние выполненные проекты (не более 4) -->
    <div class="my-4">
        <h3 class="h4 fw-bold mb-3">Последние выполненные проекты</h3>

        {% if completed_apps %}
            <div class="row row-cols-1 row-cols-sm-2 row-cols-md-4 g-3">
                {% for app in completed_apps %}
                    <div class="col">
                        <div class="card h-100 border shadow-sm">
                            <!-- Фотография дизайна или плана по ТЗ -->
                            {% if app.design_image %}
                                <img src="{{ app.design_image.url }}" class="card-img-top object-fit-cover" alt="{{ app.title }}" style="height: 160px;">
                            {% elif app.photo %}
                                <img src="{{ app.photo.url }}" class="card-img-top object-fit-cover" alt="{{ app.title }}" style="height: 160px;">
                            {% else %}
                                <div class="bg-light d-flex align-items-center justify-content-center text-muted" style="height: 160px;">
                                    Нет фото
                                </div>
                            {% endif %}

                            <div class="card-body p-3 d-flex flex-column">
                                <span class="badge bg-secondary mb-2 align-self-start">{{ app.category.name }}</span>
                                <h6 class="card-title fw-bold mb-1 text-truncate" title="{{ app.title }}">{{ app.title }}</h6>
                                <p class="card-text text-muted small flex-grow-1" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                                    {{ app.description }}
                                </p>
                                <div class="text-muted small pt-2 border-top mt-2">
                                    <i class="bi bi-calendar"></i> {{ app.created_at|date:"d.m.Y H:i" }}
                                </div>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="p-4 text-center bg-light border rounded">
                <p class="text-muted mb-0">Пока нет выполненных проектов со статусом «Выполнено».</p>
            </div>
        {% endif %}
    </div>

</div>
{% endblock %}

```

---

### 2. Форма регистрации (`templates/registration/register.html`)
#### 6. [templates/registration/login.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/registration/login.html) и [register.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/registration/register.html)
- Аккуратные карточки авторизации и регистрации.
- В шаблоне входа встроена подсказка с учетными данными администратора: логин `admin`, пароль `admin`.
- В шаблоне регистрации выведен обязательный чекбокс согласия на обработку персональных данных и подробные подсказки к формату логина и ФИО.

---

#### Полный код `templates/registration/register.html`:
Файл: [templates/registration/register.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/registration/register.html)

### 8. `templates/registration/register.html` (Страница регистрации с подсветкой ошибок):
```html
{% extends 'base.html' %}

{% block title %}Регистрация — Design.pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card border-0 shadow rounded-4 p-4 p-md-5 bg-white">
                <div class="text-center mb-4">
                    <div class="d-inline-flex p-3 rounded-circle bg-primary bg-opacity-10 text-primary mb-3">
                        <i class="bi bi-person-plus-fill fs-2"></i>
                    </div>
                    <h2 class="fw-bold">Регистрация в Design.pro</h2>
                    <p class="text-muted small">Заполните поля для создания учетной записи</p>
                </div>

                <form method="post" novalidate>
                    {% csrf_token %}

                    {% if form.non_field_errors %}
                        <div class="alert alert-danger py-2 small">
                            {% for error in form.non_field_errors %}
                                <div><i class="bi bi-exclamation-circle me-1"></i> {{ error }}</div>
                            {% endfor %}
                        </div>
                    {% endif %}

                    <!-- ФИО -->
                    <div class="mb-3">
                        <label for="{{ form.fio.id_for_label }}" class="form-label fw-semibold">
                            {{ form.fio.label }} <span class="text-danger">*</span>
                        </label>
                        <input type="text"
                               name="{{ form.fio.html_name }}"
                               id="{{ form.fio.id_for_label }}"
                               value="{{ form.fio.value|default:'' }}"
                               class="form-control {% if form.fio.errors %}is-invalid{% endif %}"
                               placeholder="Иванов Иван Иванович"
                               required>
                        <div class="form-text small">Только кириллические буквы, дефис и пробелы</div>
                        {% if form.fio.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.fio.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <!-- Логин -->
                    <div class="mb-3">
                        <label for="{{ form.username.id_for_label }}" class="form-label fw-semibold">
                            {{ form.username.label }} <span class="text-danger">*</span>
                        </label>
                        <input type="text"
                               name="{{ form.username.html_name }}"
                               id="{{ form.username.id_for_label }}"
                               value="{{ form.username.value|default:'' }}"
                               class="form-control {% if form.username.errors %}is-invalid{% endif %}"
                               placeholder="ivanov-ivan"
                               required>
                        <div class="form-text small">Только латинские буквы и дефис, уникальный</div>
                        {% if form.username.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.username.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <!-- Email -->
                    <div class="mb-3">
                        <label for="{{ form.email.id_for_label }}" class="form-label fw-semibold">
                            {{ form.email.label }} <span class="text-danger">*</span>
                        </label>
                        <input type="email"
                               name="{{ form.email.html_name }}"
                               id="{{ form.email.id_for_label }}"
                               value="{{ form.email.value|default:'' }}"
                               class="form-control {% if form.email.errors %}is-invalid{% endif %}"
                               placeholder="ivanov@example.com"
                               required>
                        {% if form.email.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.email.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <!-- Пароль -->
                    <div class="mb-3">
                        <label for="{{ form.password.id_for_label }}" class="form-label fw-semibold">
                            {{ form.password.label }} <span class="text-danger">*</span>
                        </label>
                        <input type="password"
                               name="{{ form.password.html_name }}"
                               id="{{ form.password.id_for_label }}"
                               class="form-control {% if form.password.errors %}is-invalid{% endif %}"
                               placeholder="Введите надежный пароль"
                               required>
                        {% if form.password.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.password.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <!-- Повтор пароля -->
                    <div class="mb-3">
                        <label for="{{ form.password_confirm.id_for_label }}" class="form-label fw-semibold">
                            {{ form.password_confirm.label }} <span class="text-danger">*</span>
                        </label>
                        <input type="password"
                               name="{{ form.password_confirm.html_name }}"
                               id="{{ form.password_confirm.id_for_label }}"
                               class="form-control {% if form.password_confirm.errors %}is-invalid{% endif %}"
                               placeholder="Повторите пароль"
                               required>
                        {% if form.password_confirm.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.password_confirm.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <!-- Согласие на обработку ПДн -->
                    <div class="mb-4 form-check">
                        <input type="checkbox"
                               name="{{ form.agree_data_processing.html_name }}"
                               id="{{ form.agree_data_processing.id_for_label }}"
                               class="form-check-input {% if form.agree_data_processing.errors %}is-invalid{% endif %}"
                               {% if form.agree_data_processing.value %}checked{% endif %}
                               required>
                        <label class="form-check-label small" for="{{ form.agree_data_processing.id_for_label }}">
                            Я даю согласие на обработку персональных данных <span class="text-danger">*</span>
                        </label>
                        {% if form.agree_data_processing.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.agree_data_processing.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <button type="submit" class="btn btn-primary w-100 py-2 fw-semibold shadow-sm">
                        <i class="bi bi-check2-circle me-1"></i> Зарегистрироваться
                    </button>
                </form>

                <hr class="my-4 text-secondary opacity-25">

                <div class="text-center small">
                    Уже зарегистрированы? <a href="{% url 'login' %}" class="fw-semibold text-decoration-none">Войти в аккаунт</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```

---

### 3. Форма авторизации (`templates/registration/login.html`)
Файл: [templates/registration/login.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/registration/login.html)

### 7. `templates/registration/login.html` (Страница авторизации):
```html
{% extends 'base.html' %}

{% block title %}Вход — Design.pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card border-0 shadow rounded-4 p-4 p-md-5 bg-white">
                <div class="text-center mb-4">
                    <div class="d-inline-flex p-3 rounded-circle bg-primary bg-opacity-10 text-primary mb-3">
                        <i class="bi bi-box-arrow-in-right fs-2"></i>
                    </div>
                    <h2 class="fw-bold">Авторизация</h2>
                    <p class="text-muted small">Введите логин и пароль для входа в систему</p>
                </div>

                <form method="post" novalidate>
                    {% csrf_token %}

                    {% if form.non_field_errors %}
                        <div class="alert alert-danger py-2 small mb-3">
                            {% for error in form.non_field_errors %}
                                <div><i class="bi bi-exclamation-triangle-fill me-1"></i> {{ error }}</div>
                            {% endfor %}
                        </div>
                    {% endif %}

                    <div class="mb-3">
                        <label for="{{ form.username.id_for_label }}" class="form-label fw-semibold">
                            Логин <span class="text-danger">*</span>
                        </label>
                        <input type="text"
                               name="{{ form.username.html_name }}"
                               id="{{ form.username.id_for_label }}"
                               value="{{ form.username.value|default:'' }}"
                               class="form-control {% if form.username.errors or form.non_field_errors %}is-invalid{% endif %}"
                               placeholder="Введите логин"
                               required autofocus>
                        {% if form.username.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.username.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <div class="mb-4">
                        <label for="{{ form.password.id_for_label }}" class="form-label fw-semibold">
                            Пароль <span class="text-danger">*</span>
                        </label>
                        <input type="password"
                               name="{{ form.password.html_name }}"
                               id="{{ form.password.id_for_label }}"
                               class="form-control {% if form.password.errors or form.non_field_errors %}is-invalid{% endif %}"
                               placeholder="Введите пароль"
                               required>
                        {% if form.password.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.password.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <button type="submit" class="btn btn-primary w-100 py-2 fw-semibold shadow-sm">
                        <i class="bi bi-box-arrow-in-right me-1"></i> Войти
                    </button>
                </form>

                <div class="alert alert-info py-2 px-3 small mt-4 mb-0 bg-light border">
                    <i class="bi bi-info-circle-fill text-primary me-1"></i>
                    <strong>Данные администратора:</strong> логин <code>admin</code>, пароль <code>admin</code>
                </div>

                <hr class="my-4 text-secondary opacity-25">

                <div class="text-center small">
                    Еще нет аккаунта? <a href="{% url 'register' %}" class="fw-semibold text-decoration-none">Зарегистрироваться</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```

---

## 1.5. Готовый отчет по практической работе №2.1

```markdown
МИНИСТЕРСТВО ПРОСВЕЩЕНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ
ОТЧЕТ ПО ПРАКТИЧЕСКОЙ РАБОТЕ №2.1
Тема: «Реализация функционала гостя на веб-портале Design.pro»

1. ЦЕЛЬ РАБОТЫ:
Освоить паттерн разработки Model-View-Template (MVT) в среде Django, разработать кастомную модель пользователя с дополнительным полем ФИО, реализовать механизм регистрации с жесткой серверной валидацией входных данных и подсветкой ошибок в интерфейсе, а также создать систему аутентификации с ролевым разделением маршрутизации.

2. ТЕХНИЧЕСКИЕ СРЕДСТВА И ОКРУЖЕНИЕ:
- Среда разработки: PyCharm 2024.x
- Язык программирования: Python 3.12
- Веб-фреймворк: Django 5.x
- СУБД: SQLite 3
- Порт сервера: http://localhost:8089/

3. ХОД ВЫПОЛНЕНИЯ РАБОТЫ:
3.1. Создана кастомная модель User, наследующая AbstractUser, с полем fio = models.CharField(max_length=150). В settings.py зарегистрирована директива AUTH_USER_MODEL = 'catalog.User'.
3.2. Создана форма UserRegistrationForm в catalog/forms.py с реализацией строгой валидации:
     - clean_fio(): валидация кириллицы, дефисов и пробелов регулярным выражением r'^[а-яА-ЯёЁ\s-]+$'.
     - clean_username(): валидация латинских букв и дефисов регулярным выражением r'^[a-zA-Z-]+$', а также регистронезависимая проверка уникальности логина в базе данных.
     - clean(): проверка совпадения полей password и password_confirm.
     - agree_data_processing: валидация обязательного чекбокса согласия на обработку ПДн.
3.3. Разработан контроллер index() в catalog/views.py. Для подсчета заявок в работе применен метод Application.objects.filter(status='in_progress').count(). Для вывода 4-х последних выполненных заявок применен срез [:4] с оптимизацией выборки .select_related('category').
3.4. В шаблоне register.html реализован вывод классов is-invalid и блоков div.invalid-feedback для подсветки невалидных полей красной рамкой.
3.5. Разработан контроллер login_view(), обеспечивающий аутентификацию через authenticate() и дифференцированный редирект: администраторы направляются на /admin-panel/, клиенты — на /cabinet/.

4. РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:
- Попытка регистрации с логином "иванов" (кириллица) отклонена с сообщением: «Логин может содержать только латинские буквы и дефис».
- Попытка регистрации с ФИО "John Doe" (латиница) отклонена с сообщением: «ФИО может содержать только кириллические буквы, дефис и пробелы».
- Попытка регистрации без чекбокса согласия на ПДн отклонена с сообщением: «Необходимо согласиться на обработку персональных данных».
- Успешная регистрация приводит к автоматической авторизации и мгновенному переходу в личный кабинет.
- Счетчик на главной странице точно отображает количество заявок в статусе «Принято в работу».

5. ВЫВОД:
Все требования практической работы №2.1 выполнены в полном объеме. Обеспечена высокая надежность за счет серверной валидации и удобный интерфейс с интерактивной обратной связью.
```

---

## 1.6. Контрольные вопросы и эталонные ответы для защиты ПР №2.1

1. **Вопрос:** Что такое MVT в Django и чем отличается от MVC?  
   **Ответ:** MVT — это архитектурная разновидность паттерна MVC. Model отвечает за базу данных и ORM, View играет роль Контроллера (обрабатывает HTTP-запрос, применяет бизнес-логику и взаимодействует с моделями), а Template выполняет роль View (отвечает за визуальное представление и рендеринг HTML для пользователя).

2. **Вопрос:** Почему мы создали кастомную модель `User` через `AbstractUser` и почему это нужно делать в начале проекта?  
   **Ответ:** Это позволило добавить обязательное поле ФИО в саму таблицу пользователей. Это быстрее и архитектурно чище, чем делать дополнительную связанную таблицу `Profile` через `OneToOneField`, требующую постоянных SQL `JOIN`. Объявлять модель в `AUTH_USER_MODEL` нужно до первой миграции, чтобы стандартные приложения Django связали свои внешние ключи с нашей таблицей.

3. **Вопрос:** Как обеспечивается уникальность логина?  
   **Ответ:** На уровне БД ограничением `UNIQUE` поля `username` и на уровне формы в методе `clean_username()`, где выполняется регистронезависимая проверка `User.objects.filter(username__iexact=username).exists()`.

4. **Вопрос:** Как устроен счетчик заявок в работе на главной?  
   **Ответ:** `Application.objects.filter(status='in_progress').count()` выполняет быстрый SQL-запрос `SELECT COUNT(*)`, не выгружая объекты в оперативную память сервера Python.

5. **Вопрос:** Как ограничивается вывод не более 4 выполненных заявок на главной странице?  
   **Ответ:** Срез `[:4]` в QuerySet транслируется в SQL-директиву `LIMIT 4`.

6. **Вопрос:** Зачем нужен `{% csrf_token %}` в формах?  
   **Ответ:** Для защиты от межсайтовой подделки запросов (Cross-Site Request Forgery). Django сверяет криптографический токен формы со значением в куках пользователя, исключая несанкционированную отправку форм со сторонних ресурсов.

7. **Вопрос:** Что делает `select_related('category')` в запросах?  
   **Ответ:** Это жадная загрузка (Eager Loading), которая объединяет таблицы через SQL `JOIN` и решает проблему «N+1 запросов», извлекая категорию сразу вместе с заявкой.

8. **Вопрос:** В каком виде хранятся пароли в базе данных?  
   **Ответ:** В виде криптографического хеша алгоритма PBKDF2 с солью, сформированного методом `user.set_password()`.

9. **Вопрос:** Как подсвечиваются поля с ошибками при регистрации?  
   **Ответ:** В шаблоне проверяется `{% if form.field.errors %}` и тегу `<input>` присваивается CSS-класс `is-invalid`, а под ним выводится контейнер `<div class="invalid-feedback">` с текстом ошибки.

---
# Секция 2. Практическая работа №2.2. Реализация функционала зарегистрированного пользователя

## 2.1. Постановка задачи и регламент ПР №2.2
В рамках практической работы №2.2 разрабатывается функционал для авторизованного клиента дизайн-студии:
1. **Выход из системы (Logout):**
   - Завершение сессии пользователя с очисткой cookie и редиректом на главную страницу с flash-сообщением.
2. **Создание заявки на разработку дизайна интерьера:**
   - Поля: Название, Описание, Категория (выбор из базы данных), План/фото помещения.
   - Валидация файла: форматы строго `.jpg, .jpeg, .png, .bmp`, предельный размер — **не более 2 Мб**.
   - Автоматическая фиксация статуса «Новая» и временной метки добавления.
   - Автоматическая привязка заявки к текущему авторизованному клиенту `request.user`.
3. **Просмотр своих заявок (Личный кабинет):**
   - Вывод информации: временная метка, название, описание, категория, статус заявки, фото плана.
   - Сортировка по умолчанию: от новых к старым (`-created_at`).
   - Фильтрация по статусам: «Все», «Новая», «Принято в работу», «Выполнено» со счетчиками-бейджами.
4. **Удаление своей заявки:**
   - Строгий контроль прав: пользователь может удалить **только свою заявку** и **только со статусом «Новая»**.
   - Промежуточная страница подтверждения удаления для исключения случайной потери данных.
   - Защита от прямого вызова URL удаления чужих заявок (HTTP 403 Forbidden).

---

## 2.2. Теория и архитектура пользовательского функционала

### Валидация бинарных файлов и Pillow:
Загрузка файлов требует указания `enctype="multipart/form-data"` в форме. Валидатор `validate_photo_file` проверяет размер через `file.size <= 2 * 1024 * 1024` и расширение файла. Библиотека Pillow валидирует графический поток байтов, исключая маскировку исполняемых файлов под изображения.

### Безопасное удаление данных (Защита от IDOR / Broken Access Control):
Удаление выполняется только методом POST с CSRF-токеном. В контроллере проверяется `application.user == request.user` и `application.status == 'new'`. Это исключает удаление чужих заявок или заявок, уже принятых в работу дизайнерами.

---

## 2.3. Пошаговая реализация бэкенда для ПР №2.2

### 1. Модели `Category` и `Application`
Файл: [catalog/models.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/models.py)
```python
def validate_photo_file(file):
    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла не должен превышать {max_size_mb} Мб.')
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
        raise ValidationError(f'Недопустимый формат файла ({ext}). Разрешены: jpg, jpeg, png, bmp.')

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

class Application(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_IN_PROGRESS, 'Принято в работу'),
        (STATUS_COMPLETED, 'Выполнено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='applications', verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название заявки')
    description = models.TextField(verbose_name='Описание заявки')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='applications', verbose_name='Категория')
    photo = models.ImageField(upload_to='photos/', validators=[validate_photo_file],
                              verbose_name='Фото помещения или его план')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Временная метка добавления')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name='Статус')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий администратора')
    design_image = models.ImageField(upload_to='designs/', blank=True, null=True, verbose_name='Изображение дизайна')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    @property
    def is_deletable(self):
        return self.status == self.STATUS_NEW
```

### 2. Форма создания заявки (`catalog/forms.py`)
Форма `ApplicationCreateForm` содержит поля `title`, `description`, `category`, `photo` с переопределением метода `clean_photo()` для валидации веса и типа файла.

### 3. Контроллеры пользователя (`catalog/views.py`)
- `logout_view(request)`: завершает сессию через `logout(request)`.
- `cabinet_view(request)`: защищен декоратором `@login_required`, производит фильтрацию по `user=request.user` и GET-параметру `status`.
- `create_application_view(request)`: сохраняет заявку через `form.save(commit=False)` с привязкой `app.user = request.user` и начальным статусом `STATUS_NEW`.
- `delete_application_view(request, pk)`: проверяет `application.user == request.user` и `application.is_deletable`, после чего удаляет объект.

### 4. Маршрутизация URL (`catalog/urls.py`)
```python
urlpatterns += [
    path('logout/', views.logout_view, name='logout'),
    path('cabinet/', views.cabinet_view, name='cabinet'),
    path('application/create/', views.create_application_view, name='application-create'),
    path('application/<int:pk>/delete/', views.delete_application_view, name='application-delete'),
]
```

---

## 2.4. Пошаговый разбор и полный код шаблонов ПР №2.2

### 1. Личный кабинет пользователя (`templates/catalog/cabinet.html`)
#### 3. [templates/catalog/cabinet.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/cabinet.html) — Личный кабинет клиента
- **Панель быстрой фильтрации:**  
  Кнопки `btn-group` с параметрами `?status=all`, `?status=new`, `?status=in_progress`, `?status=completed`.  
  Текущий выбранный фильтр подсвечивается темным цветом через проверку:
  `{% if current_filter == 'new' %}btn-dark{% else %}btn-outline-secondary{% endif %}`.
- **Компактная адаптивная таблица:**  
  Включает колонки: Дата, Название и описание, Категория, Миниатюра плана, Цветной бейдж статуса (Новая — желтый, В работе — голубой, Выполнено — зеленый), Ответ студии (комментарий или кнопка открытия дизайна).
- **Динамические модальные окна подтверждения удаления:**  
  Каждая строка таблицы для заявки в статусе «Новая» генерирует уникальное модальное окно:
  ```html
  <button data-bs-toggle="modal" data-bs-target="#delModal{{ app.pk }}">Удалить</button>
  <div class="modal fade" id="delModal{{ app.pk }}"> ... </div>
  ```
  Использование `{{ app.pk }}` в ID модального окна гарантирует, что при нажатии кнопки «Удалить» откроется диалог подтверждения строго для выбранной заявки без применения сложного JavaScript.
- **Блокировка удаления:**  
  Если статус заявки изменен администратором на «В работе» или «Выполнено», кнопка удаления заменяется текстом «Недоступно», а бэкенд дополнительно отклоняет любые несанкционированные попытки удаления.

#### Полный код `templates/catalog/cabinet.html`:
Файл: [templates/catalog/cabinet.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/catalog/cabinet.html)

### 3. `templates/catalog/cabinet.html` (Личный кабинет пользователя):
```html
{% extends 'base.html' %}

{% block title %}Личный кабинет — Design.pro{% endblock %}

{% block content %}
<div class="container">

    <!-- Заголовок и кнопка -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
            <h2 class="h3 fw-bold mb-0">Мои заявки на дизайн</h2>
            <div class="text-muted small">Пользователь: {{ user.fio|default:user.username }}</div>
        </div>
        <a href="{% url 'application-create' %}" class="btn btn-primary btn-sm">+ Новая заявка</a>
    </div>

    <!-- Фильтрация по статусу -->
    <div class="mb-3 d-flex align-items-center gap-2">
        <span class="small text-muted">Фильтр:</span>
        <div class="btn-group btn-group-sm" role="group">
            <a href="{% url 'cabinet' %}?status=all" class="btn {% if current_filter == 'all' or not current_filter %}btn-dark{% else %}btn-outline-secondary{% endif %}">
                Все ({{ total_count }})
            </a>
            <a href="{% url 'cabinet' %}?status=new" class="btn {% if current_filter == 'new' %}btn-dark{% else %}btn-outline-secondary{% endif %}">
                Новые ({{ new_count }})
            </a>
            <a href="{% url 'cabinet' %}?status=in_progress" class="btn {% if current_filter == 'in_progress' %}btn-dark{% else %}btn-outline-secondary{% endif %}">
                В работе ({{ in_progress_count }})
            </a>
            <a href="{% url 'cabinet' %}?status=completed" class="btn {% if current_filter == 'completed' %}btn-dark{% else %}btn-outline-secondary{% endif %}">
                Выполненные ({{ completed_count }})
            </a>
        </div>
    </div>

    <!-- Таблица заявок -->
    {% if applications %}
        <div class="table-responsive border rounded bg-white">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light small">
                    <tr>
                        <th>Дата</th>
                        <th>Название</th>
                        <th>Категория</th>
                        <th>План</th>
                        <th>Статус</th>
                        <th>Ответ студии</th>
                        <th class="text-end">Действие</th>
                    </tr>
                </thead>
                <tbody class="small">
                    {% for app in applications %}
                        <tr>
                            <!-- Временная метка по ТЗ -->
                            <td class="text-nowrap text-muted">{{ app.created_at|date:"d.m.Y H:i" }}</td>

                            <!-- Название и описание по ТЗ -->
                            <td>
                                <div class="fw-bold">{{ app.title }}</div>
                                <div class="text-muted" style="max-width: 250px; font-size: 0.85rem;">{{ app.description }}</div>
                            </td>

                            <!-- Категория заявки по ТЗ -->
                            <td><span class="badge bg-light text-dark border">{{ app.category.name }}</span></td>

                            <!-- Фото помещения -->
                            <td>
                                {% if app.photo %}
                                    <a href="{{ app.photo.url }}" target="_blank">
                                        <img src="{{ app.photo.url }}" alt="План" class="rounded border" style="width: 45px; height: 45px; object-fit: cover;">
                                    </a>
                                {% endif %}
                            </td>

                            <!-- Статус заявки по ТЗ -->
                            <td>
                                {% if app.status == 'new' %}
                                    <span class="badge bg-warning text-dark">Новая</span>
                                {% elif app.status == 'in_progress' %}
                                    <span class="badge bg-info text-dark">Принято в работу</span>
                                {% elif app.status == 'completed' %}
                                    <span class="badge bg-success">Выполнено</span>
                                {% endif %}
                            </td>

                            <!-- Ответ студии (комментарий или дизайн) -->
                            <td>
                                {% if app.status == 'in_progress' and app.comment %}
                                    <span class="text-info-emphasis"><strong>Комментарий:</strong> {{ app.comment }}</span>
                                {% elif app.status == 'completed' %}
                                    <div class="d-flex align-items-center gap-1">
                                        {% if app.design_image %}
                                            <a href="{{ app.design_image.url }}" target="_blank" class="btn btn-sm btn-outline-success py-0 px-2">Дизайн</a>
                                        {% endif %}
                                        {% if app.comment %}<small class="text-muted">{{ app.comment }}</small>{% endif %}
                                    </div>
                                {% else %}
                                    <span class="text-muted">—</span>
                                {% endif %}
                            </td>

                            <!-- Кнопка удаления (только если статус Новая) -->
                            <td class="text-end">
                                {% if app.is_deletable %}
                                    <button type="button" class="btn btn-outline-danger btn-sm py-0 px-2" data-bs-toggle="modal" data-bs-target="#delModal{{ app.pk }}">
                                        Удалить
                                    </button>

                                    <!-- Простое окно подтверждения удаления -->
                                    <div class="modal fade text-start" id="delModal{{ app.pk }}" tabindex="-1">
                                        <div class="modal-dialog modal-dialog-centered">
                                            <div class="modal-content">
                                                <div class="modal-header py-2">
                                                    <h6 class="modal-title fw-bold">Подтверждение удаления</h6>
                                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                                </div>
                                                <div class="modal-body">
                                                    Вы действительно хотите удалить заявку <strong>«{{ app.title }}»</strong>?
                                                </div>
                                                <div class="modal-footer py-2">
                                                    <button type="button" class="btn btn-sm btn-light" data-bs-dismiss="modal">Отмена</button>
                                                    <form method="post" action="{% url 'application-delete' app.pk %}">
                                                        {% csrf_token %}
                                                        <button type="submit" class="btn btn-sm btn-danger">Да, удалить</button>
                                                    </form>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                {% else %}
                                    <span class="text-muted small" title="Удалить можно только заявку со статусом «Новая»">Недоступно</span>
                                {% endif %}
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <div class="p-4 text-center border rounded bg-light">
            <p class="text-muted mb-2">Заявок с выбранным фильтром не найдено.</p>
            <a href="{% url 'application-create' %}" class="btn btn-sm btn-primary">Создать первую заявку</a>
        </div>
    {% endif %}

</div>
{% endblock %}

```

---

### 2. Форма создания заявки (`templates/catalog/application_form.html`)
#### 5. [templates/catalog/application_form.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/application_form.html) — Создание заявки
- Компактная центрированная карточка шириной до 650px.
- Поля: Название заявки, Категория (выпадающий список `<select>`), Описание, Поле выбора файла плана с памяткой: *«Разрешены форматы: jpg, jpeg, png, bmp. Максимальный размер: до 2 Мб»*.

#### Полный код `templates/catalog/application_form.html`:
Файл: [templates/catalog/application_form.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/catalog/application_form.html)

### 4. `templates/catalog/application_form.html` (Форма создания заявки):
```html
{% extends 'base.html' %}

{% block title %}Создание заявки — Design.pro{% endblock %}

{% block content %}
<div class="container" style="max-width: 650px;">
    <div class="card border p-4 bg-white">
        <div class="mb-3">
            <a href="{% url 'cabinet' %}" class="btn btn-outline-secondary btn-sm mb-2">&larr; Назад к моим заявкам</a>
            <h3 class="h4 fw-bold mb-1">Новая заявка на дизайн</h3>
            <p class="text-muted small mb-0">Все поля обязательны для заполнения</p>
        </div>

        <form method="post" enctype="multipart/form-data" novalidate>
            {% csrf_token %}

            {% if form.non_field_errors %}
                <div class="alert alert-danger py-2 small">
                    {% for err in form.non_field_errors %}{{ err }}{% endfor %}
                </div>
            {% endif %}

            <!-- Название заявки -->
            <div class="mb-3">
                <label class="form-label small fw-semibold">Название заявки <span class="text-danger">*</span></label>
                {{ form.title }}
                {% if form.title.errors %}
                    <div class="text-danger small mt-1">{% for e in form.title.errors %}{{ e }}{% endfor %}</div>
                {% endif %}
            </div>

            <!-- Категория заявки -->
            <div class="mb-3">
                <label class="form-label small fw-semibold">Категория <span class="text-danger">*</span></label>
                {{ form.category }}
                {% if form.category.errors %}
                    <div class="text-danger small mt-1">{% for e in form.category.errors %}{{ e }}{% endfor %}</div>
                {% endif %}
            </div>

            <!-- Описание заявки -->
            <div class="mb-3">
                <label class="form-label small fw-semibold">Описание помещения <span class="text-danger">*</span></label>
                {{ form.description }}
                {% if form.description.errors %}
                    <div class="text-danger small mt-1">{% for e in form.description.errors %}{{ e }}{% endfor %}</div>
                {% endif %}
            </div>

            <!-- Фото помещения или его план -->
            <div class="mb-4">
                <label class="form-label small fw-semibold">Фото помещения или план <span class="text-danger">*</span></label>
                {{ form.photo }}
                <div class="text-muted small mt-1">Разрешенные форматы: <strong>jpg, jpeg, png, bmp</strong>. Максимальный размер: <strong>до 2 Мб</strong>.</div>
                {% if form.photo.errors %}
                    <div class="text-danger small mt-1">{% for e in form.photo.errors %}{{ e }}{% endfor %}</div>
                {% endif %}
            </div>

            <div class="d-flex justify-content-end gap-2">
                <a href="{% url 'cabinet' %}" class="btn btn-light btn-sm">Отмена</a>
                <button type="submit" class="btn btn-primary btn-sm px-4">Отправить заявку</button>
            </div>
        </form>
    </div>
</div>
{% endblock %}

```

---

### 3. Подтверждение удаления заявки (`templates/catalog/application_confirm_delete.html`)
Файл: [templates/catalog/application_confirm_delete.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/catalog/application_confirm_delete.html)

### 5. `templates/catalog/application_confirm_delete.html` (Подтверждение удаления):
```html
{% extends 'base.html' %}

{% block title %}Удаление заявки — Design.pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-0 shadow rounded-4 p-4 p-md-5 bg-white text-center">
                <div class="d-inline-flex p-3 rounded-circle bg-danger bg-opacity-10 text-danger mb-3 mx-auto">
                    <i class="bi bi-trash3-fill fs-1"></i>
                </div>
                <h3 class="fw-bold mb-2">Удаление заявки</h3>
                <p class="text-secondary mb-4">
                    Вы действительно уверены, что хотите удалить заявку:
                    <br>
                    <strong class="text-dark fs-5">«{{ application.title }}»</strong>?
                </p>

                <div class="alert alert-warning text-start small mb-4">
                    <i class="bi bi-exclamation-triangle-fill me-1"></i>
                    Внимание: Данное действие необратимо. Удаление доступно только для заявок со статусом <strong>«Новая»</strong>.
                </div>

                <form method="post">
                    {% csrf_token %}
                    <div class="d-flex justify-content-center gap-3">
                        <a href="{% url 'cabinet' %}" class="btn btn-outline-secondary px-4">
                            Отмена
                        </a>
                        <button type="submit" class="btn btn-danger px-4 fw-semibold">
                            <i class="bi bi-trash3-fill me-1"></i> Да, удалить
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```

---

## 2.5. Готовый отчет по практической работе №2.2

```markdown
МИНИСТЕРСТВО ПРОСВЕЩЕНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ
ОТЧЕТ ПО ПРАКТИЧЕСКОЙ РАБОТЕ №2.2
Тема: «Реализация функционала зарегистрированного пользователя на веб-портале Design.pro»

1. ЦЕЛЬ РАБОТЫ:
Разработать защищенную пользовательскую область (Личный кабинет), спроектировать связанные реляционные модели данных Category и Application, реализовать обработку и серверную валидацию загружаемых медиафайлов, создать интерфейс подачи заявок, фильтрации по статусам и безопасного удаления.

2. ТЕХНИЧЕСКИЕ СРЕДСТВА:
- Python 3.12, Django 5.x, SQLite 3, Pillow (библиотека обработки графики).

3. ХОД ВЫПОЛНЕНИЯ РАБОТЫ:
3.1. В catalog/models.py созданы модели Category и Application с внешним ключом user = ForeignKey(User, on_delete=CASCADE).
3.2. Написан валидатор validate_photo_file(), проверяющий расширение файла (.jpg, .jpeg, .png, .bmp) и лимит веса 2 Мб (2*1024*1024 байт).
3.3. Реализована форма ApplicationCreateForm. В шаблоне application_form.html указан атрибут enctype="multipart/form-data". В контроллере create_application_view данные сохраняются через form.save(commit=False) с назначением app.user = request.user и начального статуса 'new'.
3.4. Реализован личный кабинет cabinet_view(): выборка отфильтрована строго по владельцу (user=request.user) и отсортирована по -created_at. Реализована фильтрация по GET-параметру status с выводом счетчиков для каждого статуса.
3.5. Реализован защищенный механизм удаления заявок в delete_application_view: проверка application.user == request.user (защита от горизонтальной эскалации привилегий) и application.status == 'new'. Для подтверждения выводится шаблон application_confirm_delete.html.
3.6. Реализован контроллер logout_view, очищающий сессию пользователя.

4. РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:
- Успешно загружен план помещения в формате PNG (1.2 Мб).
- При попытке загрузить файл .pdf или изображение размером 3.5 Мб форма возвращает понятное сообщение об ошибке.
- Пользователь видит только свои заявки; переключение фильтров корректно изолирует статусы.
- Удаление заявки со статусом «Новая» проходит успешно. Прямая попытка отправить POST-запрос на удаление заявки со статусом «В работе» отклоняется системой.

5. ВЫВОД:
Пользовательский функционал полностью удовлетворяет требованиям ТЗ. Реализованы жесткие барьеры безопасности, исключающие модификацию и удаление чужих или находящихся в обработке данных.
```

---

## 2.6. Контрольные вопросы и эталонные ответы для защиты ПР №2.2

1. **Вопрос:** Где и как проверяется ограничение размера фото в 2 МБ?  
   **Ответ:** В функции-валидаторе `validate_photo_file` в `models.py`. Она проверяет `file.size > 2 * 1024 * 1024` и расширение файла. При превышении лимита или недопустимом формате выбрасывается исключение `ValidationError`.

2. **Вопрос:** Почему обычный пользователь не может удалить заявку в статусе «Принято в работу»?  
   **Ответ:** В представлении `delete_application_view` проверяется свойство `application.is_deletable` (`status == 'new'`). Если статус изменен на «Принято в работу» или «Выполнено», операция программно пресекается с выводом предупреждающего сообщения.

3. **Вопрос:** Как защищено удаление от подмены `id` в URL (Horizontal Privilege Escalation)?  
   **Ответ:** Запрос выполняется с явной проверкой `if application.user != request.user: return HttpResponseForbidden()`. Пользователь не имеет технической возможности удалить заявку другого клиента.

4. **Вопрос:** Как работает фильтрация по статусу в кабинете?  
   **Ответ:** Через GET-параметр `?status=...`. Контроллер считывает параметр `request.GET.get('status')` и применяет `.filter(status=current_filter)`.

5. **Вопрос:** Что такое `commit=False` в `form.save(commit=False)`?  
   **Ответ:** Создает экземпляр модели в памяти Python, не сохраняя его сразу в базу данных, что позволяет программно привязать текущего пользователя (`application.user = request.user`) и выставить статус `STATUS_NEW`.

6. **Вопрос:** Как работает библиотека Pillow в проекте?  
   **Ответ:** Pillow верифицирует графический поток байтов при сохранении `ImageField`, гарантируя, что под видом картинки не загружен исполняемый файл или скрипт.

7. **Вопрос:** Что выполняет декоратор `@login_required`?  
   **Ответ:** Проверяет `request.user.is_authenticated`. Если пользователь анонимен, перенаправляет его на `LOGIN_URL` с параметром `?next=`.

---
# Секция 3. Практическая работа №2.3. Реализация функционала администратора

## 3.1. Постановка задачи и регламент ПР №2.3
В рамках практической работы №2.3 реализуется функционал управления дизайн-студией:
1. **Разграничение прав доступа:**
   - Панель доступна только администраторам (`is_staff=True` или `is_superuser=True`).
   - Разделение: стандартная админка Django перенесена на URL `/superadmin/`, а служебная панель студии доступна по адресу `/admin-panel/`.
2. **Смена статуса заявки (Конечный автомат / Finite State Machine):**
   - Смена статуса разрешена **только из статуса «Новая»**. Смена со статусов «В работе» или «Выполнено» строго заблокирована!
   - Перевод в **«Принято в работу»**: обязательно текстовое поле с комментарием администратора.
   - Перевод в **«Выполнено»**: обязательно прикрепление изображения дизайна (форматы `jpg, png, bmp`, размер **до 5 Мб**), сохраняемого в директорию `media/designs/`.
3. **Управление категориями заявок:**
   - Добавление новой категории (валидация уникальности без учета регистра).
   - Удаление категории: при удалении категории **каскадно удаляются все связанные заявки** (`on_delete=models.CASCADE`).
   - Страница подтверждения удаления категории с предупреждением о количестве удаляемых заявок.

---

## 3.2. Теория и архитектура административного функционала

### Разграничение прав доступа:
Проверяется предикатом `is_admin(user)` через декоратор `@user_passes_test(is_admin, login_url='login')`. Это гарантирует, что обычный пользователь `ivanov` при попытке открыть `/admin-panel/` получит автоматический редирект на форму авторизации.

### Конечный автомат (State Machine):
Смена статусов допускается только по строгому графу состояний:
- `Новая` ➔ `Принято в работу` (при наличии комментария)
- `Новая` ➔ `Выполнено` (при наличии файла дизайна)
- Повторные переходы заблокированы на уровне модели (`can_change_status`) и контроллеров.

### Каскадное удаление данных (`models.CASCADE`):
Внешний ключ `category = models.ForeignKey(Category, on_delete=models.CASCADE)` гарантирует, что при удалении категории база данных не оставит висячих внешних ключей (сиротских записей).

---

## 3.3. Пошаговая реализация бэкенда для ПР №2.3

### 1. Валидатор дизайна (`validate_design_file`)
```python
def validate_design_file(file):
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Максимальный размер дизайна не должен превышать {max_size_mb} Мб.')
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
        raise ValidationError(f'Недопустимый формат файла ({ext}). Разрешены: jpg, jpeg, png, bmp.')
```

### 2. Формы смены статусов и категории (`catalog/forms.py`)
- `StatusToInProgressForm`: текстовое поле `comment` (обязательно).
- `StatusToCompletedForm`: поле `design_image` (обязательно, валидатор до 5 Мб).
- `CategoryForm`: поле `name` (проверка уникальности `clean_name()`).

### 3. Контроллеры панели администратора (`catalog/views.py`)
- `admin_panel_view(request)`: вывод всех заявок всех пользователей с фильтрацией и списка категорий.
- `admin_change_status_in_progress(request, pk)`: смена на «Принято в работу» при `application.status == STATUS_NEW`.
- `admin_change_status_completed(request, pk)`: смена на «Выполнено» при `application.status == STATUS_NEW` с сохранением дизайна в `media/designs/`.
- `admin_add_category(request)`: создание новой категории.
- `admin_delete_category(request, pk)`: каскадное удаление категории и привязанных заявок.

### 4. Регистрация в стандартной панели Django (`catalog/admin.py`)
Файл: [catalog/admin.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/admin.py)

### 7. `catalog/admin.py` (Полный код):
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Application


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения пользователей в панели superadmin"""
    list_display = ('username', 'fio', 'email', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'fio', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('fio',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('fio',)}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в superadmin"""
    list_display = ('id', 'name', 'applications_count')
    search_fields = ('name',)

    def applications_count(self, obj):
        return obj.applications.count()
    applications_count.short_description = 'Количество заявок'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Настройка отображения заявок в superadmin"""
    list_display = ('id', 'title', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__fio')
    readonly_fields = ('created_at',)
    list_per_page = 20

```

### 5. Маршрутизация URL (`catalog/urls.py`)
```python
urlpatterns += [
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('admin-panel/application/<int:pk>/in-progress/', views.admin_change_status_in_progress, name='admin-status-in-progress'),
    path('admin-panel/application/<int:pk>/completed/', views.admin_change_status_completed, name='admin-status-completed'),
    path('admin-panel/category/add/', views.admin_add_category, name='admin-add-category'),
    path('admin-panel/category/<int:pk>/delete/', views.admin_delete_category, name='admin-delete-category'),
]
```

---

## 3.4. Пошаговый разбор и полный код шаблонов ПР №2.3

### 1. Панель управления администратора (`templates/catalog/admin_panel.html`)
#### 4. [templates/catalog/admin_panel.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/admin_panel.html) — Панель администратора
Разделена на два понятных блока:
- **Блок 1: Управление категориями заявок:**  
  - Компактная форма с инпутом и кнопкой «+ Добавить».
  - Горизонтальный список существующих категорий с бейджами и количеством привязанных заявок.
  - Каждая категория снабжена кнопкой удаления с модальным окном, явно предупреждающим: *«При удалении категории будут удалены все заявки данной категории!»*.
- **Блок 2: Все заявки и смена статусов:**  
  - Таблица всех заявок клиентов с фильтром по статусам.
  - Для заявок в статусе «Новая» доступны две кнопки:
    - **«В работу»:** открывает модальное окно с обязательным полем комментария (`<textarea name="comment" required>`).
    - **«Выполнить»:** открывает модальное окно с обязательным полем загрузки файла дизайна (`<input type="file" name="design_image" required>`).
  - Для заявок в статусе «Принято в работу» или «Выполнено» кнопки скрыты и выводится надпись «Смена статуса невозможна».

#### Полный код `templates/catalog/admin_panel.html`:
Файл: [templates/catalog/admin_panel.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/catalog/admin_panel.html)

### 6. `templates/catalog/admin_panel.html` (Панель управления администратора):
```html
{% extends 'base.html' %}

{% block title %}Панель администратора — Design.pro{% endblock %}

{% block content %}
<div class="container">

    <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
            <h2 class="h3 fw-bold mb-0">Панель администратора</h2>
            <div class="text-muted small">Управление категориями и смена статусов заявок</div>
        </div>
        <div>
            <a href="/superadmin/" target="_blank" class="btn btn-outline-secondary btn-sm">Django Superadmin</a>
        </div>
    </div>

    <!-- БЛОК 1: Управление категориями заявок -->
    <div class="card mb-4 border">
        <div class="card-header bg-light py-2">
            <h6 class="mb-0 fw-bold">1. Управление категориями заявок</h6>
        </div>
        <div class="card-body">
            <div class="row g-3 align-items-center">
                <!-- Форма добавления категории -->
                <div class="col-md-5">
                    <form method="post" action="{% url 'admin-add-category' %}" class="d-flex gap-2">
                        {% csrf_token %}
                        <input type="text" name="name" class="form-control form-control-sm" placeholder="Название новой категории" required>
                        <button type="submit" class="btn btn-primary btn-sm text-nowrap">+ Добавить</button>
                    </form>
                </div>
                <!-- Список категорий -->
                <div class="col-md-7">
                    <div class="d-flex flex-wrap gap-2 align-items-center">
                        <span class="small text-muted">Существующие:</span>
                        {% for cat in categories %}
                            <div class="badge bg-light text-dark border p-2 d-flex align-items-center gap-1">
                                <span>{{ cat.name }} ({{ cat.applications.count }})</span>
                                <button type="button" class="btn-close" style="font-size: 0.55rem;" data-bs-toggle="modal" data-bs-target="#delCat{{ cat.pk }}" title="Удалить категорию"></button>
                            </div>

                            <!-- Модалка удаления категории (с предупреждением о каскадном удалении) -->
                            <div class="modal fade text-start" id="delCat{{ cat.pk }}" tabindex="-1">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="modal-header py-2">
                                            <h6 class="modal-title text-danger fw-bold">Удаление категории «{{ cat.name }}»</h6>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body small">
                                            <strong>Внимание по ТЗ!</strong> При удалении категории будут удалены все заявки данной категории ({{ cat.applications.count }} шт.). Заявки этой категории больше не будут отображаться.
                                        </div>
                                        <div class="modal-footer py-2">
                                            <button type="button" class="btn btn-sm btn-light" data-bs-dismiss="modal">Отмена</button>
                                            <form method="post" action="{% url 'admin-delete-category' cat.pk %}">
                                                {% csrf_token %}
                                                <button type="submit" class="btn btn-sm btn-danger">Удалить категорию и заявки</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {% empty %}
                            <span class="text-muted small">Категорий пока нет.</span>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- БЛОК 2: Заявки на дизайн и смена статусов -->
    <div class="card border">
        <div class="card-header bg-light py-2 d-flex justify-content-between align-items-center">
            <h6 class="mb-0 fw-bold">2. Заявки пользователей и смена статусов</h6>
            <!-- Фильтр -->
            <div class="btn-group btn-group-sm">
                <a href="{% url 'admin_panel' %}?status=all" class="btn {% if status_filter == 'all' or not status_filter %}btn-dark{% else %}btn-outline-secondary{% endif %}">Все ({{ total_count }})</a>
                <a href="{% url 'admin_panel' %}?status=new" class="btn {% if status_filter == 'new' %}btn-dark{% else %}btn-outline-secondary{% endif %}">Новые ({{ new_count }})</a>
                <a href="{% url 'admin_panel' %}?status=in_progress" class="btn {% if status_filter == 'in_progress' %}btn-dark{% else %}btn-outline-secondary{% endif %}">В работе ({{ in_progress_count }})</a>
                <a href="{% url 'admin_panel' %}?status=completed" class="btn {% if status_filter == 'completed' %}btn-dark{% else %}btn-outline-secondary{% endif %}">Выполненные ({{ completed_count }})</a>
            </div>
        </div>

        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 small">
                <thead class="table-light">
                    <tr>
                        <th>№</th>
                        <th>Дата</th>
                        <th>Клиент</th>
                        <th>Заявка</th>
                        <th>Категория</th>
                        <th>План</th>
                        <th>Статус</th>
                        <th class="text-end">Смена статуса</th>
                    </tr>
                </thead>
                <tbody>
                    {% for app in applications %}
                        <tr>
                            <td>#{{ app.pk }}</td>
                            <td class="text-nowrap text-muted">{{ app.created_at|date:"d.m.Y H:i" }}</td>
                            <td>
                                <div>{{ app.user.username }}</div>
                                {% if app.user.fio %}<small class="text-muted">{{ app.user.fio }}</small>{% endif %}
                            </td>
                            <td>
                                <div class="fw-bold">{{ app.title }}</div>
                                <div class="text-muted" style="max-width: 220px;">{{ app.description|truncatewords:8 }}</div>
                                {% if app.comment %}<small class="text-info d-block">Коммент: {{ app.comment }}</small>{% endif %}
                            </td>
                            <td><span class="badge bg-light text-dark border">{{ app.category.name }}</span></td>
                            <td>
                                {% if app.photo %}
                                    <a href="{{ app.photo.url }}" target="_blank">
                                        <img src="{{ app.photo.url }}" alt="План" class="rounded border" style="width: 40px; height: 40px; object-fit: cover;">
                                    </a>
                                {% endif %}
                                {% if app.design_image %}
                                    <a href="{{ app.design_image.url }}" target="_blank" title="Дизайн">
                                        <img src="{{ app.design_image.url }}" alt="Дизайн" class="rounded border border-success" style="width: 40px; height: 40px; object-fit: cover;">
                                    </a>
                                {% endif %}
                            </td>
                            <td>
                                {% if app.status == 'new' %}
                                    <span class="badge bg-warning text-dark">Новая</span>
                                {% elif app.status == 'in_progress' %}
                                    <span class="badge bg-info text-dark">В работе</span>
                                {% elif app.status == 'completed' %}
                                    <span class="badge bg-success">Выполнено</span>
                                {% endif %}
                            </td>
                            <td class="text-end text-nowrap">
                                {% if app.can_change_status %}
                                    <!-- Кнопка 1: В работу -->
                                    <button type="button" class="btn btn-outline-info btn-sm py-0 px-2" data-bs-toggle="modal" data-bs-target="#inProg{{ app.pk }}">
                                        В работу
                                    </button>

                                    <!-- Кнопка 2: Выполнить -->
                                    <button type="button" class="btn btn-outline-success btn-sm py-0 px-2" data-bs-toggle="modal" data-bs-target="#comp{{ app.pk }}">
                                        Выполнить
                                    </button>

                                    <!-- Модалка: Смена на «Принято в работу» (комментарий обязателен) -->
                                    <div class="modal fade text-start" id="inProg{{ app.pk }}" tabindex="-1">
                                        <div class="modal-dialog modal-dialog-centered">
                                            <div class="modal-content">
                                                <div class="modal-header py-2">
                                                    <h6 class="modal-title fw-bold">Принять заявку #{{ app.pk }} в работу</h6>
                                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                                </div>
                                                <form method="post" action="{% url 'admin-status-in-progress' app.pk %}">
                                                    {% csrf_token %}
                                                    <div class="modal-body">
                                                        <label class="form-label small fw-semibold">Укажите комментарий <span class="text-danger">*</span></label>
                                                        <textarea name="comment" class="form-control form-control-sm" rows="3" required placeholder="Например: Взято в работу дизайнером..."></textarea>
                                                    </div>
                                                    <div class="modal-footer py-2">
                                                        <button type="button" class="btn btn-sm btn-light" data-bs-dismiss="modal">Отмена</button>
                                                        <button type="submit" class="btn btn-sm btn-info text-white">Сохранить статус «В работу»</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Модалка: Смена на «Выполнено» (дизайн обязателен) -->
                                    <div class="modal fade text-start" id="comp{{ app.pk }}" tabindex="-1">
                                        <div class="modal-dialog modal-dialog-centered">
                                            <div class="modal-content">
                                                <div class="modal-header py-2">
                                                    <h6 class="modal-title fw-bold">Завершить заявку #{{ app.pk }}</h6>
                                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                                </div>
                                                <form method="post" action="{% url 'admin-status-completed' app.pk %}" enctype="multipart/form-data">
                                                    {% csrf_token %}
                                                    <div class="modal-body">
                                                        <label class="form-label small fw-semibold">Прикрепите изображение дизайна <span class="text-danger">*</span></label>
                                                        <input type="file" name="design_image" class="form-control form-control-sm" accept=".jpg,.jpeg,.png,.bmp" required>
                                                        <small class="text-muted d-block mt-1">Форматы: jpg, jpeg, png, bmp</small>
                                                    </div>
                                                    <div class="modal-footer py-2">
                                                        <button type="button" class="btn btn-sm btn-light" data-bs-dismiss="modal">Отмена</button>
                                                        <button type="submit" class="btn btn-sm btn-success">Сохранить статус «Выполнено»</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                {% else %}
                                    <span class="text-muted small">Смена статуса невозможна</span>
                                {% endif %}
                            </td>
                        </tr>
                    {% empty %}
                        <tr>
                            <td colspan="8" class="text-center py-3 text-muted">Заявок не найдено.</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

</div>
{% endblock %}

```

---

### 2. Подтверждение удаления категории (`templates/catalog/category_confirm_delete.html`)
Файл: [templates/catalog/category_confirm_delete.html](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/templates/catalog/category_confirm_delete.html)

```html
{% extends 'base.html' %}

{% block title %}Удаление категории — Design.pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-0 shadow rounded-4 p-4 p-md-5 bg-white text-center">
                <div class="d-inline-flex p-3 rounded-circle bg-danger bg-opacity-10 text-danger mb-3 mx-auto">
                    <i class="bi bi-exclamation-triangle-fill fs-1"></i>
                </div>
                <h3 class="fw-bold mb-2">Удаление категории</h3>
                <p class="text-secondary mb-3">
                    Вы уверены, что хотите удалить категорию <strong>«{{ category.name }}»</strong>?
                </p>

                <div class="alert alert-danger text-start small mb-4">
                    <strong>Внимание!</strong> При удалении категории будут безвозвратно удалены все связанные заявки ({{ category.applications.count }} шт.).
                </div>

                <form method="post">
                    {% csrf_token %}
                    <div class="d-flex justify-content-center gap-3">
                        <a href="{% url 'admin_panel' %}" class="btn btn-outline-secondary px-4">
                            Отмена
                        </a>
                        <button type="submit" class="btn btn-danger px-4 fw-semibold">
                            <i class="bi bi-trash3-fill me-1"></i> Подтвердить удаление
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 3.5. Готовый отчет по практической работе №2.3

```markdown
МИНИСТЕРСТВО ПРОСВЕЩЕНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ
ОТЧЕТ ПО ПРАКТИЧЕСКОЙ РАБОТЕ №2.3
Тема: «Реализация функционала администратора на веб-портале Design.pro»

1. ЦЕЛЬ РАБОТЫ:
Разработать административную панель управления дизайн-студией, настроить систему разграничения прав доступа на базе декораторов Django, реализовать бизнес-логику конечного автомата смены статусов заявок и управление справочником категорий с каскадным удалением зависимостей.

2. ТЕХНИЧЕСКИЕ СРЕДСТВА:
- Python 3.12, Django 5.x, SQLite 3, Pillow.

3. ХОД ВЫПОЛНЕНИЯ РАБОТЫ:
3.1. Создана функция-предикат is_admin() и контроллеры панели администратора защищены декоратором @user_passes_test(is_admin, login_url='login').
3.2. Стандартный административный интерфейс Django перенесен на URL /superadmin/.
3.3. Реализован конечный автомат смены статусов заявок:
     - Проверка application.status == Application.STATUS_NEW. При попытке изменить статус у заявок 'in_progress' или 'completed' операция блокируется.
     - Форма StatusToInProgressForm требует обязательного указания комментария администратора.
     - Форма StatusToCompletedForm требует обязательного прикрепления графического файла готового дизайна с валидацией размера до 5 Мб (validate_design_file) и сохранением в media/designs/.
3.4. Реализовано управление категориями: форма CategoryForm проверяет регистронезависимую уникальность названия.
3.5. Реализован контроллер admin_delete_category. При подтверждении удаления категории срабатывает правило on_delete=models.CASCADE, удаляющее саму категорию и все сопряженные заявки из таблицы catalog_application.

4. РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:
- Попытка доступа к /admin-panel/ под учетной записью клиента petrov возвращает редирект на вход.
- Успешно переведена новая заявка в статус «Принято в работу» с комментарием «Назначен архитектор».
- Попытка повторно изменить статус у данной заявки заблокирована системой.
- Успешно создана новая категория «Скандинавский стиль» и удалена временная категория — все зависимые заявки корректно стерты каскадом.

5. ВЫВОД:
Административный модуль полностью отвечает требованиям ТЗ. Гарантируется целостность данных, строгое соблюдение регламента смены статусов и надежное разграничение привилегий.
```

---

## 3.6. Контрольные вопросы и эталонные ответы для защиты ПР №2.3

1. **Вопрос:** Что происходит с заявками при удалении категории?  
   **Ответ:** В модели `Application` в поле `category` указано `on_delete=models.CASCADE`. База данных SQLite автоматически удаляет все связанные с этой категорией заявки.

2. **Вопрос:** Почему со статуса «В работе» или «Выполнено» нельзя сменить статус?  
   **Ответ:** Согласно ТЗ, смена разрешена только из статуса «Новая». В контроллере проверяется `if application.status != Application.STATUS_NEW: return redirect(...)`.

3. **Вопрос:** Как разграничены права доступа гостей, клиентов и администратора?  
   **Ответ:** Гости проверяются через `not user.is_authenticated`, клиенты — через `@login_required`, администратор — через `@user_passes_test(is_admin)` с проверкой флагов `is_staff` / `is_superuser`.

4. **Вопрос:** Почему админка доступна по адресу `/superadmin`?  
   **Ответ:** Это прямое требование ТЗ раздела "Инструкция для студента". В корневом `urls.py` мы переопределили путь на `path('superadmin/', admin.site.urls)`.

5. **Вопрос:** Зачем папки в `media` разделены на `photos/` и `designs/`?  
   **Ответ:** Для разграничения входящих исходников клиентов (планов помещений до 2 Мб) и результатов работы дизайнеров студии (готовых визуализаций до 5 Мб).

6. **Вопрос:** Что такое `related_name` во внешнем ключе?  
   **Ответ:** Это имя обратной связи от целевой модели к исходной (например, `category.applications.all()`).

---
# Секция 4. Автоматизированное тестирование, запуск проекта и Полный сводный ТОП-25 вопросов

## 4.1. Автоматизированное тестирование (`catalog/tests.py`)
## 13. Шаг 11. Автоматизированное тестирование (`tests.py`)

Файл: [catalog/tests.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/tests.py).

Запуск тестов:
```powershell
python manage.py test
```
Результат выполнения:
```text
Creating test database for alias 'default'...
......
----------------------------------------------------------------------
Ran 6 tests in 10.995s

OK
Destroying test database for alias 'default'...
```
Все 6 тестов проверяют:
1. Валидацию ФИО, логина, совпадения паролей и согласия при регистрации.
2. Валидацию формата файла (.png разрешен, .txt блокируется) и авто-статус `Новая`.
3. Запрет на удаление заявки со статусом `Принято в работу`.
4. Обязательность комментария при взятии заявки в работу и запрет повторной смены статуса.
5. Каскадное удаление заявок при удалении категории.
6. Точность счетчика на главной и ограничение ровно в 4 выполненных проекта.

---

### Полный сплошной код пакета автоматизированных тестов:
Файл: [catalog/tests.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/tests.py)

### 8. `catalog/tests.py` (Полный код):
```python
import io
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User, Category, Application


def get_test_image(name='test.png', ext='PNG', size=(20, 20), color='blue'):
    buf = io.BytesIO()
    img = Image.new('RGB', size, color=color)
    img.save(buf, format=ext)
    return SimpleUploadedFile(name, buf.getvalue(), content_type=f'image/{ext.lower()}')


class DesignStudioTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Admin
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.ru',
            password='admin',
            fio='Администратор Главный'
        )
        # Regular user
        self.user = User.objects.create_user(
            username='petrov',
            email='petrov@test.ru',
            password='password123',
            fio='Петров Петр Петрович'
        )
        # Categories
        self.cat_3d = Category.objects.create(name='3D-дизайн')
        self.cat_sketch = Category.objects.create(name='Эскиз')

    def test_registration_validation(self):
        """Тест валидации регистрации пользователя"""
        # Невалидное ФИО (латиница)
        res = self.client.post(reverse('register'), {
            'fio': 'John Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'pass',
            'password_confirm': 'pass',
            'agree_data_processing': 'on'
        })
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res.context['form'], 'fio', 'ФИО может содержать только кириллические буквы, дефис и пробелы.')

        # Невалидный логин (кириллица)
        res = self.client.post(reverse('register'), {
            'fio': 'Иванов Иван',
            'username': 'иванов',
            'email': 'ivan@example.com',
            'password': 'pass',
            'password_confirm': 'pass',
            'agree_data_processing': 'on'
        })
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res.context['form'], 'username', 'Логин может содержать только латинские буквы и дефис.')

        # Несовпадение паролей
        res = self.client.post(reverse('register'), {
            'fio': 'Иванов Иван',
            'username': 'ivanov',
            'email': 'ivan@example.com',
            'password': 'pass1',
            'password_confirm': 'pass2',
            'agree_data_processing': 'on'
        })
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res.context['form'], 'password_confirm', 'Пароли не совпадают. Пожалуйста, повторите ввод.')

        # Успешная регистрация
        res = self.client.post(reverse('register'), {
            'fio': 'Сидоров Сидор',
            'username': 'sidorov',
            'email': 'sidorov@example.com',
            'password': 'sidorov-pass',
            'password_confirm': 'sidorov-pass',
            'agree_data_processing': 'on'
        })
        self.assertEqual(res.status_code, 302)
        self.assertTrue(User.objects.filter(username='sidorov').exists())

    def test_create_application_validation(self):
        """Тест создания заявки и валидации файла"""
        self.client.login(username='petrov', password='password123')

        # Запрещенный формат файла (.txt)
        bad_file = SimpleUploadedFile('plan.txt', b'file content', content_type='text/plain')
        res = self.client.post(reverse('application-create'), {
            'title': 'Гостиная',
            'description': 'Описание комнаты',
            'category': self.cat_3d.pk,
            'photo': bad_file
        })
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Application.objects.filter(title='Гостиная').exists())

        # Корректное фото (.png)
        good_file = get_test_image('plan.png', 'PNG')
        res = self.client.post(reverse('application-create'), {
            'title': 'Гостиная лофт',
            'description': 'Описание лофта',
            'category': self.cat_3d.pk,
            'photo': good_file
        })
        self.assertEqual(res.status_code, 302)
        app = Application.objects.get(title='Гостиная лофт')
        self.assertEqual(app.status, Application.STATUS_NEW)
        self.assertEqual(app.user, self.user)

    def test_delete_application_restrictions(self):
        """Тест удаления заявки: только со статусом 'Новая'"""
        self.client.login(username='petrov', password='password123')
        good_file = get_test_image('p.png', 'PNG')

        # Заявка 1: Новая (удаление разрешено)
        app_new = Application.objects.create(
            user=self.user,
            title='Заявка новая',
            description='Тест',
            category=self.cat_3d,
            photo=good_file,
            status=Application.STATUS_NEW
        )
        # Заявка 2: В работе (удаление запрещено)
        app_progress = Application.objects.create(
            user=self.user,
            title='Заявка в работе',
            description='Тест',
            category=self.cat_3d,
            photo=good_file,
            status=Application.STATUS_IN_PROGRESS
        )

        # Пытаемся удалить заявку в работе
        res = self.client.post(reverse('application-delete', args=[app_progress.pk]))
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Application.objects.filter(pk=app_progress.pk).exists())

        # Удаляем новую заявку
        res = self.client.post(reverse('application-delete', args=[app_new.pk]))
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Application.objects.filter(pk=app_new.pk).exists())

    def test_admin_status_transitions(self):
        """Тест смены статусов администратором"""
        self.client.login(username='admin', password='admin')
        good_file = get_test_image('p.png', 'PNG')
        app = Application.objects.create(
            user=self.user,
            title='Тест статуса',
            description='Тест',
            category=self.cat_3d,
            photo=good_file,
            status=Application.STATUS_NEW
        )

        # 1. Новая -> В работу без комментария (должна быть ошибка)
        res = self.client.post(reverse('admin-status-in-progress', args=[app.pk]), {'comment': ''})
        app.refresh_from_db()
        self.assertEqual(app.status, Application.STATUS_NEW)

        # 2. Новая -> В работу с комментарием
        res = self.client.post(reverse('admin-status-in-progress', args=[app.pk]), {'comment': 'Взят в работу дизайнером'})
        app.refresh_from_db()
        self.assertEqual(app.status, Application.STATUS_IN_PROGRESS)
        self.assertEqual(app.comment, 'Взят в работу дизайнером')

        # 3. Попытка изменить статус, когда заявка уже 'in_progress' (должна блокироваться)
        res = self.client.post(reverse('admin-status-in-progress', args=[app.pk]), {'comment': 'Новый коммент'})
        app.refresh_from_db()
        self.assertEqual(app.comment, 'Взят в работу дизайнером')

    def test_category_cascade_delete(self):
        """Тест: при удалении категории каскадно удаляются все её заявки"""
        self.client.login(username='admin', password='admin')
        good_file = get_test_image('p.png', 'PNG')
        cat = Category.objects.create(name='Временная категория')
        app = Application.objects.create(
            user=self.user,
            title='Заявка для удаления',
            description='Удалить',
            category=cat,
            photo=good_file
        )

        self.assertEqual(cat.applications.count(), 1)
        res = self.client.post(reverse('admin-delete-category', args=[cat.pk]))
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Category.objects.filter(pk=cat.pk).exists())
        self.assertFalse(Application.objects.filter(pk=app.pk).exists())

    def test_main_page_counter_and_limit(self):
        """Тест главной страницы: счетчик в работе и ограничение до 4 выполненных заявок"""
        good_file = get_test_image('p.png', 'PNG')

        # Создаем 3 заявки в работе
        for i in range(3):
            Application.objects.create(
                user=self.user,
                title=f'В работе {i}',
                description='desc',
                category=self.cat_3d,
                photo=good_file,
                status=Application.STATUS_IN_PROGRESS
            )

        # Создаем 6 выполненных заявок
        for i in range(6):
            Application.objects.create(
                user=self.user,
                title=f'Выполнено {i}',
                description='desc',
                category=self.cat_3d,
                photo=good_file,
                status=Application.STATUS_COMPLETED
            )

        res = self.client.get(reverse('index'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['in_progress_count'], 3)
        self.assertEqual(len(res.context['completed_apps']), 4)

```

---

---

## 4.2. Инструкция по развертыванию и запуску сервера

### 1. Выполнение миграций:
```powershell
& "C:\Users\fer\PycharmProjects\YP_DJANGO_3\.venv\Scripts\python.exe" "C:\Users\fer\PycharmProjects\YP_DJANGO_3\design_studio\manage.py" makemigrations
& "C:\Users\fer\PycharmProjects\YP_DJANGO_3\.venv\Scripts\python.exe" "C:\Users\fer\PycharmProjects\YP_DJANGO_3\design_studio\manage.py" migrate
```

### 2. Запуск полного пакета модульных тестов:
```powershell
& "C:\Users\fer\PycharmProjects\YP_DJANGO_3\.venv\Scripts\python.exe" "C:\Users\fer\PycharmProjects\YP_DJANGO_3\design_studio\manage.py" test catalog.tests -v 2
```
*Результат: `Ran 6 tests in ...s — OK`*.

### 3. Запуск сервера разработки на регламентном порту 8089:
```powershell
& "C:\Users\fer\PycharmProjects\YP_DJANGO_3\.venv\Scripts\python.exe" "C:\Users\fer\PycharmProjects\YP_DJANGO_3\design_studio\manage.py" runserver 8089
```

---

## 4.3. Таблица учетных записей для демонстрации и защиты

| Роль | Логин | Пароль | ФИО | Доступные разделы |
| :--- | :--- | :--- | :--- | :--- |
| **Главный Администратор** | `admin` | `admin` | Главный Администратор | `/admin-panel/`<br>`/superadmin/`<br>`/` |
| **Клиент дизайн-студии** | `ivanov` | `ivanov123` | Иванов Иван Иванович | `/cabinet/`<br>`/application/create/`<br>`/` |

---

## 4.4. Полный сводный ТОП-25 вопросов и эталонных ответов для защиты
*(Единый справочник для экспресс-подготовки перед экзаменационной комиссией)*

## 14. Шаг 12. ТОП-25 вопросов и эталонных ответов для защиты

1. **Вопрос:** Что такое MVT в Django и чем отличается от MVC?  
   **Ответ:** MVT — это разновидность MVC. Model отвечает за базу данных и ORM, View играет роль Контроллера (обрабатывает запрос и применяет логику), а Template выполняет роль View (отображает данные в HTML).

2. **Вопрос:** Почему мы создали кастомную модель `User` через `AbstractUser`?  
   **Ответ:** Это позволило добавить обязательное поле ФИО в саму таблицу пользователей. Это быстрее и архитектурно правильнее, чем делать дополнительную таблицу `Profile` через `OneToOneField`, требующую постоянных SQL `JOIN`.

3. **Вопрос:** Как обеспечивается уникальность логина?  
   **Ответ:** На уровне БД ограничением `UNIQUE` поля `username` и на уровне формы в методе `clean_username()`.

4. **Вопрос:** Где и как проверяется ограничение размера фото в 2 МБ?  
   **Ответ:** В функции-валидаторе `validate_photo_file` в `models.py`. Она проверяет `file.size > 2 * 1024 * 1024` и расширение файла. При несоответствии выбрасывается `ValidationError`.

5. **Вопрос:** Что происходит с заявками при удалении категории?  
   **Ответ:** В модели `Application` в поле `category` указано `on_delete=models.CASCADE`. База данных SQLite автоматически удаляет все связанные с этой категорией заявки.

6. **Вопрос:** Почему обычный пользователь не может удалить заявку в статусе «Принято в работу»?  
   **Ответ:** В представлении `delete_application_view` проверяется свойство `application.is_deletable` (`status == 'new'`). Если статус изменен, операция программно пресекается.

7. **Вопрос:** Как защищено удаление от подмены `id` в URL?  
   **Ответ:** Запрос выполняется через `get_object_or_404(Application, pk=pk, user=request.user)`. Запрос жестко привязан к текущему пользователю; попытка ввести чужой ID вернет ошибку 404.

8. **Вопрос:** Как устроен счетчик заявок в работе на главной?  
   **Ответ:** `Application.objects.filter(status='in_progress').count()` выполняет быстрый SQL-запрос `SELECT COUNT(*)`, не выгружая объекты в память.

9. **Вопрос:** Как ограничивается вывод не более 4 выполненных заявок на главной?  
   **Ответ:** Срез `[:4]` в QuerySet транслируется в SQL-директиву `LIMIT 4`.

10. **Вопрос:** Почему со статуса «В работе» или «Выполнено» нельзя сменить статус?  
    **Ответ:** Согласно ТЗ, смена разрешена только из статуса «Новая». В методе контроллера стоит условие `if application.status != Application.STATUS_NEW: return redirect(...)`.

11. **Вопрос:** Зачем нужен `{% csrf_token %}` в формах?  
    **Ответ:** Для защиты от межсайтовой подделки запросов (CSRF). Django сверяет криптографический токен формы с токеном в сессии.

12. **Вопрос:** Что делает `select_related('category')` в запросах?  
    **Ответ:** Это жадная загрузка (Eager Loading), которая объединяет таблицы через SQL `JOIN` и решает проблему «N+1 запросов».

13. **Вопрос:** Как разграничены права доступа гостей, клиентов и администратора?  
    **Ответ:** Гости проверяются через `not user.is_authenticated`, клиенты — через `@login_required`, администратор — через `@user_passes_test(is_admin)` с проверкой флагов `is_staff` / `is_superuser`.

14. **Вопрос:** Как работает фильтрация по статусу в кабинете?  
    **Ответ:** Через GET-параметр `?status=...`. Контроллер считывает параметр `request.GET.get('status')` и применяет `.filter(status=current_filter)`.

15. **Вопрос:** Почему админка доступна по адресу `/superadmin`?  
    **Ответ:** Это прямое требование ТЗ раздела "Инструкция для студента". В `urls.py` мы переопределили путь на `path('superadmin/', admin.site.urls)`.

16. **Вопрос:** В каком виде хранятся пароли в базе?  
    **Ответ:** В виде криптографического хеша алгоритма PBKDF2 с солью, сформированного методом `user.set_password()`.

17. **Вопрос:** Как Django раздает загруженные картинки при разработке?  
    **Ответ:** С помощью функции `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` в `urls.py` при `DEBUG = True`.

18. **Вопрос:** В чем разница между `makemigrations` и `migrate`?  
    **Ответ:** `makemigrations` создает файл описания изменений схемы, а `migrate` применяет их к таблицам базы данных.

19. **Вопрос:** Зачем папки в media разделены на `photos/` и `designs/`?  
    **Ответ:** Для разделения входящих исходников клиентов и результатов работы дизайнеров студии.

20. **Вопрос:** Как подсвечиваются поля с ошибками при регистрации?  
    **Ответ:** В шаблоне проверяется `{% if form.field.errors %}` и тегу `<input>` присваивается класс `is-invalid`, а под ним выводится `<div class="invalid-feedback">`.

21. **Вопрос:** Что такое `commit=False` в `form.save(commit=False)`?  
    **Ответ:** Создает экземпляр модели в памяти, не сохраняя его сразу в БД, чтобы мы могли программно привязать пользователя или статус (`application.user = request.user`).

22. **Вопрос:** Зачем нужен файл `manage.py`?  
    **Ответ:** Это скрипт командной строки для управления проектом (запуск сервера, миграции, тесты).

23. **Вопрос:** Что такое `related_name` во внешнем ключе?  
    **Ответ:** Это имя обратной связи от целевой модели к исходной (например, `category.applications.all()`).

24. **Вопрос:** Как работает библиотека Pillow в проекте?  
    **Ответ:** Pillow верифицирует графический поток байтов при сохранении `ImageField`, гарантируя, что под видом картинки не загружен исполняемый файл или скрипт.

25. **Вопрос:** Как запустить сервер на требуемом порту 8089?  
    **Ответ:** Командой `python manage.py runserver 8089`.


---

---

## 4.5. Инженерные приемы оптимизации интерфейса
### 10.6. Инженерные приемы облегчения интерфейса

Чтобы сделать интерфейс легким, быстрым и удобным для защиты перед комиссией:
1. **Исключение тяжелых фреймворков:** Мы не подключали React, Vue или громоздкие сборщики Webpack/Vite. Использован чистый легковесный CDN Bootstrap 5 (CSS + JS).
2. **Семантическая верстка:** Таблицы стилизованы классами `table-hover` и `align-middle`, обеспечивая идеальное выравнивание текста и миниатюр изображений по вертикали.
3. **Модальные окна на чистом Bootstrap:** Все диалоги подтверждения удаления и формы смены статусов работают на стандартных data-атрибутах Bootstrap (`data-bs-toggle="modal"`), не требуя ни строчки кастомного JavaScript.
4. **Легкие стили ([style.css](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/static/css/style.css)):**  
   Файл кастомных стилей сокращен до системного шрифтового стека `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto`, свойства `object-fit: cover` для картинок и базовых правил отображения ошибок, что гарантирует мгновенную загрузку страниц.

---

---

## 4.6. Итоговый чек-лист студента перед показом преподавателю

- [ ] **1. Запуск сервера:** Сервер запускается на `http://localhost:8089/`.
- [ ] **2. ПР №2.1 (Гость):**
  - [ ] Главная страница: отображается динамический счетчик заявок в работе; отображается не более 4 карточек выполненных работ с интерактивной сменой фото при наведении.
  - [ ] Регистрация (`/register/`): при попытке ввести английское ФИО или логин кириллицей поле подсвечивается красной рамкой `is-invalid` и выводится текст ошибки.
  - [ ] Регистрация: при успешной регистрации происходит автологин и мгновенный вход в личный кабинет.
  - [ ] Вход (`/login/`): клиент `ivanov` перенаправляется в `/cabinet/`; администратор `admin` — в `/admin-panel/`.
- [ ] **3. ПР №2.2 (Клиент):**
  - [ ] Подача заявки (`/application/create/`): при попытке загрузить файл больше 2 Мб или неподдерживаемый формат (`.pdf`, `.txt`) форма возвращает ошибку.
  - [ ] Заявка сохраняется со статусом «Новая» и прикрепляется к текущему пользователю.
  - [ ] Личный кабинет (`/cabinet/`): работают фильтры по статусам (Все, Новые, В работе, Выполненные).
  - [ ] Удаление заявки: кнопка удаления доступна ТОЛЬКО у заявок со статусом «Новая»; открывается экран подтверждения; после подтверждения заявка стирается.
  - [ ] Выход: кнопка «Выйти» завершает сессию.
- [ ] **4. ПР №2.3 (Администратор):**
  - [ ] Доступ: посторонний пользователь не может зайти в `/admin-panel/`.
  - [ ] Смена статуса: кнопка «В работу» требует комментарий; после перевода статус заявки нельзя изменить повторно.
  - [ ] Смена статуса: кнопка «Выполнено» требует обязательного файла дизайна до 5 Мб; файл сохраняется в `media/designs/`.
  - [ ] Категории: создание категории; каскадное удаление категории удаляет все привязанные к ней заявки.
  - [ ] Стандартная админка: доступна по адресу `http://localhost:8089/superadmin/`.
- [ ] **5. Тестирование:** Выполняется `python manage.py test` — все 6 тестов завершаются со статусом `OK`.
