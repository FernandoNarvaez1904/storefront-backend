# Generated by Django 4.0.5 on 2022-06-06 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_item_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorydocument',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='itemdetail',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='modifystockorder',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='purchasedocument',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='saledocument',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
