# Generated by Django 5.0.2 on 2024-05-31 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Инструкция Ассистенту')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Инструкция Ассистенту',
                'verbose_name_plural': 'Инструкция Ассистенту',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
