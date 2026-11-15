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
| [**Секция 0**](#секция-0-общесистемный-фундамент-архитектура-и-первоначальная-настройка-проекта) | **Общесистемный фундамент** | MVT vs MVC, HTTP-цикл, анализ ТЗ, окружение Python 3.12, детальный разбор и код `settings.py`, архитектура контроллеров и полный код `catalog/views.py`, медиа-хранилище, базовый каркас `base.html` и стили |
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

## 6. Шаг 4. Представления (Views) и бизнес-логика (`catalog/views.py`) — полный архитектурный разбор

Файл: [catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/views.py)

Представления (Views) в Django — это «мозг» и главный диспетчер всего веб-приложения. В архитектуре MVT именно View принимает входящий HTTP-запрос от пользователя, применяет бизнес-логику, общается с базой данных через модели и решает, какую HTML-страницу или ответ вернуть браузеру.

### 6.1. Теория представлений в Django простыми словами (без сложных терминов)

Представьте веб-сайт как **ресторан**:
- **Посетитель (Браузер)** делает заказ — это входящий сетевой пакет **`HttpRequest`**.
- **Официант/Диспетчер (urls.py)** смотрит в меню и направляет заказ на нужную кухню.
- **Шеф-повар (View в views.py)** — это и есть представление! Он берет заказ, идет в кладовую за продуктами (**Models / База данных**), готовит блюдо, красиво оформляет его на тарелке (**Template / HTML-шаблон**) и отдает официанту, чтобы тот унес его клиенту — это исходящий ответ **`HttpResponse`**.

#### Главная формула любого View в Django:
```python
def my_view(request):
    # 1. Приняли запрос (request)
    # 2. Выполнили логику (достали данные из БД, проверили форму)
    # 3. Вернули ответ (render или redirect)
    return HttpResponse(...) # или render(request, 'page.html', context)
```

---

### 6.2. Почему в проекте используются FBV (функции), а не CBV (классы)?

В Django есть два подхода к написанию представлений:
1. **FBV (Function-Based Views) — представления на функциях:**  
   Каждое действие описывается как обычная Python-функция (`def my_view(request):`).
2. **CBV (Class-Based Views) — представления на классах:**  
   Действия описываются через наследование от стандартных классов Django (`ListView`, `CreateView`, `DeleteView`).

> [!TIP]
> **Почему FBV лучше для учебной практики и демонстрационного экзамена:**  
> - **Прозрачность 100%:** В функции нет «скрытой магии» наследования и миксинов. Каждая строчка видна: где проверяется метод `POST`, где создается форма, где делается `save()`, куда идет редирект.  
> - **Легкость объяснения преподавателю:** Студент может пальцем показать каждую строчку и объяснить её назначение за 30 секунд.  
> - **Полный контроль над поведением:** Не нужно переопределять сложные методы `get_context_data()`, `form_valid()` или `get_queryset()`.

---

### 6.3. Фундаментальные концепции работы View, которые нужно знать

#### 1. Разделение запросов `GET` и `POST`
Любая веб-страница работает в двух основных режимах:
- **`GET` (Получить / Посмотреть):**  
  Пользователь просто открывает ссылку или вводит адрес в браузере. Данные из базы только читаются. Если на странице есть форма, при `GET` мы показываем её **пустой** для заполнения. Также в GET передаются параметры фильтрации в URL (например, `?status=new`).
- **`POST` (Отправить / Изменить):**  
  Пользователь нажал кнопку «Отправить», «Зарегистрироваться», «Удалить» или «Войти». Браузер отправляет пачку данных на сервер в теле запроса. При `POST` мы считываем данные, валидируем их и сохраняем в базу данных.

#### 2. Разница между `render()` и `redirect()`: Паттерн PRG (Post/Redirect/Get)
- **`render(request, 'template.html', context)`:**  
  Берет HTML-шаблон, подставляет в него переменные из словаря `context` и отдает браузеру готовый HTML со статусом `200 OK`. Адрес в строке браузера при этом **НЕ меняется**.
- **`redirect('route_name')`:**  
  Возвращает браузеру короткий ответ `302 Found` с заголовком `Location: /cabinet/`. Браузер, получив этот ответ, сам делает **новый чистый GET-запрос** по новому адресу.

> [!IMPORTANT]
> **Почему после успешного POST ВСЕГДА делается `redirect()`, а не `render()`?**  
> Это всемирный стандарт веб-разработки, называемый **PRG (Post/Redirect/Get)**.  
> Если после создания заявки вернуть `render()`, и пользователь случайно нажмет кнопку «Обновить страницу» (F5) в браузере, браузер покажет пугающее окно: *«Повторно отправить форму?»*. При нажатии «Да» в базе создастся **заявка-дубликат**!  
> Если же сделать `redirect()`, адрес очищается, и при нажатии F5 пользователь просто обновит личный кабинет без повторного создания заявки.

#### 3. Загрузка файлов и `request.FILES`
Обычные текстовые поля формы передаются в словаре `request.POST`.  
Но бинарные файлы (фотографии планов помещений, эскизы дизайна) попадают в отдельный словарь **`request.FILES`**.  
Поэтому в представлениях создания заявки и сдачи дизайна форма инициализируется строго двумя аргументами:
```python
form = ApplicationCreateForm(request.POST, request.FILES)
```
*Если забыть передать `request.FILES`, Django даже не заметит прикрепленный файл, и он не сохранится в базу!*  
А в HTML-форме обязательно должен быть указан атрибут: `enctype="multipart/form-data"`.

#### 4. Декораторы доступа: Безопасность и разграничение прав
Декоратор — это функция-надстройка, которая выполняется **до** вызова самого представления (своеобразный «фейсконтроль» на входе):
- **`@login_required`:**  
  Проверяет, авторизован ли посетитель (`request.user.is_authenticated`). Если гость попытается открыть страницу `/cabinet/` или `/application/create/`, декоратор не пустит его и мгновенно перенаправит на `/login/?next=/cabinet/`.
- **`@user_passes_test(is_admin, login_url='login')`:**  
  Запускает функцию проверки прав `is_admin`. Если у пользователя нет прав персонала (`is_staff` или `is_superuser`), доступ к панели администратора блокируется, и его перенаправляет на страницу авторизации.

#### 5. Система Flash-сообщений (`django.contrib.messages`)
Как передать уведомление пользователю («Заявка создана!», «Неверный пароль», «Категория удалена»), если мы делаем `redirect()`?  
Переменные из контекста при редиректе теряются! Поэтому Django сохраняет сообщения во временное хранилище сессии пользователя:
- `messages.success(request, 'Текст успеха')` — зеленая плашка.
- `messages.error(request, 'Текст ошибки')` — красная плашка.
- `messages.info(request, 'Информационный текст')` — синяя плашка.  
При следующем открытии страницы базовый шаблон `base.html` считывает эти сообщения, отображает их и тут же удаляет из сессии.

---

### 6.4. Сводная архитектурная таблица всех представлений `catalog/views.py`

| № | Функция представления | URL-маршрут | HTTP-методы | Права доступа | Назначение и краткая логика |
| :- | :--- | :--- | :--- | :--- | :--- |
| **1** | `is_admin(user)` | — (хелпер) | — | Внутренняя функция | Проверяет, что пользователь аутентифицирован и имеет флаг `is_staff` или `is_superuser`. |
| **2** | `index(request)` | `/` | GET | Доступно всем | Главная страница: счетчик заявок в работе (`COUNT`) и 4 последние выполненные заявки с категориями. |
| **3** | `register_view(request)` | `/register/` | GET, POST | Только для гостей | Регистрация нового клиента с серверной валидацией, автологином и редиректом в личный кабинет. |
| **4** | `login_view(request)` | `/login/` | GET, POST | Только для гостей | Аутентификация по логину/паролю и ролевое перенаправление: клиент ➔ кабинет, админ ➔ панель управления. |
| **5** | `logout_view(request)` | `/logout/` | GET, POST | Авторизованные | Завершение сеанса пользователя, очистка сессионных cookies и редирект на главную страницу. |
| **6** | `cabinet_view(request)` | `/cabinet/` | GET | `@login_required` | Личный кабинет клиента: фильтрация своих заявок по статусу, бейджи-счетчики и сортировка по дате. |
| **7** | `create_application_view(request)` | `/application/create/` | GET, POST | `@login_required` | Оформление заявки с загрузкой плана помещения до 2 Мб, автопривязкой автора и установкой статуса «Новая». |
| **8** | `delete_application_view(request, pk)` | `/application/<pk>/delete/` | GET, POST | `@login_required` | Безопасное удаление заявки: проверка авторства (IDOR-защита), проверка статуса «Новая» и диалог подтверждения. |
| **9** | `admin_panel_view(request)` | `/admin-panel/` | GET | `@user_passes_test` | Главная панель админа: список всех заявок с фильтрами, модалки смены статусов и блок управления категориями. |
| **10** | `admin_change_status_in_progress(request, pk)` | `/admin-panel/application/<pk>/in-progress/` | POST | `@user_passes_test` | Смена статуса заявки «Новая» ➔ «Принято в работу» с обязательным текстовым комментарием. |
| **11** | `admin_change_status_completed(request, pk)` | `/admin-panel/application/<pk>/completed/` | POST | `@user_passes_test` | Смена статуса заявки «Новая» ➔ «Выполнено» с обязательным прикреплением готового дизайн-проекта до 5 Мб. |
| **12** | `admin_add_category(request)` | `/admin-panel/category/add/` | POST | `@user_passes_test` | Добавление новой категории помещений с проверкой уникальности названия без учета регистра. |
| **13** | `admin_delete_category(request, pk)` | `/admin-panel/category/<pk>/delete/` | GET, POST | `@user_passes_test` | Каскадное удаление категории (`CASCADE`): автоматическое удаление всех заявок этой категории с подтверждением. |

---

### 6.5. Полный сплошной код файла `catalog/views.py` (310 строк без сокращений)

Файл: [catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/views.py)

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

from .models import Application, Category, User
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    ApplicationCreateForm,
    StatusToInProgressForm,
    StatusToCompletedForm,
    CategoryForm,
)


