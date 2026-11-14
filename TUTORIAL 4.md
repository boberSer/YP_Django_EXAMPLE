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
               │  • DOCTYPE, <head>, Pure Native CSS     │
               │  • Чистая навигационная панель          │
               │  • Блок flash-сообщений (messages)      │
               │                                         │
               │  ┌───────────────────────────────────┐  │
               │  │   {% block content %}{% endblock %}│  │  <-- «Посадочное место» для дочерних страниц
               │  └───────────────────────────────────┘  │
               │                                         │
               │  • Общий подвал (footer)                │
               │  • Нативный HTML5 <dialog> API          │
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
#### 1. [templates/base.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/base.html) — Базовый скелет и чистая навигация (Pure Native CSS)
- **Архитектура чистого CSS (100% Native, без Bootstrap):**  
  Из базового шаблона полностью исключены внешние CDN-зависимости (Bootstrap CSS, Bootstrap Icons, Bootstrap JS). Интерфейс построен на принципах бескомпромиссного брутализма и минимализма: строгая монохромная палитра, четкие рамки, моноширинный шрифт, полное отсутствие скруглений и теней.
- **Адаптивное меню навигации:**
  Контейнер `.site-header` и `.header-inner` используют Flexbox-раскладку без JavaScript:
  - Гость видит: логотип `DESIGN.PRO`, ссылку «Главная», кнопки `[ Вход ]` и `[ Регистрация ]`.
  - Авторизованный клиент видит: пункты «Мои заявки», «Создать заявку», блок профиля с логином/ФИО и кнопку `[ Выход ]`.
  - Администратор дополнительно видит: акцентную ссылку «Панель управления» и прямую ссылку в админку Django (`/superadmin/`).
- **Вывод Flash-сообщений (`messages`):**  
  Контейнер `.messages-container` отображает уведомления фреймворка `django.contrib.messages` (`alert-success`, `alert-danger`, `alert-info`) с нативной кнопкой закрытия `[X]`, удаляющей блок через `this.parentElement.remove()` без библиотек.
- **Липкий подвал (Sticky Footer на Flexbox):**  
  Тело документа `body` имеет стили `display: flex; flex-direction: column; min-height: 100vh;`, а контейнер `main` занимает всё свободное пространство (`flex-grow: 1`), прижимая `.site-footer` к низу окна при любом объеме контента.

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
    <!-- Чистый CSS без Bootstrap -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>

<!-- Шапка и главное меню -->
<header class="site-header">
    <div class="container header-inner">
        <a class="site-logo" href="{% url 'index' %}">Design.pro</a>

        <nav class="main-nav">
            <a class="nav-link {% if request.resolver_match.url_name == 'index' %}active{% endif %}"
               href="{% url 'index' %}">Главная</a>
            {% if user.is_authenticated %}
                <a class="nav-link {% if request.resolver_match.url_name == 'cabinet' %}active{% endif %}"
                   href="{% url 'cabinet' %}">Мои заявки</a>
                <a class="nav-link {% if request.resolver_match.url_name == 'application-create' %}active{% endif %}"
                   href="{% url 'application-create' %}">Создать заявку</a>
                {% if user.is_staff or user.is_superuser %}
                    <a class="nav-link admin-link {% if request.resolver_match.url_name == 'admin_panel' %}active{% endif %}"
                       href="{% url 'admin_panel' %}">Панель управления</a>
                    <a class="nav-link superadmin-link" href="/superadmin/" target="_blank">Superadmin</a>
                {% endif %}
            {% endif %}
        </nav>

        <div class="user-block">
            {% if user.is_authenticated %}
                <span class="user-info">
                        {{ user.username }}{% if user.fio %} ({{ user.fio }}){% endif %}
                    </span>
                <a href="{% url 'logout' %}" class="btn btn-sm btn-danger">Выход</a>
            {% else %}
                <a href="{% url 'login' %}" class="btn btn-sm">Вход</a>
                <a href="{% url 'register' %}" class="btn btn-sm">Регистрация</a>
            {% endif %}
        </div>
    </div>
</header>

<!-- Сообщения системы -->
<div class="container messages-container">
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{% if message.tags == 'error' %}danger{% else %}{{ message.tags }}{% endif %}">
                <span>{{ message }}</span>
                <button type="button" class="alert-close" onclick="this.parentElement.remove()" title="Закрыть">Закрыть</button>
            </div>
        {% endfor %}
    {% endif %}
</div>

<!-- Основной контент страницы -->
<main class="container main-content">
    {% block content %}{% endblock %}
</main>

<!-- Подвал сайта -->
<footer class="site-footer">
    <div class="container footer-inner">
        <span>© 2026 Студия дизайна интерьеров <strong>Design.pro</strong></span>
        <span>Порт: <strong>8089</strong> | Админка Django: <a href="/superadmin" target="_blank">/superadmin</a></span>
    </div>
</footer>

</body>
</html>
```

#### Полный код `static/css/style.css` (Чистый CSS без Bootstrap):
Файл: [static/css/style.css](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/static/css/style.css)

> **Основные блоки стилей:**
> 1. Базовые стили (`body`, шрифты, ссылки, контейнер `.container`).
> 2. Шапка сайта и меню (`.site-header`, `.site-logo`, `.nav-link`, `.user-block`).
> 3. Кнопки (`.btn`, `.btn-primary`, `.btn-danger`, `.btn-success`).
> 4. Карточки и промо-блок (`.box`, `.hero-box`, счетчик заявок `.counter-box`, карточки проектов `.project-card`).
> 5. Фильтрация и таблицы данных (`.filter-group`, `.table-wrap`, `table`, статусные бейджи `.badge`).
> 6. Формы и подсветка валидации (`.form-box`, `input`, `textarea`, `.is-invalid`, `.field-error`).
> 7. Системные уведомления (`.alert`) и нативные модальные окна (`dialog`).
> 8. Подвал сайта (`.site-footer`).

### 9. `static/css/style.css` (Структурированный чистый CSS):
```css
/* Основные стили сайта Design.pro */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    border-radius: 0 !important;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f4f6f9;
    color: #212529;
    line-height: 1.5;
    font-size: 14px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

