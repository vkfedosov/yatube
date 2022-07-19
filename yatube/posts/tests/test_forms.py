import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='username',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
        )
        cls.image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='test_image.gif',
            content=cls.image,
            content_type='posts/images/',
        )
        cls.post_create_form_data = {
            'text': 'Тестовый пост',
            'group': cls.group.id,
        }
        cls.group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='slug_2',
        )
        cls.post_edit_form_data = {
            'text': 'Тестовый пост 2',
            'group': cls.group_2.id,
        }
        cls.create_post_with_image_form_data = {
            'text': 'Тестовый пост',
            'group': cls.group.id,
            'image': cls.uploaded,
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.author = User.objects.get(username='username')
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

    def post_create(self, reverse_page, form_data):
        """Создание поста."""
        return self.authorized_author.post(
            reverse_page,
            data=form_data,
            follow=True,
        )

    def test_create_post_form(self):
        """Форма создания поста работает корректно."""
        post_count_before_creations = Post.objects.count()
        response = self.post_create(reverse('posts:post_create'),
                                    self.post_create_form_data)
        post_count_after_creations = Post.objects.count()
        post = Post.objects.last()
        self.assertRedirects(
            response,
            reverse('posts:profile', args=('username',))
        )
        self.assertEqual(
            post_count_after_creations,
            post_count_before_creations + 1
        )
        self.assertEqual(self.post_create_form_data['text'], post.text)
        self.assertEqual(self.post_create_form_data['group'], post.group.id)

    def test_edit_post_form(self):
        """Форма редактирования поста работает корректно."""
        self.post_create(reverse('posts:post_create'),
                         self.post_create_form_data)
        post_count_before_edit = Post.objects.count()
        post = Post.objects.first()
        response = self.post_create(
            reverse('posts:post_edit', args=(post.id,)),
            self.post_edit_form_data)
        post_count_after_edit = Post.objects.count()
        post_edited = Post.objects.first()
        self.assertRedirects(
            response,
            reverse('posts:post_detail', args=(post.id,))
        )
        self.assertEqual(post_count_before_edit, post_count_after_edit)
        self.assertEqual(self.post_edit_form_data['text'], post_edited.text)
        self.assertEqual(
            self.post_edit_form_data['group'],
            post_edited.group.id
        )

    def test_create_post_with_image(self):
        """Форма создания поста с картинкой работает корректно."""
        self.post_create(reverse('posts:post_create'),
                         self.create_post_with_image_form_data)
        post = Post.objects.first()
        self.assertEqual(f'posts/images/{self.uploaded}', post.image)
