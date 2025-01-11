# Generated by Django 5.1.2 on 2025-01-11 00:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_core', '0004_completiontracking_delete_contentcompletion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coursemember',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='ContentCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_completions', to='lms_core.coursecontent')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completed_contents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Content Completion',
                'verbose_name_plural': 'Content Completions',
                'unique_together': {('student', 'content')},
            },
        ),
        migrations.DeleteModel(
            name='CompletionTracking',
        ),
    ]
