# Generated by Django 5.1.4 on 2025-01-23 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_remove_wishlist_item_alter_wishlist_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
