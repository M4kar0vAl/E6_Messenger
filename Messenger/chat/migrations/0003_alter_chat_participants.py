# Generated by Django 5.0.4 on 2024-04-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='participants',
            field=models.JSONField(default=dict),
        ),
    ]
