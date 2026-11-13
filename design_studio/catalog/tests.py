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
