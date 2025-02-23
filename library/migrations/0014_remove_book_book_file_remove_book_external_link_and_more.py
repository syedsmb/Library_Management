# Generated by Django 5.1.4 on 2025-01-27 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_alter_book_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_file',
        ),
        migrations.RemoveField(
            model_name='book',
            name='external_link',
        ),
        migrations.AddField(
            model_name='book',
            name='discounted_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='book',
            name='original_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
