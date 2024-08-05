# Generated by Django 5.0.7 on 2024-08-04 12:50

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0008_alter_announcement_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='current_time',
            field=models.CharField(default='00:00', max_length=10),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='last_active',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='song',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tracking.song'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='store_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]