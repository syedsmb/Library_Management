# Generated by Django 5.1.4 on 2025-01-28 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_alter_book_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='birth_date',
        ),
    ]
