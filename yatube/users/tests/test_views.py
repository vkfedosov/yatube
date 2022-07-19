from django.test import Client, TestCase
from django.urls import reverse

from ..forms import User


class UsersViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='username',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'users/signup.html': reverse('users:signup'),
            'users/login.html': reverse('users:login'),
            'users/password_change_done.html': reverse(
                'users:password_change_done'
            ),
            'users/password_change_form.html': reverse(
                'users:password_change'
            ),
            'users/password_reset_done.html': reverse(
                'users:password_reset_done'
            ),
            'users/password_reset_form.html': reverse(
                'users:password_reset'
            ),
            'users/password_reset_confirm.html': reverse(
                'users:password_reset_confirm',
                args=('MTA', '62c-50b743b5ddbd6f5432fa')
            ),
            'users/password_reset_complete.html': reverse(
                'users:password_reset_complete'
            ),
            'users/logged_out.html': reverse('users:logout'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