a {
    color: #0d6efd;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

img {
    max-width: 100%;
    height: auto;
}

.container {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 15px;
}

.main-content {
    flex-grow: 1;
    padding-bottom: 30px;
}

/* Шапка сайта и меню */
.site-header {
    background: #ffffff;
    border-bottom: 1px solid #dee2e6;
    padding: 12px 0;
    margin-bottom: 25px;
}

.header-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.site-logo {
    font-size: 18px;
    font-weight: bold;
    color: #212529;
    text-decoration: none;
}

.site-logo:hover {
    text-decoration: none;
    color: #212529;
}

.main-nav {
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
}

.nav-link {
    color: #212529;
    padding: 6px 12px;
    font-size: 13px;
    text-decoration: none;
    border: 1px solid #ced4da;
    background-color: #ffffff;
}

.nav-link:hover {
    background-color: #e9ecef;
    color: #212529;
    text-decoration: none;
}

.nav-link.active {
    background-color: #e9ecef;
    color: #212529;
    font-weight: bold;
}

.nav-link.admin-link,
.superadmin-link {
    color: #212529;
    border: 1px solid #ced4da;
    background-color: #ffffff;
}

.user-block {
    display: flex;
    align-items: center;
    gap: 10px;
}

.user-info {
    font-size: 13px;
    color: #495057;
    background: #e9ecef;
    padding: 6px 10px;
    border: 1px solid #ced4da;
}

/* Кнопки */
.btn,
button,
input[type="submit"],
input[type="button"] {
    display: inline-block;
    padding: 6px 12px;
    font-size: 13px;
    font-family: inherit;
    border: 1px solid #ced4da;
    background: #ffffff;
    color: #212529;
    cursor: pointer;
    text-decoration: none;
    vertical-align: middle;
}

.btn:hover,
button:hover,
input[type="submit"]:hover {
    background: #e9ecef;
    text-decoration: none;
}

.btn-primary {
    background: #0d6efd;
    border-color: #0d6efd;
    color: #ffffff !important;
}

.btn-primary:hover {
    background: #0b5ed7;
    border-color: #0a58ca;
    color: #ffffff !important;
}

.btn-danger {
    background: #dc3545;
    border-color: #dc3545;
    color: #ffffff !important;
}

.btn-danger:hover {
    background: #bb2d3b;
    border-color: #b02a37;
    color: #ffffff !important;
}

.btn-success {
    background: #198754;
    border-color: #198754;
    color: #ffffff !important;
}

.btn-success:hover {
    background: #157347;
    border-color: #146c43;
    color: #ffffff !important;
}

.btn-sm {
    padding: 3px 8px;
    font-size: 12px;
}

.btn-in-progress {
    color: #055160;
    border-color: #b6effb;
    background-color: #cff4fc;
}

.btn-in-progress:hover {
    background-color: #b6effb;
}

.btn-full {
    width: 100%;
    padding: 10px;
}

/* Блоки и карточки */
.box {
    background: #ffffff;
    border: 1px solid #dee2e6;
    padding: 20px;
    margin-bottom: 25px;
}

.box-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
}

.box-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 15px;
}

.box-subtitle {
    font-size: 13px;
    color: #6c757d;
    margin-top: 2px;
}

/* Промо-блок главной страницы */
.hero-box {
    background: #ffffff;
    border: 1px solid #dee2e6;
    padding: 25px;
    margin-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
}

.hero-content {
    flex: 1 1 500px;
}

.hero-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
}

.hero-desc {
    color: #6c757d;
    margin-bottom: 15px;
    font-size: 14px;
}

.hero-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

/* Счетчик заявок в работе */
.counter-box {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    padding: 20px;
    text-align: center;
    min-width: 240px;
}

.counter-label {
    font-size: 12px;
    font-weight: bold;
    color: #6c757d;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.counter-number {
    font-size: 42px;
    font-weight: bold;
    color: #0d6efd;
    margin: 5px 0;
    line-height: 1;
}

.counter-caption {
    font-size: 12px;
    color: #6c757d;
}

/* Сетка карточек проектов */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 15px;
    margin-top: 15px;
}

.project-card {
    background: #ffffff;
    border: 1px solid #dee2e6;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.project-card img {
    width: 100%;
    height: 160px;
    object-fit: cover;
    display: block;
    background: #e9ecef;
}

.project-placeholder {
    width: 100%;
    height: 160px;
    background: #e9ecef;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #6c757d;
    font-size: 13px;
}

.project-body {
    padding: 12px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.project-title {
    font-size: 15px;
    font-weight: bold;
    margin: 6px 0 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.project-desc {
    font-size: 12px;
    color: #6c757d;
    margin-bottom: 10px;
    flex-grow: 1;
}

.project-date {
    font-size: 11px;
    color: #adb5bd;
    border-top: 1px solid #f1f3f5;
    padding-top: 6px;
}

/* Фильтры */
.filter-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}

.filter-label {
    font-size: 12px;
    font-weight: 600;
    color: #6c757d;
}

.filter-group {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
}

.filter-btn {
    padding: 5px 10px;
    font-size: 12px;
    background: #e9ecef;
    color: #495057;
    text-decoration: none;
    font-weight: 500;
}

.filter-btn:hover {
    background: #dee2e6;
    text-decoration: none;
}

.filter-btn.active {
    background: #0d6efd;
    color: #ffffff;
}

/* Таблицы */
.table-wrap {
    width: 100%;
    overflow-x: auto;
    border: 1px solid #dee2e6;
    background: #ffffff;
    margin: 15px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

th, td {
    padding: 10px 12px;
    border-bottom: 1px solid #dee2e6;
    vertical-align: middle;
    text-align: left;
}

th {
    background: #f8f9fa;
    font-weight: 600;
    color: #495057;
}

tr:hover td {
    background: #f8f9fa;
}

.col-date {
    width: 120px;
}

.col-category {
    width: 130px;
}

.col-thumb {
    width: 70px;
}

.col-status {
    width: 140px;
}

.col-action {
    text-align: right;
    width: 120px;
}

.col-date-text {
    white-space: nowrap;
    color: #6c757d;
    font-size: 12px;
}

.col-action-cell {
    text-align: right;
    white-space: nowrap;
}

.app-title {
    font-weight: 600;
    color: #212529;
}

.app-desc {
    color: #495057;
    font-size: 12px;
    margin-top: 3px;
    max-width: 260px;
}

.app-thumb {
    width: 44px;
    height: 44px;
    object-fit: cover;
    border: 1px solid #dee2e6;
    display: block;
}

.table-thumb-cell {
    display: flex;
    gap: 4px;
}

.plan-thumb {
    width: 38px;
    height: 38px;
    object-fit: cover;
    border: 1px solid #dee2e6;
    display: block;
}

.design-thumb {
    width: 38px;
    height: 38px;
    object-fit: cover;
    border: 2px solid #198754;
    display: block;
}

.comment-text {
    font-size: 12px;
    color: #055160;
}

.completed-reply {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
}

.comment-note {
    font-size: 11px;
    color: #495057;
}

/* Бейджи */
.badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 600;
}

.badge-new {
    background: #fff3cd;
    color: #856404;
    border: 1px solid #ffeeba;
}

.badge-in_progress,
.badge-progress {
    background: #cff4fc;
    color: #055160;
    border: 1px solid #b6effb;
}

.badge-completed {
    background: #d1e7dd;
    color: #0f5132;
    border: 1px solid #badbcc;
}

.badge-category {
    background: #e9ecef;
    color: #495057;
}

/* Формы */
.form-box {
    max-width: 520px;
    margin: 30px auto;
    background: #ffffff;
    border: 1px solid #dee2e6;
    padding: 25px;
}

.form-header {
    text-align: center;
    margin-bottom: 20px;
}

.form-back-link {
    margin-bottom: 12px;
    text-align: left;
}

.form-back-link a {
    color: #0d6efd;
    font-size: 13px;
    text-decoration: underline;
}

.form-back-link a:hover {
    color: #0a58ca;
}

.form-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 4px;
}

