from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post, User


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='username',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.author = User.objects.get(username='username')
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

        cache.clear()

    def test_pages_available_to_client(self):
        """Страницы:
        /
        /posts/<post_id>/
        /group/<slug>/
        /profile/<username>/
        доступны всем пользователям.
        """
        endpoint_names = (
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{self.post.id}/'
        )
        for endpoint in endpoint_names:
            with self.subTest(endpoint):
                response = self.client.get(endpoint)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_to_client(self):
        """Страницы:
        /create/
        /posts/<post_id>/edit/
        /follow/
        /profile/<str:username>/follow/
        /profile/<str:username>/unfollow/
        переправляют анонимного пользователя.
        """
        endpoint_names = (
            '/create/',
            f'/posts/{self.post.id}/edit/',
            '/follow/',
            f'/profile/{self.user.username}/follow/',
            f'/profile/{self.user.username}/unfollow/',
        )
        for endpoint in endpoint_names:
            with self.subTest(endpoint):
                response = self.client.get(endpoint, follow=True)
                self.assertRedirects(response, f'/auth/login/?next={endpoint}')

    def test_post_id_edit_page(self):
        """Страница /posts/<post_id>/edit/ доступна автору поста."""
        if self.authorized_author == self.user:
            response = self.author.get(f'/posts/{self.post.id}/edit/')
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_page(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_non_existing_page(self):
        """Страница /non_existing/ не существует."""
        response = self.client.get('/non_existing/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = [
            (
                ('/',
                 self.authorized_client),
                'posts/index.html'
            ),
            (
                (f'/group/{self.group.slug}/',
                 self.authorized_client),
                'posts/group_list.html'
            ),
            (
                (f'/profile/{self.user.username}/',
                 self.authorized_client),
                'posts/profile.html'
            ),
            (
                (f'/posts/{self.post.id}/',
                 self.authorized_client),
                'posts/post_detail.html'
            ),
            (
                ('/create/',
                 self.authorized_client),
                'posts/create_post.html'
            ),
            (
                (f'/posts/{self.post.id}/edit/',
                 self.authorized_author),
                'posts/create_post.html'
            ),
            (
                ('/follow/',
                 self.authorized_client),
                'posts/follow.html'
            ),
            (
                (f'/profile/{self.user.username}/follow/',
                 self.authorized_client),
                'posts/follow.html'
            ),
            (
                (f'/profile/{self.user.username}/unfollow/',
                 self.authorized_client),
                'posts/unfollow.html'
            ),
        ]
        for (reverse_name, client), template in templates_url_names:
            with self.subTest(reverse_name=reverse_name):
                response = client.get(reverse_name)
                self.assertTemplateUsed(response, template)
