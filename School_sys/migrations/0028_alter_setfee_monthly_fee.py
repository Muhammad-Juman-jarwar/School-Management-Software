# Generated by Django 4.2 on 2023-04-15 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('School_sys', '0027_alter_setfee_exam_fee_alter_setfee_other_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setfee',
            name='monthly_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
