# Generated by Django 2.2.16 on 2022-07-19 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20220719_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Картинка прикрепленная к посту', upload_to='posts/', verbose_name='Картинка'),
        ),
    ]