def is_admin(user):
    """Проверка прав администратора"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def index(request):
    """
    Главная страница «Design.pro»:
    - Счетчик: количество заявок в статусе «Принято в работу»
    - Не более 4 последних заявок в статусе «Выполнено»
    """
    in_progress_count = Application.objects.filter(status=Application.STATUS_IN_PROGRESS).count()
    completed_apps = Application.objects.filter(
        status=Application.STATUS_COMPLETED
    ).select_related('category').order_by('-created_at')[:4]

    context = {
        'in_progress_count': in_progress_count,
        'completed_apps': completed_apps,
    }
    return render(request, 'index.html', context)


def register_view(request):
    """
    Регистрация нового пользователя с серверной валидацией.
    """
    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Регистрация прошла успешно! Добро пожаловать, {user.fio or user.username}!')
            login(request, user)
            return redirect('cabinet')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме регистрации.')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """
    Авторизация пользователя и администратора.
    Перенаправление:
    - Пользователь -> Личный кабинет (cabinet)
    - Администратор -> Панель администратора (admin_panel)
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_panel')
        return redirect('cabinet')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Вы успешно вошли как {user.username}!')

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_staff or user.is_superuser:
                return redirect('admin_panel')
            return redirect('cabinet')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """
    Выход из учетной записи для всех авторизованных пользователей.
    """
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('index')


