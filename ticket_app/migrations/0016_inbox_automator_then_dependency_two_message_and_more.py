# Generated by Django 4.1.3 on 2022-11-12 14:26

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
        ('ticket_app', '0015_automator_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inbox', to='login_app.user')),
            ],
        ),
        migrations.AddField(
            model_name='automator',
            name='then_dependency_two',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('subject', models.CharField(default='', max_length=255)),
                ('body', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.TextField(default='', max_length='32')),
                ('inbox', models.ManyToManyField(related_name='messages', to='ticket_app.inbox')),
                ('recipients', models.ManyToManyField(related_name='messages', to='login_app.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent', to='login_app.user')),
                ('starred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='starred', to='ticket_app.inbox')),
                ('trashed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trashed', to='ticket_app.inbox')),
                ('viewed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed', to='ticket_app.inbox')),
            ],
        ),
        migrations.CreateModel(
            name='CannedResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('body', ckeditor.fields.RichTextField(blank=True, default='', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='canned_responses', to='login_app.user')),
            ],
        ),
    ]
