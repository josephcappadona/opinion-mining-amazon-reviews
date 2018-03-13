# Generated by Django 2.0.2 on 2018-03-13 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazonapp', '0003_auto_20180313_0619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='amazonapp.Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
