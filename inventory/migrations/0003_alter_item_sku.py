# Generated by Django 4.0.5 on 2022-06-02 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_remove_itemdetail_sku_item_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(max_length=255),
        ),
    ]