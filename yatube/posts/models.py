from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Group(models.Model):
    """Модель создание групп для постов."""
    group_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group',
        verbose_name='Автор группы',
        blank=True,
        null=True,
    )
    title = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Наименование группы',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор группы',
        help_text='Идентификатор группы, к которому относится пост. '
                  'Идентификатор должен быть на английском языке в одно слово '
                  'или, если слов несколько, в формате: snake_case',
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Описание, которое будет отображаться на странице группы',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель создание постов."""
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации поста',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор поста',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберете группу, к которой будет относиться пост',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Выберете картинку поста',
        upload_to='posts/',
        blank=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    """Модель для написания комментариев к постам."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Текст поста',
        help_text='Пост, к которому оставлен комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Автор, который оставил комментарий'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст комментария'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Комментарий',
        help_text='Дата публикации комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:30]


class Follow(models.Model):
    """Модель подписок на авторов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Пользователь, который подписывается'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор поста',
        help_text='Автор, но которого подписываются'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Profile(models.Model):
    """Модель настроек профиля."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name='Пользователь',
        help_text='Пользователь, который выбирает аватар'
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        default='default_avatar.png',
        help_text='Выберете картинку для аватара',
        upload_to='posts/avatar',
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватар'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
