# Generated by Django 5.2.2 on 2025-06-13 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_rename_content_message_message_body_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='user_id',
            new_name='id',
        ),
    ]
