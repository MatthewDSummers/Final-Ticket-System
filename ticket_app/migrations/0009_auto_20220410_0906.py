# Generated by Django 2.2 on 2022-04-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_app', '0008_priority_toggle_auto_priorities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(default='Low', max_length=12),
        ),
    ]
