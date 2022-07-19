from django.test import TestCase
from django.urls import reverse

from ..forms import User


class UsersFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            first_name='Ivan',
            last_name='Ivanov',
            username='username',
            email='ivan.ivanov@yandex.ru',

        )
        cls.form_data = {
            'first_name': cls.user.first_name,
            'last_name': cls.user.last_name,
            'username': cls.user.username,
            'email': cls.user.email,
        }

    def test_create_user_form(self):
        """Форма создания пользователя работает корректно."""
        self.client.post(
            reverse('users:signup'),
            data=self.form_data,
            follow=True,
        )
        field_name = {
            self.user.first_name: 'first_name',
            self.user.last_name: 'last_name',
            self.user.username: 'username',
            self.user.email: 'email',
        }
        for field, value in field_name.items():
            self.assertEqual(field, self.form_data[value])