@login_required
def cabinet_view(request):
    """
    Личный кабинет авторизованного пользователя:
    - Просмотр своих заявок (временная метка, название, описание, категория, статус)
    - Сортировка по умолчанию: от новых к старым (-created_at)
    - Фильтрация по статусу (Все, Новая, Принято в работу, Выполнено)
    """
    user_apps = Application.objects.filter(user=request.user).select_related('category')

    # Подсчет количества заявок по статусам для бейджей фильтрации
    total_count = user_apps.count()
    new_count = user_apps.filter(status=Application.STATUS_NEW).count()
    in_progress_count = user_apps.filter(status=Application.STATUS_IN_PROGRESS).count()
    completed_count = user_apps.filter(status=Application.STATUS_COMPLETED).count()

    # Применение фильтра
    current_filter = request.GET.get('status', 'all')
    if current_filter in [Application.STATUS_NEW, Application.STATUS_IN_PROGRESS, Application.STATUS_COMPLETED]:
        user_apps = user_apps.filter(status=current_filter)

    user_apps = user_apps.order_by('-created_at')

    context = {
        'applications': user_apps,
        'current_filter': current_filter,
        'total_count': total_count,
        'new_count': new_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    return render(request, 'catalog/cabinet.html', context)


@login_required
def create_application_view(request):
    """
    Создание заявки на разработку дизайна интерьера помещения.
    - Все поля обязательны
    - Валидация фото (jpg, jpeg, png, bmp до 2 Мб)
    - Автоматическая временная метка и статус «Новая»
    """
    if request.method == 'POST':
        form = ApplicationCreateForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.status = Application.STATUS_NEW
            application.save()
            messages.success(request, f'Заявка «{application.title}» успешно создана и получила статус «Новая»!')
            return redirect('cabinet')
        else:
            messages.error(request, 'Пожалуйста, проверьте корректность заполнения полей заявки.')
    else:
        form = ApplicationCreateForm()

    return render(request, 'catalog/application_form.html', {'form': form})


@login_required
def delete_application_view(request, pk):
    """
    Удаление заявки:
    - Пользователь может удалить ТОЛЬКО свою заявку
    - Удаление возможно ТОЛЬКО если статус «Новая»
    - Обязательное подтверждение действия
    """
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if not application.is_deletable:
        messages.error(
            request,
            'Запрещено! Заявку нельзя удалить, так как её статус уже изменен администратором на «Принято в работу» или «Выполнено».'
        )
        return redirect('cabinet')

    if request.method == 'POST':
        title = application.title
        application.delete()
        messages.success(request, f'Заявка «{title}» была успешно удалена.')
        return redirect('cabinet')

    return render(request, 'catalog/application_confirm_delete.html', {'application': application})


@user_passes_test(is_admin, login_url='login')
def admin_panel_view(request):
    """
    Личный кабинет администратора (панель управления):
    - Просмотр всех заявок с фильтрацией
    - Смена статуса заявок «Новая» -> «Принято в работу» (с комментарием)
    - Смена статуса заявок «Новая» -> «Выполнено» (с фото дизайна)
    - Управление категориями (добавление, удаление с каскадным удалением заявок)
    """
    status_filter = request.GET.get('status', 'all')
    all_apps = Application.objects.select_related('user', 'category').all()

    total_count = all_apps.count()
    new_count = all_apps.filter(status=Application.STATUS_NEW).count()
    in_progress_count = all_apps.filter(status=Application.STATUS_IN_PROGRESS).count()
    completed_count = all_apps.filter(status=Application.STATUS_COMPLETED).count()

    if status_filter in [Application.STATUS_NEW, Application.STATUS_IN_PROGRESS, Application.STATUS_COMPLETED]:
        applications = all_apps.filter(status=status_filter).order_by('-created_at')
    else:
        applications = all_apps.order_by('-created_at')

    categories = Category.objects.all().order_by('name')
    category_form = CategoryForm()

    context = {
        'applications': applications,
        'categories': categories,
        'category_form': category_form,
        'status_filter': status_filter,
        'total_count': total_count,
        'new_count': new_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    return render(request, 'catalog/admin_panel.html', context)


@user_passes_test(is_admin, login_url='login')
def admin_change_status_in_progress(request, pk):
    """
    Смена статуса заявки с «Новая» на «Принято в работу» с обязательным комментарием.
    """
    application = get_object_or_404(Application, pk=pk)

    if application.status != Application.STATUS_NEW:
        messages.error(request, 'Смена статуса с «Принято в работу» или «Выполнено» невозможна.')
        return redirect('admin_panel')

    if request.method == 'POST':
        form = StatusToInProgressForm(request.POST)
        if form.is_valid():
            application.status = Application.STATUS_IN_PROGRESS
            application.comment = form.cleaned_data['comment']
            application.save()
            messages.success(request, f'Заявка #{application.pk} переведена в статус «Принято в работу».')
        else:
            messages.error(request, 'Для перевода заявки в работу обязательно укажите комментарий.')
    return redirect('admin_panel')


@user_passes_test(is_admin, login_url='login')
def admin_change_status_completed(request, pk):
    """
    Смена статуса заявки с «Новая» на «Выполнено» с обязательным прикреплением изображения дизайна.
    """
    application = get_object_or_404(Application, pk=pk)

    if application.status != Application.STATUS_NEW:
        messages.error(request, 'Смена статуса с «Принято в работу» или «Выполнено» невозможна.')
        return redirect('admin_panel')

    if request.method == 'POST':
        form = StatusToCompletedForm(request.POST, request.FILES)
        if form.is_valid():
            application.status = Application.STATUS_COMPLETED
            application.design_image = form.cleaned_data['design_image']
            application.save()
            messages.success(request, f'Заявка #{application.pk} успешно выполнена и прикреплен дизайн!')
        else:
            messages.error(request, 'Для завершения заявки обязательно загрузите изображение дизайна (jpg, jpeg, png, bmp до 5 Мб).')
    return redirect('admin_panel')


@user_passes_test(is_admin, login_url='login')
def admin_add_category(request):
    """
    Добавление новой категории заявок администратором.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория «{category.name}» успешно добавлена.')
        else:
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, f'Ошибка категории: {e}')
    return redirect('admin_panel')


@user_passes_test(is_admin, login_url='login')
def admin_delete_category(request, pk):
    """
    Удаление категории заявок:
    При удалении категории каскадно удаляются все заявки данной категории.
    """
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = category.name
        apps_count = category.applications.count()
        category.delete()  # Каскадное удаление заявок через on_delete=models.CASCADE
        messages.success(
            request,
            f'Категория «{name}» и все привязанные заявки ({apps_count} шт.) были безвозвратно удалены.'
        )
        return redirect('admin_panel')

    return render(request, 'catalog/category_confirm_delete.html', {'category': category})
```

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

### 3. Контроллеры гостевого функционала (`catalog/views.py`) — Детальный разбор функций

Файл: [catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/views.py)

В рамках Практической работы №2.1 (Функционал гостя) задействованы три ключевых представления:
1. `index(request)` — Главная страница-витрина студии со счетчиком и 4-мя последними работами.
2. `register_view(request)` — Регистрация нового аккаунта с серверной валидацией и автовходом.
3. `login_view(request)` — Авторизация пользователей и администратора с ролевым перенаправлением.

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Application
from .forms import UserRegistrationForm, UserLoginForm
```

---

#### 3.1. Функция `index(request)` — Главная страница («Витрина студии»)

```python
def index(request):
    """
    Главная страница «Design.pro»:
    - Счетчик: количество заявок в статусе «Принято в работу»
    - Не более 4 последних заявок в статусе «Выполнено»
    """
    in_progress_count = Application.objects.filter(status=Application.STATUS_IN_PROGRESS).count()
    completed_apps = Application.objects.filter(
        status=Application.STATUS_COMPLETED
    ).select_related('category').order_by('-created_at')[:4]

    context = {
        'in_progress_count': in_progress_count,
        'completed_apps': completed_apps,
    }
    return render(request, 'index.html', context)
```

##### Логика работы «на пальцах» (без заморочек):
Когда посетитель заходит на сайт `http://localhost:8089/`, браузер делает GET-запрос к `index()`.
Функция делает две вещи:
1. Идет в базу данных и считает, сколько сейчас заявок «в работе» (например, 7 штук). Это число выводится крупной цифрой в промо-блоке.
2. Ищет все готовые дизайн-проекты (статус «Выполнено»), берет из них **ровно 4 самые свежие работы** и прикрепляет к ним названия категорий.
3. Упаковывает всё это в «чемоданчик» (словарь `context`) и отправляет в шаблон `index.html`. Шаблон превращает эти данные в красивую страницу.

##### Построчный разбор каждой команды:
- `in_progress_count = Application.objects.filter(status=Application.STATUS_IN_PROGRESS).count()`:
  - `Application.objects.filter(...)` — отбирает из таблицы заявок только те, у которых статус равен `'in_progress'`.
  - `.count()` — **критически важная оптимизация!** Он не загружает объекты заявок в оперативную память Python, а заставляет СУБД выполнить быстрый SQL-запрос `SELECT COUNT(*) FROM catalog_application WHERE status = 'in_progress';`. Это работает мгновенно даже при миллионе записей.
- `completed_apps = Application.objects.filter(status=Application.STATUS_COMPLETED)`:
  - Фильтрует только завершенные заявки (`status='completed'`).
- `.select_related('category')`:
  - **Оптимизация жадной загрузки (Eager Loading):** модель `Application` связана с моделью `Category` через внешний ключ `ForeignKey`. Если не написать `.select_related('category')`, Django при выводе имени каждой категории в цикле шаблона будет делать отдельный SQL-запрос к таблице категорий (так называемая проблема N+1 запросов). Метод `select_related` делает один умный SQL `INNER JOIN`, подтягивая названия категорий сразу в основном запросе.
- `.order_by('-created_at')`:
  - Знак минус перед `created_at` означает сортировку по убыванию (SQL `ORDER BY created_at DESC`). То есть самые новые завершенные проекты будут идти первыми.
- `[:4]`:
  - Стандартный срез Python, который Django ORM транслирует в SQL-директиву `LIMIT 4`. Из базы извлекаются ровно 4 строки, что строго соответствует ТЗ («не более 4 последних заявок»).
- `context = {'in_progress_count': in_progress_count, 'completed_apps': completed_apps}`:
  - Создает словарь данных для шаблонизатора DTL. Внутри `index.html` эти переменные будут доступны как `{{ in_progress_count }}` и `{% for app in completed_apps %}`.
- `return render(request, 'index.html', context)`:
  - Склеивает шаблон с данными и возвращает браузеру готовую HTML-страницу со статусом `200 OK`.

---

#### 3.2. Функция `register_view(request)` — Регистрация нового пользователя

```python
def register_view(request):
    """
    Регистрация нового пользователя с серверной валидацией.
    """
    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Регистрация прошла успешно! Добро пожаловать, {user.fio or user.username}!')
            login(request, user)
            return redirect('cabinet')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме регистрации.')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
```

##### Логика работы «на пальцах» (без заморочек):
- Если на страницу регистрации случайно зашел уже авторизованный пользователь, мы не мучаем его формой, а сразу перенаправляем в личный кабинет (`redirect('cabinet')`).
- Если пользователь просто открыл страницу (метод `GET`), мы создаем чистую пустую форму `UserRegistrationForm()` и показываем её (`render`).
- Если пользователь заполнил поля и нажал кнопку «Зарегистрироваться» (метод `POST`):
  1. Загружаем присланные данные в форму.
  2. Запускаем строгую проверку `form.is_valid()` (ФИО на кириллицу, уникальность логина, совпадение паролей, галочку ПДн).
  3. Если всё чисто — создаем пользователя в БД (`form.save()`), показываем зеленое уведомление «Регистрация прошла успешно!», **сразу авторизуем его** (`login(request, user)`) и отправляем в личный кабинет. Пользователю не нужно второй раз вводить логин и пароль!
  4. Если найдены ошибки — выводим красное сообщение, и снова отображаем форму: поля с ошибками подсветятся красным цветом (класс `is-invalid`), а под ними напишется точная причина ошибки.

##### Построчный разбор каждой команды:
- `if request.user.is_authenticated: return redirect('cabinet')`:
  - Защита от бессмысленных действий. Проверяет, вошел ли пользователь в систему. Если да — перенаправляет в кабинет.
- `if request.method == 'POST':`:
  - Проверяет тип HTTP-запроса. Если метод `POST` — значит, пользователь нажал кнопку отправки формы.
- `form = UserRegistrationForm(request.POST)`:
  - Создает экземпляр формы и «связывает» (bind) его с данными из `request.POST`.
- `if form.is_valid():`:
  - Запускает валидацию всех полей и кастомные методы `clean_fio()`, `clean_username()`, `clean()`. Если хотя бы в одном поле ошибка — возвращает `False`.
- `user = form.save()`:
  - Вызывает метод `save()` нашей формы. Внутри него вызывается `user.set_password(password)`, который хэширует пароль по алгоритму PBKDF2/SHA-256 и сохраняет новую запись в таблице `catalog_user`.
- `messages.success(request, f'...')`:
  - Записывает flash-сообщение об успехе во временное хранилище сессии.
- `login(request, user)`:
  - Стандартная функция Django Auth. Создает запись сессии в таблице `django_session` и записывает идентификатор пользователя в зашифрованные cookie браузера (`sessionid`).
- `return redirect('cabinet')`:
  - Паттерн PRG: шлет ответ `302 Found` с переходом на страницу личного кабинета.
- Ветка `else` (при невалидной форме):
  - `messages.error(request, 'Пожалуйста, исправьте ошибки...')` выводит предупреждение.
- Ветка `else` (при GET-запросе):
  - `form = UserRegistrationForm()` создает пустую несвязанную форму для первичного отображения.
- `return render(request, 'registration/register.html', {'form': form})`:
  - Отрисовывает страницу. Если форма содержала ошибки, объект `form` передаст их в HTML, где сработают блоки `{% if form.field.errors %}`.

---

#### 3.3. Функция `login_view(request)` — Авторизация и ролевая маршрутизация

```python
def login_view(request):
    """
    Авторизация пользователя и администратора.
    Перенаправление:
    - Пользователь -> Личный кабинет (cabinet)
    - Администратор -> Панель администратора (admin_panel)
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_panel')
        return redirect('cabinet')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Вы успешно вошли как {user.username}!')

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_staff or user.is_superuser:
                return redirect('admin_panel')
            return redirect('cabinet')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})
