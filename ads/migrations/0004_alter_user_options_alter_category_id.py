# Generated by Django 4.1 on 2022-08-23 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_alter_location_lat_alter_location_lng'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
