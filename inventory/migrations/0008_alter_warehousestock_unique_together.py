# Generated by Django 4.2.1 on 2023-06-05 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_stockrecountdocument_warehousestock_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='warehousestock',
            unique_together={('item', 'warehouse')},
        ),
    ]