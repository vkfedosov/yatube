from django.test import TestCase

from ..models import Comment, Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='username')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовая пост',
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            text='Тестовый комментарий',
            author=cls.user,
        )

    def test_models_have_correct_post_name(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = self.post
        expected_post_name = post.text[:15]
        self.assertEqual(expected_post_name, str(post))

    def test_models_have_correct_group_title(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = self.group
        expected_group_title = group.title
        self.assertEqual(expected_group_title, str(group))

    def test_models_have_correct_comment_text(self):
        """Проверяем, что у модели Comment корректно работает __str__."""
        comment = self.comment
        expected_comment_text = comment.text
        self.assertEqual(expected_comment_text, str(comment))

    def test_verbose_name_(self):
        """verbose_name в модели Post в полях совпадает с ожидаемым."""
        post = self.post
        field_verbose = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях модели Post совпадает с ожидаемым."""
        post = self.post
        field_help_text = {
            'text': 'Введите текст поста',
            'pub_date': 'Дата публикации поста',
            'author': 'Автор поста',
            'group': 'Выберете группу, к которой будет относиться пост',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
