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
    completed_apps = Application.objects.filter(status=Application.STATUS_COMPLETED).select_related('category').order_by('-created_at')[:4]

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

    return render(request, 'register/login.html', {'form': form})


def logout_view(request):
    """
    Выход из учетной записи для всех авторизованных пользователей.
    """
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('index')


@login_required
def cabinet_view(request):
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