```

##### Логика работы «на пальцах» (без заморочек):
- Если пользователь уже авторизован и опять заходит на `/login/`, система смотрит на его роль: администратора шлет в Панель управления (`/admin-panel/`), а обычного клиента — в Личный кабинет (`/cabinet/`).
- При открытии страницы (`GET`) отдается пустая форма с полями «Логин» и «Пароль».
- При нажатии кнопки «Войти» (`POST`):
  1. Форма `UserLoginForm` проверяет, есть ли такой логин и подходит ли пароль (через стандартный `django.contrib.auth.authenticate`).
  2. Если пароль не подошел — форма признается невалидной, и пользователю выводится красная ошибка: *«Неверный логин или пароль»*.
  3. Если всё верно — авторизуем пользователя через `login(request, user)`.
  4. Проверяем параметр `?next=`. Например, если неавторизованный клиент пытался открыть `/application/create/`, система сначала отправила его на страницу логина с адресом `/login/?next=/application/create/`. После успешного входа система вернет его ровно туда, куда он и шел!
  5. Если параметра `next` не было, включается **ролевой светофор**:
     - Если вошел админ (`is_staff` или `is_superuser`) — открывается `/admin-panel/`.
     - Если вошел клиент — открывается `/cabinet/`.

##### Построчный разбор каждой команды:
- `if request.user.is_authenticated:`:
  - Проверка активной сессии. Если пользователь уже залогинен, проверяются флаги прав:
    - `if request.user.is_staff or request.user.is_superuser:` ➔ редирект на `admin_panel`.
    - Иначе ➔ редирект на `cabinet`.
- `form = UserLoginForm(request.POST)`:
  - Инициализация формы аутентификации присланными логином и паролем.
- `if form.is_valid():`:
  - Внутри формы вызывается `authenticate()`. Метод проверяет хэш пароля. Если совпало — форма валидна.
- `user = form.get_user()`:
  - Достает найденный и подтвержденный объект пользователя из формы.
- `login(request, user)`:
  - Создает сессию для данного пользователя.
- `next_url = request.GET.get('next')`:
  - Считывает GET-параметр `next` из адресной строки браузера.
- `if next_url: return redirect(next_url)`:
  - Бесшовный возврат на ранее запрошенную страницу.
- `if user.is_staff or user.is_superuser: return redirect('admin_panel')`:
  - Перенаправление администратора по ТЗ в специальную панель управления.
- `return redirect('cabinet')`:
  - Перенаправление обычного клиента в его личный кабинет.
- `messages.error(request, 'Неверный логин или пароль.')`:
  - Защита от подбора паролей: мы не уточняем, что именно неверно (логин или пароль), чтобы не подсказывать злоумышленнику существование логина.

---

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

### 3. Контроллеры пользователя (`catalog/views.py`) — Детальный разбор функций

Файл: [catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/views.py)

В рамках Практической работы №2.2 (Функционал зарегистрированного клиента) реализованы 4 контроллера:
1. `logout_view(request)` — Безопасный выход из аккаунта и очистка сессии.
2. `cabinet_view(request)` — Личный кабинет клиента с бейджами-счетчиками и фильтрацией заявок по статусам.
3. `create_application_view(request)` — Создание заявки с валидацией файла плана до 2 Мб и автопривязкой автора.
4. `delete_application_view(request, pk)` — Двухэтапное безопасное удаление только своих заявок и только в статусе «Новая».

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationCreateForm
```

