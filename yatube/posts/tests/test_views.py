import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import CommentForm, PostForm
from ..models import Comment, Follow, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='username',
        )
        cls.user_2 = User.objects.create(
            username='username 2',
        )
        cls.user_3 = User.objects.create(
            username='username 3',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='slug_2',
            description='Тестовое описание 2',
        )
        cls.create_image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='test_image.gif',
            content=cls.create_image,
            content_type='posts/images/',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
            image=cls.uploaded,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            text='Тестовый комментарий',
            author=cls.user,
        )
        cls.follow = Follow.objects.create(
            user=cls.user_2,
            author=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.author = User.objects.get(username='username')
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

        self.authorized_client_follow = Client()
        self.authorized_client_follow.force_login(self.user_2)

        self.authorized_client_unfollow = Client()
        self.authorized_client_unfollow.force_login(self.user_3)

        cache.clear()

    def test_pages_uses_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = [
            (
                (reverse('posts:index'),
                 self.authorized_client),
                'posts/index.html'
            ),
            (
                (reverse('posts:group_list', args=(self.group.slug,)),
                 self.authorized_client),
                'posts/group_list.html'
            ),
            (
                (reverse('posts:profile', args=(self.user.username,)),
                 self.authorized_client),
                'posts/profile.html'
            ),
            (
                (reverse('posts:post_detail', args=(self.post.id,)),
                 self.authorized_client),
                'posts/post_detail.html'
            ),
            (
                (reverse('posts:post_create'),
                 self.authorized_client),
                'posts/create_post.html'
            ),
            (
                (reverse('posts:post_edit', args=(self.post.id,)),
                 self.authorized_author),
                'posts/create_post.html'
            ),
            (
                (reverse('posts:follow_index'),
                 self.authorized_client),
                'posts/follow.html'
            ),
            (
                (reverse('posts:profile_follow', args=(self.user.username,)),
                 self.authorized_client),
                'posts/follow.html'
            ),
            (
                (reverse('posts:profile_unfollow', args=(self.user.username,)),
                 self.authorized_client),
                'posts/unfollow.html'
            ),

        ]
        for (reverse_name, client), template in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_context(self, context_obj):
        """Проверка контекста страниц."""
        self.assertEqual(context_obj.text, self.post.text)
        self.assertEqual(context_obj.group.title, self.group.title)
        self.assertEqual(context_obj.group.slug, self.group.slug)
        self.assertEqual(context_obj.group.description, self.group.description)
        self.assertEqual(context_obj.image, self.post.image)

    def test_index_page_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        page_obj = response.context['page_obj'][0]
        self.check_context(page_obj)

    def test_group_list_page_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,))
        )
        page_obj = response.context['page_obj'][0]
        self.check_context(page_obj)

    def test_profile_page_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', args=(self.user.username,))
        )
        author_obj = response.context['author']
        post_author = author_obj.username
        self.assertEqual(post_author, self.user.username)

        page_obj = response.context['page_obj'][0]
        self.check_context(page_obj)

    def test_post_detail_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', args=(self.post.id,))
        )
        post_obj = response.context['post']
        self.check_context(post_obj)
        self.assertIsInstance(response.context['form'], CommentForm)

    def test_post_create_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_edit_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', args=(self.post.id,))
        )
        self.assertIsInstance(response.context['form'], PostForm)

    def test_follow_index_context(self):
        """Шаблон follow_index сформирован с правильным контекстом."""
        Follow.objects.create(
            user=self.user,
            author=self.author
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        page_obj = response.context['page_obj'][0]
        self.check_context(page_obj)

    def test_profile_unfollow_context(self):
        """Шаблон profile_unfollow сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile_unfollow', args=(self.user.username,))
        )
        author_obj = response.context['author']
        post_author = author_obj.username
        self.assertEqual(post_author, self.user.username)

    def test_paginator(self):
        """Шаблоны index, group_list, profile сформированы с правильным
         количеством постов на странице.
         """
        posts = [Post(
            text=f'Тестовый пост {i}',
            author=self.user,
            group=self.group
        )
            for i in range(12)]

        Post.objects.bulk_create(posts)

        pages_with_paginator = {
            reverse('posts:index'),
            reverse('posts:group_list', args=(self.group.slug,)),
            reverse('posts:profile', args=(self.user.username,)),
        }
        for reverse_name in pages_with_paginator:
            response = self.client.get(reverse_name + '?page=1')
            self.assertEqual(len(response.context['page_obj']), 10)
            response = self.client.get(reverse_name + '?page=2')
            self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_post(self):
        """Пост отображается на страницах index, group_list, profile
        и соответствует своей группе.
        """
        group_post_name = {
            reverse('posts:index'),
            reverse('posts:group_list', args=(self.group.slug,)),
            reverse('posts:profile', args=(self.user.username,)),
        }
        for reverse_name in group_post_name:
            response = self.authorized_client.get(reverse_name)
            page_obj = response.context['page_obj']
            for post in page_obj:
                with self.subTest():
                    self.assertEqual(post.group, self.group)
                    self.assertNotEqual(post.group, self.group_2)

    def test_profile_page(self):
        """На странице profile нет постов другого автора."""
        response = self.authorized_author.get(
            reverse('posts:profile', args=(self.user.username,))
        )
        page_obj = response.context['page_obj'][0]
        self.assertEqual(self.user.username, page_obj.author.username)
        self.assertEqual(self.group, page_obj.group)
        self.assertNotEqual(self.user_2.username, page_obj.author.username)
        self.assertNotEqual(self.group_2, page_obj.group)

    def test_create_comment(self):
        """Комментарий к посту может оставлять только авторизованный
        пользователь.
        """
        response = self.authorized_client.get(
            reverse('posts:post_detail', args=(self.post.id,))
        )
        comment_obj = response.context['comments'][0]
        self.assertEqual(self.comment.text, comment_obj.text)

    def test_index_page_cache(self):
        """Список постов на странице index хранится в кэше и обновляется раз в
        20 секунд.
        """
        response_empty_page = self.client.get(reverse('posts:index'))
        Post.objects.create(
            text='Тестовый пост',
            author=self.user,
            group=self.group,
            image=self.uploaded,
        )
        response_page_with_post = self.client.get(reverse('posts:index'))
        self.assertEqual(
            response_page_with_post.content,
            response_empty_page.content
        )
        cache.clear()
        response_after_clear_cache = self.client.get(reverse('posts:index'))
        self.assertNotEqual(
            response_after_clear_cache.content,
            response_empty_page.content
        )

    def test_check_followers(self):
        """Авторизованный пользователь может подписываться на других
        пользователей и удалять их из подписок.
        """
        followers_count_with_sub = Follow.objects.count()
        Follow.objects.filter(
            user=self.user_2,
            author=self.user,
        ).delete()
        count_followers_without_sub = Follow.objects.count()
        self.assertEqual(
            followers_count_with_sub,
            count_followers_without_sub + 1
        )

    def test_post_for_followers(self):
        """Новая запись пользователя появляется в ленте тех, кто на него
        подписан и не появляется в ленте тех, кто не подписан.
        """
        response = self.authorized_client_follow.get(
            reverse('posts:follow_index')
        )
        page_obj = response.context['page_obj']
        self.assertIn(self.post, page_obj)

        response = self.authorized_client_unfollow.get(
            reverse('posts:follow_index')
        )
        page_obj = response.context['page_obj']
        self.assertNotIn(self.post, page_obj)
