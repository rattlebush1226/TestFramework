# Generated by Django 5.1.7 on 2025-03-19 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0004_testcase_date_input_testcase_timestamp_output'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='date_input',
            field=models.DateTimeField(blank=True, null=True, verbose_name='日期输入'),
        ),
    ]
