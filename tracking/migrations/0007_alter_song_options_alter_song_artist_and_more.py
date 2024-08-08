# Generated by Django 5.0.7 on 2024-08-06 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0006_song_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='song',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='file',
            field=models.FileField(upload_to='songs/'),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]