# Generated by Django 5.0.7 on 2024-08-07 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0009_alter_useractivity_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Aktif'),
        ),
    ]