---

#### 3.1. Функция `logout_view(request)` — Выход из системы

```python
def logout_view(request):
    """
    Выход из учетной записи для всех авторизованных пользователей.
    """
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('index')
```

##### Логика работы «на пальцах» (без заморочек):
Когда пользователь кликает на кнопку «Выход»:
1. Функция `logout(request)` находит текущую сессию в базе данных SQLite (в таблице `django_session`) и стирает её. В браузере очищается идентификатор `sessionid`.
2. В систему сообщений добавляется информационная плашка: *«Вы успешно вышли из системы»*.
3. Пользователь перенаправляется на главную страницу (`index`), где навигационная панель снова показывает ссылки «Вход» и «Регистрация».

##### Построчный разбор:
- `logout(request)`: Встроенный механизм безопасности Django. Он полностью обнуляет объект `request.user` (превращая его в `AnonymousUser`) и инвалидирует куки сессии, предотвращая угон аккаунта через оставленную вкладку браузера.
- `messages.info(request, '...')`: Формирует синее всплывающее уведомление для пользователя.
- `return redirect('index')`: Безопасное перенаправление на корень сайта (`/`).

---

#### 3.2. Функция `cabinet_view(request)` — Личный кабинет и фильтрация заявок

```python
@login_required
def cabinet_view(request):
    """
    Личный кабинет авторизованного пользователя:
    - Просмотр своих заявок (временная метка, название, описание, категория, статус)
    - Сортировка по умолчанию: от новых к старым (-created_at)
    - Фильтрация по статусу (Все, Новая, Принято в работу, Выполнено)
    """
    user_apps = Application.objects.filter(user=request.user).select_related('category')

    # Подсчет количества заявок по статусам для бейджей фильтрации
    total_count = user_apps.count()
    new_count = user_apps.filter(status=Application.STATUS_NEW).count()
    in_progress_count = user_apps.filter(status=Application.STATUS_IN_PROGRESS).count()
    completed_count = user_apps.filter(status=Application.STATUS_COMPLETED).count()

    # Применение фильтра
    current_filter = request.GET.get('status', 'all')
    if current_filter in [Application.STATUS_NEW, Application.STATUS_IN_PROGRESS, Application.STATUS_COMPLETED]:
        user_apps = user_apps.filter(status=current_filter)

    user_apps = user_apps.order_by('-created_at')

    context = {
        'applications': user_apps,
        'current_filter': current_filter,
        'total_count': total_count,
        'new_count': new_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    return render(request, 'catalog/cabinet.html', context)
```

##### Логика работы «на пальцах» (без заморочек):
1. **Фейсконтроль (`@login_required`):** Если на страницу заглянет гость — декоратор тут же развернет его и отправит авторизоваться.
2. **Только свои заявки:** Первым делом берем из базы заявки, где автор строго равен текущему вошедшему клиенту (`user=request.user`). Чужие заявки клиент не увидит ни при каких обстоятельствах!
3. **Красивые бейджи-счетчики:** Считаем, сколько у пользователя всего заявок, сколько из них новых, сколько в работе и сколько готово. Эти цифры выводятся прямо внутри кнопок фильтров: `[Все (5)]`, `[Новые (2)]`, `[В работе (1)]`, `[Выполнено (2)]`.
4. **Фильтрация в один клик:** Пользователь нажимает на кнопку «Новые» — в строке браузера появляется `?status=new`. Функция считывает этот параметр через `request.GET.get('status')` и оставляет в списке только заявки со статусом `new`. Если параметр пустой или равен `all` — показываются все заявки.
5. **Сортировка:** Новые заявки всегда идут первыми сверху (`order_by('-created_at')`).
6. **Вывод:** Данные отправляются в шаблон `cabinet.html`.

##### Построчный разбор каждой команды:
- `@login_required`:
  - Декоратор проверяет флаг `request.user.is_authenticated`. При `False` возвращает `HTTP 302 Redirect` на `settings.LOGIN_URL` (`/login/?next=/cabinet/`).
- `user_apps = Application.objects.filter(user=request.user).select_related('category')`:
  - Базовый QuerySet. Важнейшая изоляция данных: `user=request.user`. Никакой пользователь не может просмотреть чужие заявки.
  - `select_related('category')` устраняет проблему N+1 запросов, подгружая имена категорий в одном SQL-запросе с заявками.
- `total_count = user_apps.count()` и последующие `.count()`:
  - Вычисляют точные цифры для каждого бейджа через легкие SQL-запросы `COUNT(*)`.
- `current_filter = request.GET.get('status', 'all')`:
  - Извлекает значение GET-параметра `status`. Если параметра нет, значением по умолчанию становится `'all'`.
- `if current_filter in [...]`:
  - Белый список (White List) допустимых значений фильтра. Защищает базу данных от некорректных или вредоносных значений, подставленных вручную в URL.
- `user_apps = user_apps.order_by('-created_at')`:
  - Сортирует итоговый отфильтрованный список от самых свежих к самым старым.
- `return render(request, 'catalog/cabinet.html', context)`:
  - Отрисовывает страницу кабинета с таблицей заявок и активным фильтром.

---

#### 3.3. Функция `create_application_view(request)` — Создание заявки клиентом

```python
@login_required
def create_application_view(request):
    """
    Создание заявки на разработку дизайна интерьера помещения.
    - Все поля обязательны
    - Валидация фото (jpg, jpeg, png, bmp до 2 Мб)
    - Автоматическая временная метка и статус «Новая»
    """
    if request.method == 'POST':
        form = ApplicationCreateForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.status = Application.STATUS_NEW
            application.save()
            messages.success(request, f'Заявка «{application.title}» успешно создана и получила статус «Новая»!')
            return redirect('cabinet')
        else:
            messages.error(request, 'Пожалуйста, проверьте корректность заполнения полей заявки.')
    else:
        form = ApplicationCreateForm()

    return render(request, 'catalog/application_form.html', {'form': form})
```

