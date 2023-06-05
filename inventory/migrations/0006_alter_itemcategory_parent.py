# Generated by Django 4.2.1 on 2023-06-05 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_warehouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.itemcategory'),
        ),
    ]
