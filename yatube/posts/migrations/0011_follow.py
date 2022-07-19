# Generated by Django 2.2.16 on 2022-07-18 08:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0010_auto_20220716_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(help_text='Автор, но которого подписываются', on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор поста')),
                ('user', models.ForeignKey(help_text='Пользователь, который подписывается', on_delete=None, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
    ]