.form-group {
    margin-bottom: 15px;
}

label,
.form-label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 5px;
}

input[type="text"],
input[type="password"],
input[type="email"],
input[type="file"],
textarea,
select,
.form-control,
.form-select {
    width: 100%;
    padding: 8px 10px;
    border: 1px solid #ced4da;
    font-size: 13px;
    font-family: inherit;
    background: #ffffff;
    color: #212529;
}

input:focus,
textarea:focus,
select:focus {
    border-color: #86b7fe;
    outline: 0;
}

.is-invalid {
    border-color: #dc3545 !important;
    background-color: #fff8f8;
}

.field-error,
.invalid-feedback {
    color: #dc3545;
    font-size: 12px;
    margin-top: 4px;
    display: block;
}

.field-help,
.form-text {
    color: #6c757d;
    font-size: 11px;
    margin-top: 3px;
    display: block;
}

.checkbox-group {
    display: flex;
    gap: 8px;
    align-items: center;
    margin: 15px 0;
}

.checkbox-group input[type="checkbox"] {
    width: 16px;
    height: 16px;
}

.checkbox-group label {
    margin: 0;
    font-weight: normal;
    font-size: 13px;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.form-submit {
    margin-top: 20px;
}

.credentials-hint {
    margin-top: 15px;
    padding: 12px;
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    font-size: 12px;
    color: #495057;
}

.form-footer-link {
    text-align: center;
    font-size: 13px;
    border-top: 1px solid #dee2e6;
    padding-top: 15px;
    margin-top: 20px;
}

/* Пустые состояния */
.empty-state {
    padding: 30px;
    text-align: center;
    color: #6c757d;
    background: #f8f9fa;
}

.empty-state-text {
    margin-bottom: 12px;
}

/* Админ панель */
.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 20px;
}

.admin-subtitle {
    font-size: 13px;
    color: #6c757d;
    margin-top: 2px;
}

.cat-manage-grid {
    display: grid;
    grid-template-columns: 1fr 1.6fr;
    gap: 20px;
    align-items: start;
}

.cat-add-form {
    display: flex;
    gap: 8px;
}

.cat-add-input {
    flex-grow: 1;
}

.cat-list-title {
    font-size: 12px;
    font-weight: 600;
    color: #6c757d;
    margin-bottom: 8px;
}

.cat-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.cat-tag {
    background: #e9ecef;
    border: 1px solid #dee2e6;
    padding: 4px 8px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
}

.cat-del-btn {
    padding: 2px 6px;
    font-size: 11px;
}

/* Сообщения / Alerts */
.messages-container {
    margin-bottom: 15px;
}

.alert {
    padding: 10px 15px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid transparent;
    font-size: 13px;
}

.alert-success {
    background: #d1e7dd;
    color: #0f5132;
    border-color: #badbcc;
}

.alert-danger,
.alert-error {
    background: #f8d7da;
    color: #842029;
    border-color: #f5c2c7;
}

.alert-warning {
    background: #fff3cd;
    color: #664d03;
    border-color: #ffecb5;
}

.alert-info {
    background: #cff4fc;
    color: #055160;
    border-color: #b6effb;
}

.alert-close {
    background: none;
    border: none;
    font-size: 12px;
    cursor: pointer;
    color: inherit;
    text-decoration: underline;
}

.alert-close:hover {
    opacity: 0.8;
}

/* Диалоги (HTML5 dialog) */
dialog {
    background: #ffffff;
    border: 1px solid #dee2e6;
    padding: 20px;
    max-width: 450px;
    width: 90%;
    margin: auto;
}

dialog::backdrop {
    background: rgba(0, 0, 0, 0.4);
}

.dialog-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #dee2e6;
}

.dialog-message {
    margin-bottom: 12px;
    font-size: 14px;
}

.dialog-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px solid #dee2e6;
}

.inline-form {
    display: inline;
}

.confirm-box {
    text-align: center;
    max-width: 480px;
}

.confirm-actions {
    display: flex;
    justify-content: center;
    gap: 12px;
}

/* Подвал */
.site-footer {
    background: #ffffff;
    border-top: 1px solid #dee2e6;
    padding: 15px 0;
    margin-top: auto;
    font-size: 12px;
    color: #6c757d;
}

.footer-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}

/* Вспомогательные классы */
.text-danger {
    color: #dc3545 !important;
}

.text-success {
    color: #198754 !important;
}

.text-muted {
    color: #6c757d !important;
}

.text-center {
    text-align: center !important;
}

.text-end {
    text-align: right !important;
}

.fw-bold {
    font-weight: bold !important;
}