##### Логика работы «на пальцах» (без заморочек):
1. Клиент нажимает пункт меню «Создать заявку» (метод `GET`) ➔ открывается форма с полями: «Название», «Описание», выпадающий список «Категория» и поле загрузки файла «План помещения».
2. Клиент заполняет поля, прикрепляет план квартиры и жмет «Отправить заявку» (метод `POST`):
   - **Важнейшая деталь:** форма принимает не только текст `request.POST`, но и файл `request.FILES`.
   - Запускается проверка: название заполнено, категория выбрана, файл не тяжелее 2 Мб и имеет правильный формат (jpg, png, bmp).
   - Если всё верно — происходит изящный трюк с **`commit=False`**: мы создаем заявку в памяти компьютера, сервер сам своей рукой подписывает автора (`application.user = request.user`) и ставит статус «Новая» (`STATUS_NEW`). Клиент никак не может подделать автора или поставить статус «Выполнено»!
   - Заявка сохраняется в базу данных SQLite, файл плана сохраняется в папку `media/photos/`.
   - Появляется зеленая плашка об успехе, и клиент перенаправляется в кабинет к списку своих заявок.
   - Если файл был больше 2 Мб или поле пустое — форма подсветит ошибки красным цветом.

##### Построчный разбор каждой команды:
- `form = ApplicationCreateForm(request.POST, request.FILES)`:
  - Инициализирует форму текстом (`POST`) и бинарным потоком загруженного файла (`FILES`).
- `if form.is_valid():`:
  - Проверяет все поля модели и вызывает валидатор файла `validate_photo_file`.
- `application = form.save(commit=False)`:
  - **Что такое `commit=False`?** Метод создает объект модели `Application` в памяти Python, но **НЕ отправляет SQL-запрос `INSERT` в базу данных**. Это нужно потому, что поля `user` (автор) и `status` в форме отсутствуют (их нельзя доверять вводить пользователю!).
- `application.user = request.user`:
  - На сервере принудительно устанавливаем текущего авторизованного пользователя в качестве владельца заявки.
- `application.status = Application.STATUS_NEW`:
  - Гарантируем, что любая созданная заявка получает статус `new` («Новая»).
- `application.save()`:
  - Теперь, когда все обязательные поля заполнены, вызывается финальное сохранение в БД. Django автоматически сохраняет файл в `media/photos/` и генерирует дату создания `created_at`.
- `messages.success(request, f'Заявка «...» успешно создана...!')`:
  - Flash-уведомление для информирования клиента.
- `return redirect('cabinet')`:
  - Перенаправление в кабинет по паттерну PRG (предотвращает повторную отправку при F5).

---

#### 3.4. Функция `delete_application_view(request, pk)` — Безопасное удаление заявки

```python
@login_required
def delete_application_view(request, pk):
    """
    Удаление заявки:
    - Пользователь может удалить ТОЛЬКО свою заявку
    - Удаление возможно ТОЛЬКО если статус «Новая»
    - Обязательное подтверждение действия
    """
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if not application.is_deletable:
        messages.error(
            request,
            'Запрещено! Заявку нельзя удалить, так как её статус уже изменен администратором на «Принято в работу» или «Выполнено».'
        )
        return redirect('cabinet')

    if request.method == 'POST':
        title = application.title
        application.delete()
        messages.success(request, f'Заявка «{title}» была успешно удалена.')
        return redirect('cabinet')

    return render(request, 'catalog/application_confirm_delete.html', {'application': application})
```

##### Логика работы «на пальцах» (без заморочек):
Удаление заявки — операция необратимая, поэтому здесь действуют **три железных правила безопасности**:
1. **Защита от хакеров (IDOR-защита):** Заявка ищется строго с условием `user=request.user`. Если злоумышленник попытается удалить чужую заявку, вручную введя в браузере `http://localhost:8089/application/42/delete/`, система выдаст ошибку `404 Страница не найдена` — для чужака этой заявки просто не существует!
2. **Бизнес-правило ТЗ:** Заявку разрешено удалять **только пока она «Новая»**. Если дизайнер уже взял её в работу или выполнил, удалять её категорически запрещено! В таком случае пользователю покажется красная ошибка, а операция заблокируется.
3. **Двухэтапное подтверждение (защита от случайного клика):**
   - Этап 1 (`GET`): Пользователь нажал кнопку с иконкой урны в таблице. Сервер открывает отдельную страницу подтверждения: *«Вы действительно хотите удалить заявку "Дизайн гостиной"? Это действие нельзя отменить!»* с кнопками «Да, удалить» и «Отмена».
   - Этап 2 (`POST`): Пользователь нажимает «Да, удалить». Отправляется POST-запрос, запись стирается из базы данных, а пользователь возвращается в кабинет с зеленым сообщением об успехе.

##### Построчный разбор каждой команды:
- `application = get_object_or_404(Application, pk=pk, user=request.user)`:
  - Ищет заявку по первичному ключу `pk` И по владельцу `request.user`. Если запись не найдена или принадлежит другому человеку — немедленно выбрасывает исключение `Http404`.
- `if not application.is_deletable:`:
  - Обращение к кастомному свойству модели `Application` (`@property def is_deletable: return self.status == self.STATUS_NEW`).
- `messages.error(request, 'Запрещено! ...')`:
  - Блокирует удаление и сообщает клиенту о нарушении регламента.
- `if request.method == 'POST':`:
  - Проверяет, что пользователь подтвердил удаление отправкой формы с CSRF-токеном.
- `application.delete()`:
  - Выполняет SQL-запрос `DELETE FROM catalog_application WHERE id = ...;` и удаляет привязанный файл изображения с диска.
- `return render(request, 'catalog/application_confirm_delete.html', {'application': application})`:
  - Отрисовывает страницу диалога подтверждения при первом переходе по ссылке (метод `GET`).

---

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

### 3. Контроллеры панели администратора (`catalog/views.py`) — Детальный разбор функций

Файл: [catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_DJANGO_3/design_studio/catalog/views.py)

