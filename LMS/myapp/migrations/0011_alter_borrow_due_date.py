# Generated by Django 4.0.4 on 2022-05-21 15:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_borrow_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 5, 20, 32, 35, 318136)),
        ),
    ]
