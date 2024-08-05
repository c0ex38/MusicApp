# Generated by Django 5.0.7 on 2024-08-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_useractivity_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='announcements/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]