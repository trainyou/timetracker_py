# Generated by Django 4.1.3 on 2023-03-28 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0003_daily_records_assignments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_records',
            name='assignments',
            field=models.CharField(max_length=200),
        ),
    ]
