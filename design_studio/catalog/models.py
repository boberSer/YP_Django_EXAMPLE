import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_photo_file(file):
    """
    Валидация фото помещения/плана:
    - Разрешенные форматы: jpg, jpeg, png, bmp
    - Максимальный размер: 2 Мб
    """
    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла не должен превышать {max_size_mb} Мб.')

    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    if ext not in valid_extensions:
        raise ValidationError(
            f'Недопустимый формат файла ({ext}). Разрешены только: jpg, jpeg, png, bmp.'
        )


def validate_design_file(file):
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла не должен превышать {max_size_mb} Мб.')

    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    if ext not in valid_extensions:
        raise ValidationError(
            f'Недопустимый формат файла ({ext}). Разрешены только: jpg, jpeg, png, bmp.'
        )


class User(AbstractUser):
    """
    Кастомная модель пользователя с полем ФИО.
    Логин: только латиница и дефис.
    ФИО: только кириллица, дефис и пробелы.
    """
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


class Category(models.Model):
    """
    Категория заявки (например, «3D-дизайн», «2D-дизайн», «Эскиз»).
    При удалении категории каскадно удаляются все связанные заявки.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Application(models.Model):
    """
    Модель заявки на разработку дизайна интерьера.
    """
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_IN_PROGRESS, 'Принято в работу'),
        (STATUS_COMPLETED, 'Выполнено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название заявки'
    )
    description = models.TextField(
        verbose_name='Описание заявки'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Категория заявки'
    )
    photo = models.ImageField(
        upload_to='photos/',
        validators=[validate_photo_file],
        verbose_name='Фото помещения или его план'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Временная метка добавления'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name='Статус заявки'
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий администратора'
    )
    design_image = models.ImageField(
        upload_to='designs/',
        blank=True,
        null=True,
        validators=[validate_design_file],
        verbose_name='Изображение созданного дизайна'
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.pk} {self.title} [{self.get_status_display()}]'

    @property
    def is_deletable(self):
        """Пользователь может удалить только свою заявку со статусом 'Новая'"""
        return self.status == self.STATUS_NEW

    @property
    def can_change_status(self):
        """Смена статуса возможна ТОЛЬКО для статуса 'Новая'"""
        return self.status == self.STATUS_NEW