В рамках Практической работы №2.3 (Функционал администратора) реализовано разграничение прав доступа и 6 управляющих контроллеров:
1. `is_admin(user)` — Функция-предикат для проверки прав сотрудника или суперпользователя.
2. `admin_panel_view(request)` — Сводная панель управления: просмотр всех заявок с фильтрами, статистика и блок категорий.
3. `admin_change_status_in_progress(request, pk)` — Смена статуса заявки «Новая» ➔ «Принято в работу» с обязательным комментарием.
4. `admin_change_status_completed(request, pk)` — Смена статуса «Новая» ➔ «Выполнено» с обязательным прикреплением файла дизайна до 5 Мб.
5. `admin_add_category(request)` — Добавление новой категории помещений с проверкой уникальности.
6. `admin_delete_category(request, pk)` — Каскадное удаление категории и всех сопряженных заявок (`on_delete=models.CASCADE`).

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Application, Category
from .forms import StatusToInProgressForm, StatusToCompletedForm, CategoryForm
```

---

#### 3.1. Функция-предикат `is_admin(user)` и декоратор `@user_passes_test`

```python
def is_admin(user):
    """Проверка прав администратора"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)
```

##### Логика работы «на пальцах» (без заморочек):
Это функция-«вахтер». Она принимает объект пользователя и дает один из двух ответов: `True` (пропускаем) или `False` (вход запрещен).  
Условия для допуска:
1. Пользователь должен быть авторизован (`is_authenticated`).
2. У него должна стоять хотя бы одна из двух галочек администратора: `is_staff` (сотрудник) или `is_superuser` (главный администратор).  
Если обычный клиент (у которого эти флаги равны `False`) попробует зайти на любой URL админки, декоратор `@user_passes_test(is_admin, login_url='login')` не пустит его и перебросит на страницу входа.

##### Построчный разбор:
- `user.is_authenticated`: Исключает анонимных посетителей (гостей сайта).
- `(user.is_staff or user.is_superuser)`: Проверяет системные флаги прав модели `AbstractUser`.
- `@user_passes_test(is_admin, login_url='login')`: Стандартный декоратор безопасности Django. Он оборачивает каждую функцию администратора. Если вызов `is_admin(request.user)` вернул `False`, запрос немедленно прерывается редиректом на `login_url`.

---

#### 3.2. Функция `admin_panel_view(request)` — Главная панель управления

```python
@user_passes_test(is_admin, login_url='login')
def admin_panel_view(request):
    """
    Личный кабинет администратора (панель управления):
    - Просмотр всех заявок с фильтрацией
    - Смена статуса заявок «Новая» -> «Принято в работу» (с комментарием)
    - Смена статуса заявок «Новая» -> «Выполнено» (с фото дизайна)
    - Управление категориями (добавление, удаление с каскадным удалением заявок)
    """
    status_filter = request.GET.get('status', 'all')
    all_apps = Application.objects.select_related('user', 'category').all()

    total_count = all_apps.count()
    new_count = all_apps.filter(status=Application.STATUS_NEW).count()
    in_progress_count = all_apps.filter(status=Application.STATUS_IN_PROGRESS).count()
    completed_count = all_apps.filter(status=Application.STATUS_COMPLETED).count()

    if status_filter in [Application.STATUS_NEW, Application.STATUS_IN_PROGRESS, Application.STATUS_COMPLETED]:
        applications = all_apps.filter(status=status_filter).order_by('-created_at')
    else:
        applications = all_apps.order_by('-created_at')

    categories = Category.objects.all().order_by('name')
    category_form = CategoryForm()

    context = {
        'applications': applications,
        'categories': categories,
        'category_form': category_form,
        'status_filter': status_filter,
        'total_count': total_count,
        'new_count': new_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    return render(request, 'catalog/admin_panel.html', context)
```

##### Логика работы «на пальцах» (без заморочек):
Это главный рабочий пульт администратора студии.  
Когда админ заходит на `/admin-panel/`:
1. Из базы вынимаются **абсолютно все заявки всех клиентов** (в отличие от кабинета клиента, где выборка ограничена `user=request.user`).
2. Чтобы сервер не тормозил, используется жадная загрузка `.select_related('user', 'category')` — одним махом подтягиваются логины авторов и названия категорий.
3. Считаются счетчики для бейджей на кнопках фильтра: сколько всего, новых, в работе и выполненных.
4. Если админ кликнул по фильтру (например, `?status=new`), список заявок фильтруется.
5. Загружается список всех категорий помещений, отсортированный по алфавиту (`order_by('name')`).
6. Создается пустая форма `CategoryForm()` для быстрого добавления новой категории прямо на этой странице.
7. Всё отрисовывается в шаблоне `admin_panel.html`.

##### Построчный разбор каждой команды:
- `all_apps = Application.objects.select_related('user', 'category').all()`:
  - Формирует QuerySet со всеми заявками и выполняет двойной SQL `INNER JOIN` (с таблицей `catalog_user` и `catalog_category`). Это предотвращает десятки лишних запросов к базе.
- `status_filter = request.GET.get('status', 'all')`:
  - Получает выбранный статус из строки браузера.
- `total_count`, `new_count`, `in_progress_count`, `completed_count`:
  - Вычисляют агрегированную статистику через вызовы `.count()`.
- `applications = all_apps.filter(status=status_filter).order_by('-created_at')`:
  - Применяет фильтрацию и сортировку по убыванию даты создания (свежие заявки сверху).
- `categories = Category.objects.all().order_by('name')`:
  - Загружает справочник категорий в алфавитном порядке.
- `category_form = CategoryForm()`:
  - Инициализирует форму для блока создания категории.
- `return render(request, 'catalog/admin_panel.html', context)`:
  - Отрисовывает интерфейс панели управления.

---

#### 3.3. Функция `admin_change_status_in_progress(request, pk)` — Перевод заявки в работу

```python
@user_passes_test(is_admin, login_url='login')
def admin_change_status_in_progress(request, pk):
    """
    Смена статуса заявки с «Новая» на «Принято в работу» с обязательным комментарием.
    """
    application = get_object_or_404(Application, pk=pk)

    if application.status != Application.STATUS_NEW:
        messages.error(request, 'Смена статуса с «Принято в работу» или «Выполнено» невозможна.')
        return redirect('admin_panel')

    if request.method == 'POST':
        form = StatusToInProgressForm(request.POST)
        if form.is_valid():
            application.status = Application.STATUS_IN_PROGRESS
            application.comment = form.cleaned_data['comment']
            application.save()
            messages.success(request, f'Заявка #{application.pk} переведена в статус «Принято в работу».')
        else:
            messages.error(request, 'Для перевода заявки в работу обязательно укажите комментарий.')
    return redirect('admin_panel')
```

##### Логика работы «на пальцах» (без заморочек):
По ТЗ заявку можно взять в работу **только из статуса «Новая»**, и при этом администратор **обязан написать текстовый комментарий** (например, указать имя назначенного дизайнера или уточняющие детали):
1. Находим заявку по номеру `pk`.
2. **Проверка Конечного Автомата (State Machine):** Смотрим текущий статус. Если заявка уже находится в статусе «Принято в работу» или «Выполнено», система выдает ошибку и блокирует смену. Повторно перевести нельзя!
3. Из формы модального окна считываем отправленный текст комментария (`form = StatusToInProgressForm(request.POST)`).
4. Проверяем валидность: комментарий не должен быть пустым!
5. Если комментарий введен:
   - Статус заявки меняется на `in_progress` («Принято в работу»).
   - В поле `comment` записывается текст администратора.
   - Заявка сохраняется в БД (`application.save()`).
   - Клиент в своем личном кабинете сразу увидит этот комментарий и новый статус!
6. Администратор перенаправляется обратно в панель управления с зеленым сообщением об успехе.

##### Построчный разбор каждой команды:
- `application = get_object_or_404(Application, pk=pk)`:
  - Извлекает заявку по её ID либо возвращает 404, если такой записи нет.
- `if application.status != Application.STATUS_NEW:`:
  - Жесткий запрет перехода: статус разрешено менять ТОЛЬКО у новых заявок.
- `form = StatusToInProgressForm(request.POST)`:
  - Связывает форму с отправленным комментарием.
- `application.comment = form.cleaned_data['comment']`:
  - Сохраняет очищенную строку комментария в объект заявки.
- `application.status = Application.STATUS_IN_PROGRESS`:
  - Фиксирует новое состояние заявки в соответствии с ТЗ.
- `application.save()`:
  - Записывает изменения в SQLite (`UPDATE catalog_application SET status = ..., comment = ... WHERE id = ...;`).
- `return redirect('admin_panel')`:
  - Возвращает администратора на страницу панели управления.

---

#### 3.4. Функция `admin_change_status_completed(request, pk)` — Завершение заявки и сдача дизайна

```python
@user_passes_test(is_admin, login_url='login')
def admin_change_status_completed(request, pk):
    """
    Смена статуса заявки с «Новая» на «Выполнено» с обязательным прикреплением изображения дизайна.
    """
    application = get_object_or_404(Application, pk=pk)

    if application.status != Application.STATUS_NEW:
        messages.error(request, 'Смена статуса с «Принято в работу» или «Выполнено» невозможна.')
        return redirect('admin_panel')

    if request.method == 'POST':
        form = StatusToCompletedForm(request.POST, request.FILES)
        if form.is_valid():
            application.status = Application.STATUS_COMPLETED
            application.design_image = form.cleaned_data['design_image']
            application.save()
            messages.success(request, f'Заявка #{application.pk} успешно выполнена и прикреплен дизайн!')
        else:
            messages.error(request, 'Для завершения заявки обязательно загрузите изображение дизайна (jpg, jpeg, png, bmp до 5 Мб).')
    return redirect('admin_panel')
```

##### Логика работы «на пальцах» (без заморочек):
По ТЗ заявку можно завершить **только из статуса «Новая»**, и при этом администратор **обязан прикрепить файл готового дизайн-проекта** (изображение до 5 Мб):
1. Находим заявку по номеру `pk`.
2. Проверяем, что заявка действительно находится в статусе «Новая». Если нет — блокируем смену.
3. Форма считывает прикрепленный файл через `request.FILES`.
4. Серверный валидатор проверяет файл:
   - Файл действительно прикреплен.
   - Размер файла не превышает 5 Мб (5 * 1024 * 1024 байт).
   - Расширение строго из списка: `.jpg`, `.jpeg`, `.png`, `.bmp`.
5. При успешной проверке:
   - Статус меняется на `completed` («Выполнено»).
   - Файл дизайна сохраняется в специальную папку `media/designs/`.
   - В поле `design_image` базы данных записывается путь к файлу.
   - Заявка сохраняется в БД.
   - **Главный эффект:** эта завершенная заявка моментально появляется на Главной странице сайта в блоке «4 последние выполненные работы»!
6. Администратор перенаправляется в панель с уведомлением об успешном выполнении.

##### Построчный разбор каждой команды:
- `form = StatusToCompletedForm(request.POST, request.FILES)`:
  - Инициализация формы с файловым потоком. Если упустить `request.FILES`, картинка не будет получена.
- `if form.is_valid():`:
  - Запускает валидатор `validate_design_file` из `models.py`.
- `application.status = Application.STATUS_COMPLETED`:
  - Устанавливает финальный статус выполнения заявки.
- `application.design_image = form.cleaned_data['design_image']`:
  - Присваивает проверенный графический файл полю `ImageField(upload_to='designs/')`.
- `application.save()`:
  - Django физически сохраняет файл в каталог `media/designs/` и обновляет запись в таблице `catalog_application`.

---

#### 3.5. Функция `admin_add_category(request)` — Создание новой категории

```python
@user_passes_test(is_admin, login_url='login')
def admin_add_category(request):
    """
    Добавление новой категории заявок администратором.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория «{category.name}» успешно добавлена.')
        else:
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, f'Ошибка категории: {e}')
    return redirect('admin_panel')
