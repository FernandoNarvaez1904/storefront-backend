# Generated by Django 4.2.1 on 2023-06-06 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_warehousestock_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmovementaction',
            name='is_cumulative',
            field=models.BooleanField(default=True),
        ),
    ]
