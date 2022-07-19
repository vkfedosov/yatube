from http import HTTPStatus

from django.test import Client, TestCase

from ..forms import User


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='username',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_available_to_client(self):
        """Страницы:
        /auth/signup/
        /auth/login/
        /auth/logout/
        /auth/password_reset/done/
        /auth/password_reset/
        /auth/reset/done/
        доступны всем пользователям.
        """
        endpoint_names = (
            '/auth/signup/',
            '/auth/login/',
            '/auth/logout/',
            '/auth/password_reset/done/',
            '/auth/password_reset/',
            '/auth/reset/done/',
        )
        for endpoint in endpoint_names:
            with self.subTest(endpoint):
                response = self.client.get(endpoint)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_available_to_authorized_client(self):
        """Страницы:
        /auth/password_change/done/
        /auth/password_change/
        /auth/reset/<uidb64>/<token>/
        доступны авторизованным пользователям.
        """
        endpoint_names = (
            '/auth/password_change/done/',
            '/auth/password_change/',
            '/auth/reset/MTA/62c-50b743b5ddbd6f5432fa/',
        )
        for endpoint in endpoint_names:
            with self.subTest(endpoint):
                response = self.authorized_client.get(endpoint)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_done_page_redirect(self):
        """Страница /auth/password_change/done/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.client.get(
            '/auth/password_change/done/',
            follow=True
        )
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password_change/done/'
        )

    def test_password_change_page_redirect(self):
        """Страница по адресу /auth/password_change/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.client.get('/auth/password_change/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password_change/'
        )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'users/signup.html': '/auth/signup/',
            'users/login.html': '/auth/login/',
            'users/password_change_done.html': '/auth/password_change/done/',
            'users/password_change_form.html': '/auth/password_change/',
            'users/password_reset_done.html': '/auth/password_reset/done/',
            'users/password_reset_form.html': '/auth/password_reset/',
            'users/password_reset_confirm.html':
                '/auth/reset/MTA/62c-50b743b5ddbd6f5432fa/',
            'users/password_reset_complete.html': '/auth/reset/done/',
            'users/logged_out.html': '/auth/logout/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