```

##### Логика работы «на пальцах» (без заморочек):
В панели управления есть блок «Создать категорию»:
1. Администратор пишет название (например, *«Скандинавский стиль»*) и жмет «Добавить».
2. Отправляется POST-запрос.
3. Форма `CategoryForm` проверяет:
   - Поле не пустое.
   - Такой категории еще нет в базе (причем проверка регистронезависимая: если есть *«Кухня»*, добавить *«кухня»* или *«КУХНЯ»* не разрешат).
4. Если название уникальное — категория сохраняется в таблицу `catalog_category`.
5. Показывается зеленая плашка: *«Категория "Скандинавский стиль" успешно добавлена»*.
6. Если была ошибка (например, дубликат) — форма собирает ошибки и выводит их красным цветом.
7. Администратор возвращается в панель управления. Новая категория сразу появляется в выпадающих списках клиентов при создании заявок!

##### Построчный разбор каждой команды:
- `form = CategoryForm(request.POST)`:
  - Загружает введенное название в форму категории.
- `if form.is_valid():`:
  - Вызывает метод `clean_name()`, где выполняется проверка `Category.objects.filter(name__iexact=name).exists()`.
- `category = form.save()`:
  - Записывает новую категорию в базу данных SQLite.
- `for field, errs in form.errors.items():`:
  - Цикл распаковывает ошибки валидации и отправляет их в `messages.error` для вывода в интерфейсе.
- `return redirect('admin_panel')`:
  - Возврат в панель управления.

---

#### 3.6. Функция `admin_delete_category(request, pk)` — Каскадное удаление категории

```python
@user_passes_test(is_admin, login_url='login')
def admin_delete_category(request, pk):
    """
    Удаление категории заявок:
    При удалении категории каскадно удаляются все заявки данной категории.
    """
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = category.name
        apps_count = category.applications.count()
        category.delete()  # Каскадное удаление заявок через on_delete=models.CASCADE
        messages.success(
            request,
            f'Категория «{name}» и все привязанные заявки ({apps_count} шт.) были безвозвратно удалены.'
        )
        return redirect('admin_panel')

    return render(request, 'catalog/category_confirm_delete.html', {'category': category})
```

##### Логика работы «на пальцах» (без заморочек):
Удаление категории — опаснейшая операция, потому что к ней привязаны заявки клиентов:
1. **Каскадное удаление (`CASCADE`):** По ТЗ, если удалить категорию (например, *«Спальня»*), база данных обязана автоматически удалить все заявки, которые были созданы в этой категории. Это обеспечивает строгость целостности данных (не может быть заявки с «пустой» несуществующей категорией).
2. **Двухэтапное подтверждение:**
   - **Этап 1 (`GET`):** Администратор кликает кнопку «Удалить категорию». Система открывает отдельное окно подтверждения `category_confirm_delete.html`: *«Внимание! При удалении категории "Спальня" будут безвозвратно удалены 3 привязанные к ней заявки! Вы уверены?»*.
   - **Этап 2 (`POST`):** Администратор нажимает «Да, удалить категорию».
     - Считаем, сколько заявок сейчас привязано (`apps_count = category.applications.count()`).
     - Вызываем `category.delete()`. СУБД SQLite благодаря правилу `on_delete=models.CASCADE` в модели `Application` автоматически стирает саму категорию и все сопряженные строки из таблицы заявок.
     - Выводим подробное уведомление: *«Категория "Спальня" и все привязанные заявки (3 шт.) были безвозвратно удалены»*.
     - Редирект в панель управления.

##### Построчный разбор каждой команды:
- `category = get_object_or_404(Category, pk=pk)`:
  - Находит категорию по идентификатору `pk`.
- `apps_count = category.applications.count()`:
  - Обращается к обратному связующему менеджеру `applications` (благодаря параметру `related_name='applications'` во внешнем ключе модели `Application`) и вычисляет количество зависимых записей.
- `category.delete()`:
  - Выполняет каскадное удаление на уровне СУБД SQLite.
- `messages.success(...)`:
  - Формирует информационное подтверждение с точным числом удаленных дочерних объектов.
- `return render(request, 'catalog/category_confirm_delete.html', {'category': category})`:
  - Отображает предупреждающий диалог при переходе по ссылке (метод `GET`).

---

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
