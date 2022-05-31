# Generated by Django 4.0.4 on 2022-05-31 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('media_link', models.CharField(max_length=200)),
                ('time_posted', models.CharField(max_length=100)),
                ('likes', models.IntegerField()),
                ('comments', models.JSONField()),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.person')),
            ],
        ),
    ]