.small {
    font-size: 12px !important;
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
<!-- Информационный промо-блок студии -->
<div class="hero-box">
    <div class="hero-content">
        <h1 class="hero-title">
            Студия интерьеров «Design.pro»
        </h1>
        <p class="hero-desc">
            Проектирование и создание вариантов оформления интерьеров жилых помещений. Загрузите план вашего помещения, и дизайнеры подготовят индивидуальный проект.
        </p>
        <div class="hero-actions">
            {% if user.is_authenticated %}
                <a href="{% url 'application-create' %}" class="btn btn-primary">Создать заявку</a>
                <a href="{% url 'cabinet' %}" class="btn">Мои заявки</a>
            {% else %}
                <a href="{% url 'register' %}" class="btn btn-primary">Регистрация</a>
                <a href="{% url 'login' %}" class="btn">Вход в кабинет</a>
            {% endif %}
        </div>
    </div>

    <!-- Счетчик по ТЗ: Количество заявок в статусе "Принято в работу" -->
    <div class="counter-box">
        <div class="counter-label">Заявок в работе сейчас</div>
        <div class="counter-number" id="in-progress-counter">{{ in_progress_count }}</div>
        <div class="counter-caption">В статусе «Принято в работу»</div>
    </div>
</div>

<!-- Раздел: Последние выполненные проекты (не более 4) -->
<div class="box">
    <h2 class="box-title">Последние выполненные проекты</h2>

    {% if completed_apps %}
        <div class="cards-grid">
            {% for app in completed_apps %}
                <div class="project-card">
                    <!-- Фотография дизайна или плана по ТЗ -->
                    {% if app.design_image %}
                        <img src="{{ app.design_image.url }}" alt="{{ app.title }}">
                    {% elif app.photo %}
                        <img src="{{ app.photo.url }}" alt="{{ app.title }}">
                    {% else %}
                        <div class="project-placeholder">
                            Изображение отсутствует
                        </div>
                    {% endif %}

                    <div class="project-body">
                        <div>
                            <span class="badge badge-category">{{ app.category.name }}</span>
                        </div>

                        <div class="project-title" title="{{ app.title }}">
                            {{ app.title }}
                        </div>

                        <div class="project-desc">
                            {{ app.description }}
                        </div>

                        <div class="project-date">
                            {{ app.created_at|date:"d.m.Y H:i" }}
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="empty-state">
            Пока нет выполненных проектов со статусом «Выполнено».
        </div>
    {% endif %}
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
<div class="form-box">
    <div class="form-header">
        <h2 class="form-title">Регистрация в Design.pro</h2>
        <div class="field-help">Заполните поля для создания учетной записи пользователя</div>
    </div>

    <form method="post" novalidate>
        {% csrf_token %}

        {% if form.non_field_errors %}
            <div class="alert alert-danger">
                {% for error in form.non_field_errors %}
                    <div>{{ error }}</div>
                {% endfor %}
            </div>
        {% endif %}

        <!-- ФИО -->
        <div class="form-group">
            <label for="{{ form.fio.id_for_label }}">
                {{ form.fio.label }} <span class="text-danger">*</span>
            </label>
            <input type="text"
                   name="{{ form.fio.html_name }}"
                   id="{{ form.fio.id_for_label }}"
                   value="{{ form.fio.value|default:'' }}"
                   class="{% if form.fio.errors %}is-invalid{% endif %}"
                   placeholder="Иванов Иван Иванович"
                   required>
            <div class="field-help">Только кириллические буквы, дефис и пробелы</div>
            {% if form.fio.errors %}
                <div class="field-error">
                    {% for error in form.fio.errors %}{{ error }}{% endfor %}
                </div>
            {% endif %}
        </div>

        <!-- Логин -->
        <div class="form-group">
            <label for="{{ form.username.id_for_label }}">
                {{ form.username.label }} <span class="text-danger">*</span>
            </label>
            <input type="text"
                   name="{{ form.username.html_name }}"
                   id="{{ form.username.id_for_label }}"
                   value="{{ form.username.value|default:'' }}"
                   class="{% if form.username.errors %}is-invalid{% endif %}"
                   placeholder="ivanov-ivan"
                   required>
            <div class="field-help">Только латинские буквы и дефис, уникальный</div>
            {% if form.username.errors %}
                <div class="field-error">
                    {% for error in form.username.errors %}{{ error }}{% endfor %}
                </div>
            {% endif %}
        </div>

        <!-- Email -->
        <div class="form-group">
            <label for="{{ form.email.id_for_label }}">
                {{ form.email.label }} <span class="text-danger">*</span>
            </label>
            <input type="email"
                   name="{{ form.email.html_name }}"
                   id="{{ form.email.id_for_label }}"
                   value="{{ form.email.value|default:'' }}"
                   class="{% if form.email.errors %}is-invalid{% endif %}"
                   placeholder="ivanov@example.com"
                   required>
            {% if form.email.errors %}
                <div class="field-error">
                    {% for error in form.email.errors %}{{ error }}{% endfor %}
                </div>
            {% endif %}
        </div>

        <!-- Пароль -->
        <div class="form-group">
            <label for="{{ form.password.id_for_label }}">
                {{ form.password.label }} <span class="text-danger">*</span>
            </label>
            <input type="password"
                   name="{{ form.password.html_name }}"
                   id="{{ form.password.id_for_label }}"
                   class="{% if form.password.errors %}is-invalid{% endif %}"
                   placeholder="Введите пароль"
                   required>
            {% if form.password.errors %}
                <div class="field-error">
                    {% for error in form.password.errors %}{{ error }}{% endfor %}
                </div>
            {% endif %}
        </div>

        <!-- Повтор пароля -->
        <div class="form-group">
            <label for="{{ form.password_confirm.id_for_label }}">
                {{ form.password_confirm.label }} <span class="text-danger">*</span>
            </label>
            <input type="password"
                   name="{{ form.password_confirm.html_name }}"
                   id="{{ form.password_confirm.id_for_label }}"
                   class="{% if form.password_confirm.errors %}is-invalid{% endif %}"
                   placeholder="Повторите пароль"
                   required>
            {% if form.password_confirm.errors %}
                <div class="field-error">
                    {% for error in form.password_confirm.errors %}{{ error }}{% endfor %}
                </div>
            {% endif %}
        </div>

        <!-- Согласие на обработку ПДн -->
        <div class="checkbox-group">
            <input type="checkbox"
                   name="{{ form.agree_data_processing.html_name }}"
                   id="{{ form.agree_data_processing.id_for_label }}"
                   class="{% if form.agree_data_processing.errors %}is-invalid{% endif %}"
                   {% if form.agree_data_processing.value %}checked{% endif %}
                   required>
            <label for="{{ form.agree_data_processing.id_for_label }}">
                Я даю согласие на обработку персональных данных <span class="text-danger">*</span>
            </label>
        </div>
        {% if form.agree_data_processing.errors %}
            <div class="field-error">
                {% for error in form.agree_data_processing.errors %}{{ error }}{% endfor %}
            </div>
        {% endif %}

        <div class="form-submit">
            <button type="submit" class="btn btn-primary btn-full">
                Зарегистрироваться
            </button>
        </div>
    </form>

    <div class="form-footer-link">
        Уже зарегистрированы? <a href="{% url 'login' %}" class="fw-bold">Войти в аккаунт</a>
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
<div class="form-box">
    <div class="form-header">
        <h2 class="form-title">Авторизация</h2>
        <div class="field-help">Введите ваш логин и пароль для входа в систему</div>
    </div>

    <form method="post" novalidate>
        {% csrf_token %}

        {% if form.non_field_errors %}
            <div class="alert alert-danger">
                {% for error in form.non_field_errors %}
                    <div>{{ error }}</div>
                {% endfor %}
            </div>
        {% endif %}

        <div class="form-group">
            <label for="{{ form.username.id_for_label }}">
                Логин <span class="text-danger">*</span>
            </label>
            <input type="text"
                   name="{{ form.username.html_name }}"
                   id="{{ form.username.id_for_label }}"
                   value="{{ form.username.value|default:'' }}"
                   class="{% if form.username.errors or form.non_field_errors %}is-invalid{% endif %}"
                   placeholder="Введите логин"
                   required autofocus>
            {% if form.username.errors %}
                <div class="field-error">
                    {% for error in form.username.errors %}{{ error }}{% endfor %}
                </div>
            {% endif %}
        </div>

        <div class="form-group">
            <label for="{{ form.password.id_for_label }}">
                Пароль <span class="text-danger">*</span>
            </label>
            <input type="password"
                   name="{{ form.password.html_name }}"
                   id="{{ form.password.id_for_label }}"
                   class="{% if form.password.errors or form.non_field_errors %}is-invalid{% endif %}"
                   placeholder="Введите пароль"
                   required>
            {% if form.password.errors %}
                <div class="field-error">
                    {% for error in form.password.errors %}{{ error }}{% endfor %}
                </div>
            {% endif %}
        </div>

        <div class="form-submit">
            <button type="submit" class="btn btn-primary btn-full">
                Войти в систему
            </button>
        </div>
    </form>

    <div class="credentials-hint">
        <strong>Данные администратора:</strong><br>
        логин: <code>admin</code>, пароль: <code>admin</code>
    </div>

    <div class="form-footer-link">
        Еще нет аккаунта? <a href="{% url 'register' %}" class="fw-bold">Зарегистрироваться</a>
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
<div class="box">
    <!-- Верхний блок: заголовок -->
    <div class="box-header">
        <div>
            <h2 class="box-title">Мои заявки на дизайн</h2>
            <div class="box-subtitle">
                Пользователь: <b>{{ user.fio|default:user.username }}</b>
            </div>
        </div>
    </div>

    <!-- Фильтрация по статусу -->
    <div class="filter-bar">
        <span class="filter-label">Фильтр:</span>
        <div class="filter-group">
            <a href="{% url 'cabinet' %}?status=all" class="filter-btn {% if current_filter == 'all' or not current_filter %}active{% endif %}">
                Все ({{ total_count }})
            </a>
            <a href="{% url 'cabinet' %}?status=new" class="filter-btn {% if current_filter == 'new' %}active{% endif %}">
                Новые ({{ new_count }})
            </a>
            <a href="{% url 'cabinet' %}?status=in_progress" class="filter-btn {% if current_filter == 'in_progress' %}active{% endif %}">
                В работе ({{ in_progress_count }})
            </a>
            <a href="{% url 'cabinet' %}?status=completed" class="filter-btn {% if current_filter == 'completed' %}active{% endif %}">
                Выполненные ({{ completed_count }})
            </a>
        </div>
    </div>

    <!-- Таблица заявок -->
    {% if applications %}
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th class="col-date">Дата</th>
                        <th>Название и описание</th>
                        <th class="col-category">Категория</th>
                        <th class="col-thumb">План</th>
                        <th class="col-status">Статус</th>
                        <th>Ответ студии</th>
                        <th class="col-action">Действие</th>
                    </tr>
                </thead>
                <tbody>
                    {% for app in applications %}
                        <tr>
                            <!-- Временная метка по ТЗ -->
                            <td class="col-date-text">
                                {{ app.created_at|date:"d.m.Y H:i" }}
                            </td>

                            <!-- Название и описание по ТЗ -->
                            <td>
                                <div class="app-title">{{ app.title }}</div>
                                <div class="app-desc">{{ app.description }}</div>
                            </td>

                            <!-- Категория заявки по ТЗ -->
                            <td>
                                <span class="badge badge-category">{{ app.category.name }}</span>
                            </td>

                            <!-- Фото помещения -->
                            <td>
                                {% if app.photo %}
                                    <a href="{{ app.photo.url }}" target="_blank">
                                        <img src="{{ app.photo.url }}" alt="План" class="app-thumb">
                                    </a>
                                {% else %}
                                    <span class="text-muted">—</span>
                                {% endif %}
                            </td>

                            <!-- Статус заявки по ТЗ -->
                            <td>
                                {% if app.status == 'new' %}
                                    <span class="badge badge-new">Новая</span>
                                {% elif app.status == 'in_progress' %}
                                    <span class="badge badge-progress">Принято в работу</span>
                                {% elif app.status == 'completed' %}
                                    <span class="badge badge-completed">Выполнено</span>
                                {% endif %}
                            </td>

                            <!-- Ответ студии (комментарий или дизайн) -->
                            <td>
                                {% if app.status == 'in_progress' and app.comment %}
                                    <div class="comment-text"><strong>Комментарий:</strong> {{ app.comment }}</div>
                                {% elif app.status == 'completed' %}
                                    <div class="completed-reply">
                                        {% if app.design_image %}
                                            <a href="{{ app.design_image.url }}" target="_blank" class="btn btn-sm btn-success">Дизайн</a>
                                        {% endif %}
                                        {% if app.comment %}
                                            <span class="comment-note">{{ app.comment }}</span>
                                        {% endif %}
                                    </div>
                                {% else %}
                                    <span class="text-muted">—</span>
                                {% endif %}
                            </td>

                            <!-- Кнопка удаления (только если статус Новая) -->
                            <td class="col-action-cell">
                                {% if app.is_deletable %}
                                    <button type="button" class="btn btn-danger btn-sm" onclick="document.getElementById('delModal{{ app.pk }}').showModal()">
                                        Удалить
                                    </button>

                                    <!-- Нативный диалог подтверждения удаления -->
                                    <dialog id="delModal{{ app.pk }}">
                                        <div class="dialog-title text-danger">Подтверждение удаления</div>
                                        <p class="dialog-message">
                                            Вы действительно хотите удалить заявку:
                                            <br>
                                            <strong>«{{ app.title }}»</strong>?
                                        </p>
                                        <div class="alert alert-warning">
                                            Внимание: данное действие необратимо. Удаление доступно только для заявок со статусом «Новая».
                                        </div>
                                        <div class="dialog-actions">
                                            <button type="button" class="btn btn-sm" onclick="this.closest('dialog').close()">Отмена</button>
                                            <form method="post" action="{% url 'application-delete' app.pk %}" class="inline-form">
                                                {% csrf_token %}
                                                <button type="submit" class="btn btn-danger btn-sm">Да, удалить</button>
                                            </form>
                                        </div>
                                    </dialog>
                                {% else %}
                                    <span class="text-muted small">Недоступно</span>
                                {% endif %}
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <div class="empty-state">
            <p class="empty-state-text">Заявок с выбранным фильтром не найдено.</p>
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
<div class="form-box">
    <div class="form-header">
        <div class="form-back-link">
            <a href="{% url 'cabinet' %}">Назад к моим заявкам</a>
        </div>
        <h2 class="form-title">Новая заявка на дизайн</h2>
        <div class="field-help">Все поля обязательны для заполнения по ТЗ</div>
    </div>

    <form method="post" enctype="multipart/form-data" novalidate>
        {% csrf_token %}

        {% if form.non_field_errors %}
            <div class="alert alert-danger">
                {% for err in form.non_field_errors %}<div>{{ err }}</div>{% endfor %}
            </div>
        {% endif %}

        <!-- Название заявки -->
        <div class="form-group">
            <label>Название заявки <span class="text-danger">*</span></label>
            {{ form.title }}
            {% if form.title.errors %}
                <div class="field-error">{% for e in form.title.errors %}{{ e }}{% endfor %}</div>
            {% endif %}
        </div>

        <!-- Категория заявки -->
        <div class="form-group">
            <label>Категория помещения <span class="text-danger">*</span></label>
            {{ form.category }}
            {% if form.category.errors %}
                <div class="field-error">{% for e in form.category.errors %}{{ e }}{% endfor %}</div>
            {% endif %}
        </div>

        <!-- Описание заявки -->
        <div class="form-group">
            <label>Описание пожеланий к дизайну <span class="text-danger">*</span></label>
            {{ form.description }}
            {% if form.description.errors %}
                <div class="field-error">{% for e in form.description.errors %}{{ e }}{% endfor %}</div>
            {% endif %}
        </div>

        <!-- Фото помещения или его план -->
        <div class="form-group">
            <label>Фото помещения или план <span class="text-danger">*</span></label>
            {{ form.photo }}
            <div class="field-help">Разрешенные форматы: <strong>jpg, jpeg, png, bmp</strong>. Максимальный размер: <strong>до 2 Мб</strong>.</div>
            {% if form.photo.errors %}
                <div class="field-error">{% for e in form.photo.errors %}{{ e }}{% endfor %}</div>
            {% endif %}
        </div>

        <div class="form-actions">
            <a href="{% url 'cabinet' %}" class="btn">Отмена</a>
            <button type="submit" class="btn btn-primary">Отправить заявку</button>
        </div>
    </form>
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
<div class="form-box confirm-box">
    <h2 class="form-title">Удаление заявки</h2>
    <p class="dialog-message">
        Вы действительно хотите безвозвратно удалить заявку:
        <br>
        <strong>«{{ application.title }}»</strong>?
    </p>

    <div class="alert alert-warning">
        Внимание: данное действие необратимо. Удаление доступно только для заявок со статусом <strong>«Новая»</strong>.
    </div>

    <form method="post">
        {% csrf_token %}
        <div class="confirm-actions">
            <a href="{% url 'cabinet' %}" class="btn">
                Отмена
            </a>
            <button type="submit" class="btn btn-danger">
                Да, удалить
            </button>
        </div>
    </form>
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
<div class="admin-header">
    <div>
        <h2 class="box-title">Панель администратора</h2>
        <div class="admin-subtitle">Управление категориями и смена статусов заявок клиентов</div>
    </div>
    <div>
        <a href="/superadmin/" target="_blank" class="btn btn-sm">Django Superadmin</a>
    </div>
</div>

<!-- БЛОК 1: Управление категориями заявок -->
<div class="box">
    <div class="box-header">
        <div class="box-title">1. Управление категориями заявок</div>
    </div>

    <div class="cat-manage-grid">
        <!-- Форма добавления категории -->
        <div>
            <form method="post" action="{% url 'admin-add-category' %}" class="cat-add-form">
                {% csrf_token %}
                <input type="text" name="name" placeholder="Название новой категории" required class="cat-add-input">
                <button type="submit" class="btn btn-primary btn-sm">Добавить</button>
            </form>
            <div class="field-help">Название категории должно быть уникальным</div>
        </div>

        <!-- Список существующих категорий -->
        <div>
            <div class="cat-list-title">Существующие категории:</div>
            <div class="cat-list">
                {% for cat in categories %}
                    <div class="cat-tag">
                        <span><strong>{{ cat.name }}</strong> ({{ cat.applications.count }})</span>
                        <button type="button" class="btn btn-danger btn-sm cat-del-btn" onclick="document.getElementById('delCat{{ cat.pk }}').showModal()">Удалить</button>
                    </div>

                    <!-- Диалог удаления категории с предупреждением о каскадном удалении -->
                    <dialog id="delCat{{ cat.pk }}">
                        <div class="dialog-title text-danger">Удаление категории «{{ cat.name }}»</div>
                        <div class="alert alert-danger">
                            <strong>ВНИМАНИЕ ПО ТЗ!</strong> При удалении категории будут каскадно удалены ВСЕ заявки данной категории ({{ cat.applications.count }} шт.).
                        </div>
                        <p class="dialog-message">
                            Вы абсолютно уверены, что хотите безвозвратно удалить категорию <strong>«{{ cat.name }}»</strong>?
                        </p>
                        <div class="dialog-actions">
                            <button type="button" class="btn btn-sm" onclick="this.closest('dialog').close()">Отмена</button>
                            <form method="post" action="{% url 'admin-delete-category' cat.pk %}" class="inline-form">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-danger btn-sm">Да, удалить</button>
                            </form>
                        </div>
                    </dialog>
                {% empty %}
                    <span class="text-muted">Категорий пока нет.</span>
                {% endfor %}
            </div>
        </div>
    </div>
</div>

<!-- БЛОК 2: Заявки пользователей и смена статусов -->
<div class="box">
    <div class="box-header">
        <div class="box-title">2. Заявки пользователей и смена статусов</div>
        <div class="filter-group">
            <a href="{% url 'admin_panel' %}?status=all" class="filter-btn {% if status_filter == 'all' or not status_filter %}active{% endif %}">Все ({{ total_count }})</a>
            <a href="{% url 'admin_panel' %}?status=new" class="filter-btn {% if status_filter == 'new' %}active{% endif %}">Новые ({{ new_count }})</a>
            <a href="{% url 'admin_panel' %}?status=in_progress" class="filter-btn {% if status_filter == 'in_progress' %}active{% endif %}">В работе ({{ in_progress_count }})</a>
            <a href="{% url 'admin_panel' %}?status=completed" class="filter-btn {% if status_filter == 'completed' %}active{% endif %}">Выполненные ({{ completed_count }})</a>
        </div>
    </div>

    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th class="col-thumb">№</th>
                    <th class="col-date">Дата</th>
                    <th>Клиент</th>
                    <th>Заявка</th>
                    <th class="col-category">Категория</th>
                    <th class="col-category">План/Дизайн</th>
                    <th class="col-status">Статус</th>
                    <th class="col-action">Смена статуса</th>
                </tr>
            </thead>
            <tbody>
                {% for app in applications %}
                    <tr>
                        <td class="col-date-text">#{{ app.pk }}</td>
                        <td class="col-date-text">
                            {{ app.created_at|date:"d.m.Y H:i" }}
                        </td>
                        <td>
                            <div class="fw-bold">{{ app.user.username }}</div>
                            {% if app.user.fio %}<div class="text-muted small">{{ app.user.fio }}</div>{% endif %}
                        </td>
                        <td>
                            <div class="app-title">{{ app.title }}</div>
                            <div class="app-desc">{{ app.description|truncatewords:8 }}</div>
                            {% if app.comment %}
                                <div class="comment-text">
                                    <strong>Коммент:</strong> {{ app.comment }}
                                </div>
                            {% endif %}
                        </td>
                        <td>
                            <span class="badge badge-category">{{ app.category.name }}</span>
                        </td>
                        <td>
                            <div class="table-thumb-cell">
                                {% if app.photo %}
                                    <a href="{{ app.photo.url }}" target="_blank" title="План помещения">
                                        <img src="{{ app.photo.url }}" alt="План" class="plan-thumb">
                                    </a>
                                {% endif %}
                                {% if app.design_image %}
                                    <a href="{{ app.design_image.url }}" target="_blank" title="Готовый дизайн">
                                        <img src="{{ app.design_image.url }}" alt="Дизайн" class="design-thumb">
                                    </a>
                                {% endif %}
                            </div>
                        </td>
                        <td>
                            {% if app.status == 'new' %}
                                <span class="badge badge-new">Новая</span>
                            {% elif app.status == 'in_progress' %}
                                <span class="badge badge-progress">В работе</span>
                            {% elif app.status == 'completed' %}
                                <span class="badge badge-completed">Выполнено</span>
                            {% endif %}
                        </td>
                        <td class="col-action-cell">
                            {% if app.can_change_status %}
                                <!-- Кнопка 1: В работу -->
                                <button type="button" class="btn btn-sm btn-in-progress" onclick="document.getElementById('inProg{{ app.pk }}').showModal()">
                                    В работу
                                </button>

                                <!-- Кнопка 2: Выполнить -->
                                <button type="button" class="btn btn-success btn-sm" onclick="document.getElementById('comp{{ app.pk }}').showModal()">
                                    Выполнить
                                </button>

                                <!-- Диалог: Смена на «Принято в работу» (комментарий обязателен) -->
                                <dialog id="inProg{{ app.pk }}">
                                    <div class="dialog-title">Принять заявку #{{ app.pk }} в работу</div>
                                    <form method="post" action="{% url 'admin-status-in-progress' app.pk %}">
                                        {% csrf_token %}
                                        <div class="form-group text-start">
                                            <label>Укажите комментарий <span class="text-danger">*</span></label>
                                            <textarea name="comment" rows="3" required placeholder="Например: Взято в работу дизайнером..."></textarea>
                                            <div class="field-help">Комментарий обязателен по условиям ТЗ</div>
                                        </div>
                                        <div class="dialog-actions">
                                            <button type="button" class="btn btn-sm" onclick="this.closest('dialog').close()">Отмена</button>
                                            <button type="submit" class="btn btn-primary btn-sm">Перевести «В работу»</button>
                                        </div>
                                    </form>
                                </dialog>

                                <!-- Диалог: Смена на «Выполнено» (дизайн обязателен) -->
                                <dialog id="comp{{ app.pk }}">
                                    <div class="dialog-title text-success">Завершить заявку #{{ app.pk }}</div>
                                    <form method="post" action="{% url 'admin-status-completed' app.pk %}" enctype="multipart/form-data">
                                        {% csrf_token %}
                                        <div class="form-group text-start">
                                            <label>Прикрепите изображение дизайна <span class="text-danger">*</span></label>
                                            <input type="file" name="design_image" accept=".jpg,.jpeg,.png,.bmp" required>
                                            <div class="field-help">Форматы: jpg, jpeg, png, bmp (до 5 Мб)</div>
                                        </div>
                                        <div class="dialog-actions">
                                            <button type="button" class="btn btn-sm" onclick="this.closest('dialog').close()">Отмена</button>
                                            <button type="submit" class="btn btn-success btn-sm">Сохранить «Выполнено»</button>
                                        </div>
                                    </form>
                                </dialog>
                            {% else %}
                                <span class="text-muted small">Смена невозможна</span>
                            {% endif %}
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="8" class="empty-state">
                            Заявок не найдено.
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
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
<div class="form-box confirm-box">
    <h2 class="form-title">Удаление категории</h2>
    <p class="dialog-message">
        Вы действительно хотите удалить категорию <br><strong>«{{ category.name }}»</strong>?
    </p>

    <div class="alert alert-danger">
        <strong>ВНИМАНИЕ ПО ТЗ!</strong> При удалении категории будут безвозвратно удалены все связанные заявки ({{ category.applications.count }} шт.).
    </div>

    <form method="post">
        {% csrf_token %}
        <div class="confirm-actions">
            <a href="{% url 'admin_panel' %}" class="btn">
                Отмена
            </a>
            <button type="submit" class="btn btn-danger">
                Подтвердить удаление
            </button>
        </div>
    </form>
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

26. **Вопрос:** Почему в проекте был выполнен полный отказ от Bootstrap в пользу чистого CSS?  
    **Ответ:** 
    1) **Автономность и надежность:** На демонстрационном экзамене рабочие станции часто изолированы от внешнего интернета, из-за чего CDN-ресурсы Bootstrap не загружаются и верстка «рассыпается». Чистый локальный CSS гарантирует 100% работоспособность офлайн.
    2) **Скорость и размер:** Исключение Bootstrap сэкономило сотни килобайт ненужного CSS/JS кода, обеспечив мгновенный рендеринг страницы.
    3) **Чистота кода и соответствие регламенту:** Строгий бруталистский минимализм демонстрирует комиссии глубокое владение базовыми стандартами веба (Flexbox, CSS Grid, CSS Variables) без использования готовых шаблонных компонентов.

