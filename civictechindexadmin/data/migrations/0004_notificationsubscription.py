# Generated by Django 3.0.7 on 2020-09-20 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_add_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(max_length=256)),
                ('email_address', models.EmailField(max_length=256)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('notification_type', 'email_address')},
            },
        ),
    ]