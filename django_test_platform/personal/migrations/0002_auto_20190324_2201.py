# Generated by Django 2.1.7 on 2019-03-24 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='project',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='更新时间'),
        ),
    ]
