# Полное пошаговое руководство по проекту «Design.pro» на Django (в стиле MDN Web Docs)

> Данное руководство составлено по аналогии с официальным учебным курсом **MDN (Mozilla Developer Network) Django Tutorial** («Местная библиотека / LocalLibrary»).  
> В нем подробно разобрана теория архитектуры Django (MVT), жизненный цикл HTTP-запроса, сборка шаблонов, структура медиа-хранилища, исходный код каждого модуля и подготовлены готовые ответы для успешной защиты перед преподавателем.

---

## Быстрые ссылки на ключевые файлы проекта:
- 📄 Главные настройки: [design_studio/settings.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/design_studio/settings.py)
- 🗄 Модели базы данных: [catalog/models.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/models.py)
- 📝 Формы и серверная валидация: [catalog/forms.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/forms.py)
- ⚙️ Контроллеры и бизнес-логика: [catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/views.py)
- 🧭 Маршрутизация приложения: [catalog/urls.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/urls.py)
- 🌐 Главные маршруты проекта: [design_studio/urls.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/design_studio/urls.py)
- 🛡 Регистрация в админке: [catalog/admin.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/admin.py)
- 🧪 Автоматические тесты (6 тестов): [catalog/tests.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/tests.py)

### Шаблоны интерфейса (Templates):
- 🧱 Базовый каркас сайта: [templates/base.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/base.html)
- 🏠 Главная страница (счетчик и 4 работы): [templates/index.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/index.html)
- 👤 Личный кабинет (фильтры, таблица, удаление): [templates/catalog/cabinet.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/cabinet.html)
- ✍️ Создание заявки: [templates/catalog/application_form.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/application_form.html)
- 🗑 Подтверждение удаления заявки: [templates/catalog/application_confirm_delete.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/application_confirm_delete.html)
- 🛠 Панель администратора (заявки + категории): [templates/catalog/admin_panel.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/catalog/admin_panel.html)
- 🚪 Вход в аккаунт: [templates/registration/login.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/registration/login.html)
- 📋 Регистрация (серверная подсветка ошибок): [templates/registration/register.html](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/templates/registration/register.html)

---

## 1. Теоретический фундамент: Архитектура Django и паттерн MVT

Django основан на архитектурном шаблоне **MVT (Model-View-Template)**, представляющем собой развитие паттерна MVC:

```
 Пользователь (Браузер)
      │ ▲
      │ │ 5. HTTP-ответ (HTML-страница с данными)
      ▼ │
┌────────────────────────────────────────────────────────┐
│                        DJANGO                          │
│                                                        │
│  1. URLconf (urls.py)                                  │
│     Маршрутизатор: сопоставляет URL с контроллером     │
│            │                                           │
│            ▼                                           │
│  2. View (views.py) ── [Контроллер бизнес-логики]      │
│            │                             ▲             │
│            │ 3. Запрос данных            │ Данные      │
│            ▼                             │             │
│  3. Model (models.py) ◄──────────────────┘             │
│     ORM и База данных SQLite                           │
│            │                                           │
│            │ 4. Передача контекста                     │
│            ▼                                           │
│  4. Template (templates/*.html)                        │
│     Рендеринг HTML с использованием языка тегов DTL    │
└────────────────────────────────────────────────────────┘
```

### Разбор компонентов MVT:
1. **Model (Модель):** Описывает структуру базы данных на чистом Python (класс `models.Model`). Django ORM (Object-Relational Mapping) автоматически транслирует методы Python (`.filter()`, `.create()`, `.delete()`) в SQL-запросы к СУБД SQLite.
2. **View (Представление / Контроллер):** Функция или класс, принимающий объект запроса `HttpRequest` и возвращающий `HttpResponse`. Здесь выполняется проверка прав доступа, валидация бизнес-правил и выборка данных.
3. **Template (Шаблон):** Текстовый файл (HTML), содержащий разметку страницы и теги языка DTL (Django Template Language).

---

## 2. Архитектура хранилища `media`: почему `photos/` и `designs/`

В проекте настроена простая, логичная и практичная структура медиафайлов:
```
media/
├── photos/    <-- Планы помещений и фото комнат от заказчиков (до 2 Мб)
└── designs/   <-- Готовые дизайн-проекты и визуализации от администратора
```

### Как обосновать преподавателю это решение:
- **Принцип единственной ответственности (Separation of Concerns):**  
  Входящие файлы пользователей (чертежи, замеры) и результаты работы студии (3D-рендеры, эскизы) — это две абсолютно разные сущности. Хранить их в одной куче недопустимо.
