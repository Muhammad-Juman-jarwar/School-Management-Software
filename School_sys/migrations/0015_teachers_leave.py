# Generated by Django 4.1.7 on 2023-04-09 04:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('School_sys', '0014_teachers_notification_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teachers_Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('Teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='School_sys.teachers')),
            ],
        ),
    ]
