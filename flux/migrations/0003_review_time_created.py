# Generated by Django 4.2.1 on 2023-05-30 09:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flux', '0002_ticket_time_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]