# Generated by Django 2.0.2 on 2018-02-26 05:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comander', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
