# Generated by Django 4.1.3 on 2022-12-07 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_app', '0019_inbox_messages_inbox_starred_inbox_trashed_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-status', 'priority', '-created_at']},
        ),
    ]
