# Generated by Django 4.2 on 2023-05-16 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='sender',
            field=models.CharField(max_length=100),
        ),
    ]
