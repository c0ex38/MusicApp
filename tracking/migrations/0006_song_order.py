# Generated by Django 5.0.7 on 2024-08-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_useractivity_current_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
