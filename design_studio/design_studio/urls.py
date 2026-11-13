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
