# Generated by Django 3.2.16 on 2025-01-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='Posts_images', verbose_name='Фото'),
        ),
    ]
