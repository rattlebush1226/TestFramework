# Generated by Django 5.1.7 on 2025-03-08 04:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST')], max_length=10)),
                ('headers', models.TextField(blank=True)),
                ('body', models.TextField(blank=True)),
                ('expected_response', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_time', models.DateTimeField(auto_now_add=True)),
                ('is_success', models.BooleanField()),
                ('actual_response', models.TextField()),
                ('error_message', models.TextField(blank=True)),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tester.testcase')),
            ],
        ),
    ]
