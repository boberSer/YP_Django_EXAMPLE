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
