# Generated by Django 5.1.4 on 2025-01-22 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_alter_cartitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_books', to='library.book'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to='library.book'),
        ),
    ]