27. **Вопрос:** Как работают модальные окна (удаление заявки, смена статуса) без использования JavaScript-библиотеки Bootstrap?  
    **Ответ:** Использован нативный стандартный тег HTML5 `<dialog>`. Он поддерживается всеми современными браузерами и предоставляет встроенные методы API: `dialog.showModal()` для открытия с автоматической модальной блокировкой фона (`::backdrop`) и `dialog.close()` для закрытия. Это устранило необходимость в подключении скриптов Bootstrap или jQuery.

28. **Вопрос:** Как архитектурно структурирован файл стилей `style.css`?  
    **Ответ:** Файл логически разбит на 11 модулей с оглавлением:
    1) Дизайн-токены и переменные `:root` (шрифты, цвета, рамки);
    2) Сброс стилей (Reset) с принудительным `border-radius: 0` и `box-shadow: none`;
    3) Шапка и адаптивная навигация;
    4) Система кнопок и фильтрации с эффектом инверсии;
    5) Flash-сообщения (Alerts);
    6) Промо-блок и сетка карточек проектов;
    7) Таблицы данных и статусные бейджи;
    8) Поля форм и серверная подсветка невалидных полей (`.is-invalid`);
    9) Стилизация нативных диалогов `<dialog>`;
    10) Фиксированный подвал (Sticky Footer на Flexbox);
    11) Вспомогательные утилитные классы.

