# Generated by Django 5.0.2 on 2024-02-16 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audios', models.FileField(upload_to='audios/', verbose_name='Видео')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Медиа',
                'verbose_name_plural': 'Медиа',
            },
        ),
    ]