- **Почему не использовалась разбивка по датам (`%Y/%m/%d/`):**  
  В промышленных системах с миллионами файлов разбивка по годам и месяцам необходима для преодоления лимитов файловой системы на число файлов в одном каталоге (`inode limits`). В рамках учебного проекта разбивка по годам создает пустые вложенные папки, усложняя ручную проверку. Разделение на `media/photos/` и `media/designs/` обеспечивает стопроцентную прозрачность: преподаватель открывает папку и сразу видит, где лежат исходники, а где — результат работы студии.

---

## 3. Сборка и устройство шаблонов (Templates)

### Как Django находит шаблоны:
В файле [settings.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/design_studio/settings.py) указано:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Искать в корневой папке templates/
        'APP_DIRS': True,                  # Искать внутри каждого приложения
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',     # Доступ к {{ user }}
                'django.contrib.messages.context_processors.messages', # Доступ к {{ messages }}
                'django.template.context_processors.media',        # Доступ к {{ MEDIA_URL }}
            ],
        },
    },
]
```

### Принцип наследования шаблонов (Template Inheritance):
1. **Базовый каркас (`templates/base.html`):**  
   Задает общую разметку HTML5, подключает CSS/JS фреймворка Bootstrap 5, выводит верхнее меню навигации, блок системных уведомлений и футер. В месте для изменяемого контента объявляется блок:
   ```html
   <main class="container">
       {% block content %}{% endblock %}
   </main>
   ```
2. **Дочерние шаблоны (`index.html`, `cabinet.html` и др.):**  
   Начинаются со строки `{% extends 'base.html' %}` и переопределяют блок `{% block content %}`. Это избавляет от дублирования разметки и обеспечивает принцип **DRY (Don't Repeat Yourself)**.

### Теги и фильтры языка шаблонов DTL:
- `{% csrf_token %}` — внедряет скрытый токен защиты от CSRF-атак. Обязателен для всех форм, отправляющих POST-запрос.
- `{% url 'имя_маршрута' %}` — генерирует абсолютную ссылку по имени маршрута из `urls.py`. Если изменится URL в маршрутизаторе, верстка останется рабочей.
- `{{ user.is_authenticated }}` — булево значение: авторизован ли пользователь.
- `{{ user.is_staff }}` — булево значение: является ли пользователь администратором.
- `{{ app.created_at|date:"d.m.Y H:i" }}` — фильтр форматирования даты и времени.
- `{% if form.field.errors %} is-invalid {% endif %}` — добавление Bootstrap-класса ошибки к полю ввода.

---

## 4. Пошаговая реализация проекта

### Шаг 4.1. Модели базы данных ([catalog/models.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/models.py))

```python
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings

# Валидатор фото: ограничение 2 Мб и строго форматы jpg, jpeg, png, bmp
def validate_photo_file(file):
    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла не должен превышать {max_size_mb} Мб.')
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
        raise ValidationError(f'Недопустимый формат файла ({ext}). Разрешены только: jpg, jpeg, png, bmp.')

# Кастомная модель пользователя с полем ФИО
class User(AbstractUser):
    fio = models.CharField(max_length=150, verbose_name='ФИО')

# Категория заявки (например, «3D-дизайн», «2D-дизайн», «Эскиз»)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    def __str__(self):
        return self.name