26. **Вопрос:** Почему в проекте был выполнен полный отказ от Bootstrap в пользу чистого CSS?  
    **Ответ:** 
    1) **Автономность и надежность:** На демонстрационном экзамене рабочие станции часто изолированы от внешнего интернета, из-за чего CDN-ресурсы Bootstrap не загружаются и верстка «рассыпается». Чистый локальный CSS гарантирует 100% работоспособность офлайн.
    2) **Скорость и размер:** Исключение Bootstrap сэкономило сотни килобайт ненужного CSS/JS кода, обеспечив мгновенный рендеринг страницы.
    3) **Чистота кода и соответствие регламенту:** Строгий бруталистский минимализм демонстрирует комиссии глубокое владение базовыми стандартами веба (Flexbox, CSS Grid, CSS Variables) без использования готовых шаблонных компонентов.

27. **Вопрос:** Как работают модальные окна (удаление заявки, смена статуса) без использования JavaScript-библиотеки Bootstrap?  
    **Ответ:** Использован нативный стандартный тег HTML5 `<dialog>`. Он поддерживается всеми современными браузерами и предоставляет встроенные методы API: `dialog.showModal()` для открытия с автоматической модальной блокировкой фона (`::backdrop`) и `dialog.close()` для закрытия. Это устранило необходимость в подключении скриптов Bootstrap или jQuery.

