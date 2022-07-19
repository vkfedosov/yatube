from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class AboutURLTests(TestCase):
    def test_about_page(self):
        """Страница /about/author/ доступна любому пользователю."""
        response = self.client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech_page(self):
        """Страница /about/tech/ доступна любому пользователю."""
        response = self.client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertTemplateUsed(response, template)


class AboutViewsTests(TestCase):
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech'),

        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)
