# Generated by Django 5.1 on 2024-11-15 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0002_profile_delete_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='foto_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default.jpg', upload_to='profile_images/'),
        ),
    ]