28. **Вопрос:** Как устроен файл стилей `style.css` и как в нем обеспечивается независимость от Bootstrap?  
    **Ответ:** Файл написан на чистом CSS без внешних библиотек и разбит на понятные секции: сброс базовых отступов, стили шапки и меню, кнопки основных действий, промо-блок со счетчиком, карточки проектов, оформление таблиц с бейджами статусов, карточки форм с красной подсветкой невалидных полей (`.is-invalid`), модальные окна на теге `dialog` и подвал. Использованы стандартные свойства без избыточных фреймворков.


---

---

## 4.5. Инженерные приемы оптимизации интерфейса: отказ от Bootstrap и чистый бруталистский CSS
### 10.6. Инженерные приемы максимального облегчения интерфейса

Чтобы сделать интерфейс максимально быстрым, надежным, независимым от сети и идеальным для демонстрационного экзамена:
1. **100% отказ от сторонних фреймворков и внешних CDN:**  
   В проекте полностью исключены Bootstrap CSS, Bootstrap Icons и Bootstrap JS Bundle. Сайт не обращается к внешним серверам и мгновенно функционирует в локальных изолированных сетях без доступа в интернет (offline demo-exam mode).
2. **Чистый, понятный CSS ([style.css](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/static/css/style.css)):**  
   Стили написаны вручную на чистом CSS без Bootstrap и сложных абстракций. Интерфейс аккуратный, минималистичный, блоки четко выровнены через Flexbox и Grid, таблицы и формы легко читаются, а невалидные поля подсвечиваются стандартным классом `.is-invalid`.
3. **Модальные окна на нативном HTML5 `<dialog>`:**  
   Диалоги подтверждения удаления и формы смены статусов заявок переведены на стандартный тег `<dialog>` с методами `.showModal()` и `.close()`. Это устраняет необходимость в 150+ Кб сторонних JavaScript-библиотек.
4. **Информационный промо-блок и динамический счетчик:**  
   На главной странице размещен контрастный блок счетчика с уникальным ID `#in-progress-counter`, отображающий точное число заявок в статусе «Принято в работу» напрямую из ORM.
5. **Семантическая серверная подсветка валидации:**  
   При наличии ошибок валидации формы Django поля получают класс `.is-invalid` с контрастной красной обводкой (`#cc0000`), а точный текст ошибки отображается в блоке `.field-error` непосредственно под полем.

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
