# Generated by Django 4.0.4 on 2022-05-19 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_borrow_book_borrow_book_alter_borrow_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='due_date',
            field=models.DateTimeField(default=datetime.date(2022, 6, 3)),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='issue_date',
            field=models.DateTimeField(default=datetime.date(2022, 5, 19)),
        ),
    ]