# Generated by Django 2.0.2 on 2018-03-13 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazonapp', '0004_auto_20180313_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
