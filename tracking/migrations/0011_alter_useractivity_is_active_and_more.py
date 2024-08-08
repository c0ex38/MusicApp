# Generated by Django 5.0.7 on 2024-08-07 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0010_alter_useractivity_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Aktif'),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='store_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Mağaza Adı'),
        ),
    ]
