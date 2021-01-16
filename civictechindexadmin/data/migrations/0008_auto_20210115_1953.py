# Generated by Django 3.0.7 on 2021-01-15 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_faq_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='http_status',
            field=models.CharField(max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='http_status_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='notes',
            field=models.CharField(max_length=4096, null=True),
        ),
    ]
