# Generated by Django 2.2 on 2022-04-10 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_app', '0007_auto_20220406_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='priority',
            name='toggle_auto_priorities',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
