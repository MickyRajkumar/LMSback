# Generated by Django 4.0.4 on 2022-05-19 18:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_borrow_due_date_alter_borrow_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='issue_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]