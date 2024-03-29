# Generated by Django 2.2.16 on 2022-08-22 09:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0023_auto_20220804_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to=settings.AUTH_USER_MODEL, verbose_name='Автор группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(help_text='Описание, которое будет отображаться на странице группы', verbose_name='Описание группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Идентификатор группы, к которому относится пост. Идентификатор должен быть на английском языке в одно слово или, если слов несколько, в формате: snake_case', unique=True, verbose_name='Идентификатор группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='Наименование группы'),
        ),
    ]
