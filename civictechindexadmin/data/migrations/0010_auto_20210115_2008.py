# Generated by Django 3.0.7 on 2021-01-15 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20210115_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='http_status_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
