# Generated by Django 4.0.4 on 2022-05-31 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='pic',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