# Модель заявки на дизайн
class Application(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_IN_PROGRESS, 'Принято в работу'),
        (STATUS_COMPLETED, 'Выполнено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    title = models.CharField(max_length=200, verbose_name='Название заявки')
    description = models.TextField(verbose_name='Описание заявки')
    
    # КАСКАДНОЕ УДАЛЕНИЕ: при удалении категории удаляются все привязанные заявки!
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='applications')
    photo = models.ImageField(upload_to='photos/', validators=[validate_photo_file])
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    comment = models.TextField(blank=True, null=True)
    design_image = models.ImageField(upload_to='designs/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_deletable(self):
        # Удалять разрешено только заявку в статусе "Новая"
        return self.status == self.STATUS_NEW

    @property
    def can_change_status(self):
        # Смена статуса разрешена только из статуса "Новая"
        return self.status == self.STATUS_NEW
```

---

### Шаг 4.2. Формы и серверная валидация ([catalog/forms.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/forms.py))

```python
import re
from django import forms
from django.core.exceptions import ValidationError
from .models import User, Application

class UserRegistrationForm(forms.ModelForm):
    fio = forms.CharField(label='ФИО', required=True)
    username = forms.CharField(label='Логин', required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput, required=True)
    agree_data_processing = forms.BooleanField(label='Согласие на обработку данных', required=True)

    class Meta:
        model = User
        fields = ['fio', 'username', 'email', 'password']

    # Проверка ФИО: только кириллические буквы, дефис и пробелы
    def clean_fio(self):
        fio = self.cleaned_data.get('fio', '').strip()
        if not re.fullmatch(r'^[а-яА-ЯёЁ\s-]+$', fio):
            raise ValidationError('ФИО может содержать только кириллические буквы, дефис и пробелы.')
        return fio

    # Проверка Логина: только латинские буквы и дефис
    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not re.fullmatch(r'^[a-zA-Z-]+$', username):
            raise ValidationError('Логин может содержать только латинские буквы и дефис.')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует.')
        return username

    # Проверка совпадения двух введенных паролей
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', 'Пароли не совпадают.')
        return cleaned_data

    # Хеширование пароля через PBKDF2 перед сохранением в БД
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
```

---

### Шаг 4.3. Представления ([catalog/views.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/catalog/views.py))

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Application, Category

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# 1. Главная страница
def index(request):
    in_progress_count = Application.objects.filter(status='in_progress').count()
    completed_apps = Application.objects.filter(status='completed').order_by('-created_at')[:4]
    return render(request, 'index.html', {
        'in_progress_count': in_progress_count,
        'completed_apps': completed_apps,
    })

# 2. Личный кабинет пользователя с фильтрацией
@login_required
def cabinet_view(request):
    user_apps = Application.objects.filter(user=request.user)
    current_filter = request.GET.get('status', 'all')
    if current_filter in ['new', 'in_progress', 'completed']:
        user_apps = user_apps.filter(status=current_filter)
    
    return render(request, 'catalog/cabinet.html', {
        'applications': user_apps.order_by('-created_at'),
        'current_filter': current_filter,
        'total_count': Application.objects.filter(user=request.user).count(),
        'new_count': Application.objects.filter(user=request.user, status='new').count(),
        'in_progress_count': Application.objects.filter(user=request.user, status='in_progress').count(),
        'completed_count': Application.objects.filter(user=request.user, status='completed').count(),
    })

# 3. Безопасное удаление заявки
@login_required
def delete_application_view(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if not application.is_deletable:
        messages.error(request, 'Удалить можно только заявку со статусом «Новая».')
        return redirect('cabinet')
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Заявка успешно удалена.')
        return redirect('cabinet')
    return render(request, 'catalog/application_confirm_delete.html', {'application': application})

# 4. Панель управления администратора
@user_passes_test(is_admin, login_url='login')
def admin_panel_view(request):
    status_filter = request.GET.get('status', 'all')
    apps = Application.objects.all()
    if status_filter in ['new', 'in_progress', 'completed']:
        apps = apps.filter(status=status_filter)
    
    return render(request, 'catalog/admin_panel.html', {
        'applications': apps.order_by('-created_at'),
        'categories': Category.objects.all(),
        'status_filter': status_filter,
        'total_count': Application.objects.count(),
        'new_count': Application.objects.filter(status='new').count(),
        'in_progress_count': Application.objects.filter(status='in_progress').count(),
        'completed_count': Application.objects.filter(status='completed').count(),
    })
```

---

### Шаг 4.4. Маршрутизация ([design_studio/urls.py](file:///C:/Users/fer/PycharmProjects/YP_Django_3/design_studio/design_studio/urls.py))

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # По ТЗ: Административная панель доступна по адресу /superadmin
    path('superadmin/', admin.site.urls),
    path('', include('catalog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 5. Запуск проекта и тестирование

1. Откройте консоль и активируйте виртуальное окружение:
   ```powershell
   cd C:\Users\fer\PycharmProjects\YP_Django_3\design_studio
   ..\.venv\Scripts\Activate.ps1
   ```
2. Запустите 6 автоматических тестов:
   ```powershell
   python manage.py test
   ```
   Все 6 тестов должны завершиться с результатом `OK`.
3. Запустите сервер разработки на порту **8089**:
   ```powershell
   python manage.py runserver 8089
   ```
4. Проверьте в браузере:
   - Главная: [http://localhost:8089/](http://localhost:8089/)
   - Админка: [http://localhost:8089/superadmin](http://localhost:8089/superadmin) (логин `admin`, пароль `admin`).

---

## 6. ТОП-20 вопросов для защиты перед преподавателем

1. **Вопрос:** Что означает аббревиатура MVT в Django?  
   **Ответ:** Model (структура базы данных и ORM), View (контроллер логики обработки запросов), Template (HTML-шаблоны отображения).
2. **Вопрос:** Почему мы создали кастомную модель `User` через `AbstractUser`?  
   **Ответ:** Это позволило добавить обязательное поле ФИО прямо в основную таблицу учетных записей. Это быстрее и архитектурно чище, чем делать отдельную таблицу `UserProfile` через `OneToOneField`, требующую постоянных SQL `JOIN`.
3. **Вопрос:** Как обеспечивается уникальность логина?  
   **Ответ:** На уровне БД через ограничение `UNIQUE` поля `username` и на уровне формы в методе `clean_username()`.
4. **Вопрос:** Как реализовано ограничение на размер файла 2 МБ?  
   **Ответ:** В функции `validate_photo_file` проверяется `file.size > 2 * 1024 * 1024`. Если размер превышен, возбуждается исключение `ValidationError`.
5. **Вопрос:** Что происходит с заявками при удалении категории?  
   **Ответ:** В модели `Application` во внешнем ключе на категорию объявлено `on_delete=models.CASCADE`. СУБД SQLite автоматически удаляет все связанные с категорией заявки.
6. **Вопрос:** Почему пользователь не может удалить чужую заявку?  
   **Ответ:** В контроллере `delete_application_view` запрос выполняется как `get_object_or_404(Application, pk=pk, user=request.user)`. Запрос отфильтрован строго по текущему пользователю; чужой ID вернет ошибку 404.
7. **Вопрос:** Почему пользователь не может удалить заявку со статусом «В работе»?  
   **Ответ:** В контроллере проверяется свойство модели `application.is_deletable` (`status == 'new'`). Если заявка уже взята в работу, удаление программно пресекается.
8. **Вопрос:** Как устроен счетчик заявок в работе на главной?  
   **Ответ:** Метод `Application.objects.filter(status='in_progress').count()` формирует оптимизированный SQL-запрос `SELECT COUNT(*)`, не загружая сами объекты в память.
9. **Вопрос:** Как на главной странице выводится не более 4 выполненных заявок?  
   **Ответ:** Срез `[:4]` в Django ORM транслируется в SQL-директиву `LIMIT 4`.
10. **Вопрос:** Почему со статуса «В работе» или «Выполнено» нельзя повторно сменить статус?  
    **Ответ:** По ТЗ смена разрешена только из статуса «Новая». В контроллерах проверяется `if application.status != Application.STATUS_NEW: return redirect('admin_panel')`.
11. **Вопрос:** Зачем нужен `{% csrf_token %}` в формах?  
    **Ответ:** Для защиты от атак межсайтовой подделки запросов (CSRF). Django сверяет криптографический токен формы с токеном в сессии.
12. **Вопрос:** Как подсвечиваются поля с ошибками при регистрации?  
    **Ответ:** В шаблоне проверяется `{% if form.field.errors %}` и тегу `<input>` добавляется класс `is-invalid`, а под ним выводится `<div class="invalid-feedback">` с текстом ошибки.
13. **Вопрос:** Как разделены права гостей, пользователей и администратора?  
    **Ответ:** Гости определяются через `not user.is_authenticated`, клиенты — через `user.is_authenticated`, администраторы — через декоратор `@user_passes_test(is_admin)` с проверкой `is_staff` / `is_superuser`.
14. **Вопрос:** Как работает фильтрация по статусу в кабинете?  
    **Ответ:** Через GET-параметр `?status=...`. Представление считывает `request.GET.get('status')` и применяет `.filter(status=current_filter)`.
15. **Вопрос:** Почему адрес админки перенесен на `/superadmin`?  
    **Ответ:** Это требование ТЗ ("Инструкция для студента"). Мы переопределили маршрут в файле `design_studio/urls.py`.
16. **Вопрос:** В каком виде хранятся пароли пользователей?  
    **Ответ:** Пароли хешируются с солью криптографическим алгоритмом PBKDF2-SHA256 через метод `user.set_password()`.
17. **Вопрос:** Как Django отдает загруженные картинки при разработке?  
    **Ответ:** Через вспомогательную функцию `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` при `DEBUG=True`.
18. **Вопрос:** В чем разница между `makemigrations` и `migrate`?  
    **Ответ:** `makemigrations` создает Python-файл миграции с описанием изменений схемы, а `migrate` применяет эти изменения к реальной базе данных.
19. **Вопрос:** Зачем мы выделили две папки в media (`photos/` и `designs/`)?  
    **Ответ:** Для логического разделения входных пользовательских планов от выходных результатов работы дизайнеров студии.
20. **Вопрос:** Как устроен поиск шаблонов в проекте?  
    **Ответ:** По списку путей в `TEMPLATES['DIRS']` (в нашем проекте это `BASE_DIR / 'templates'`), а также внутри каждого установленного приложения благодаря параметру `APP_DIRS: True`.
