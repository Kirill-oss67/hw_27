# Generated by Django 4.1 on 2022-09-13 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='default_name', max_length=100),
        ),
    ]
