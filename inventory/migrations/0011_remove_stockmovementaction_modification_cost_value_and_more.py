# Generated by Django 4.2.2 on 2023-06-11 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_stockmovementaction_parent_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockmovementaction',
            name='modification_cost_value',
        ),
        migrations.RemoveField(
            model_name='stockmovementaction',
            name='modification_price_value',
        ),
    ]