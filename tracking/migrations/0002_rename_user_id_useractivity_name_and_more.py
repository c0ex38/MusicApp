# Generated by Django 5.0.7 on 2024-08-04 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useractivity',
            old_name='user_id',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='useractivity',
            old_name='action',
            new_name='store_name',
        ),
    ]