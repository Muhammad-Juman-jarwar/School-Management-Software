# Generated by Django 4.1.7 on 2023-03-29 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('School_sys', '0003_teachers'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='Father_Name',
            field=models.CharField(default='add', max_length=100),
        ),
    ]
