# Generated by Django 5.1.2 on 2025-01-11 03:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Category Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Category Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Teacher')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nama Course')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('price', models.IntegerField(verbose_name='Harga')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Banner')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('max_students', models.PositiveIntegerField(default=30, verbose_name='Max Students')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms_core.category', verbose_name='Category')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Pengajar')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Daftar Course',
            },
        ),
        migrations.CreateModel(
            name='CourseContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='judul konten')),
                ('description', models.TextField(default='-', verbose_name='deskripsi')),
                ('video_url', models.CharField(blank=True, max_length=200, null=True, verbose_name='URL Video')),
                ('file_attachment', models.FileField(blank=True, null=True, upload_to='', verbose_name='File')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lms_core.course', verbose_name='matkul')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='lms_core.coursecontent', verbose_name='induk')),
            ],
            options={
                'verbose_name': 'Konten Matkul',
                'verbose_name_plural': 'Konten Matkul',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='komentar')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Approved for Display')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='pengguna')),
                ('content_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_core.coursecontent', verbose_name='konten')),
            ],
            options={
                'verbose_name': 'Komentar',
                'verbose_name_plural': 'Komentar',
            },
        ),
        migrations.CreateModel(
            name='CourseMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roles', models.CharField(choices=[('std', 'Siswa'), ('ast', 'Asisten')], default='std', max_length=3, verbose_name='peran')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lms_core.course', verbose_name='matkul')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='siswa')),
            ],
            options={
                'verbose_name': 'Subscriber Matkul',
                'verbose_name_plural': 'Subscriber Matkul',
            },
        ),
        migrations.CreateModel(
            name='CompletionTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Penyelesaian')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Siswa')),
                ('course_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_core.coursecontent', verbose_name='Konten Matkul')),
            ],
            options={
                'verbose_name': 'Completion Tracking',
                'verbose_name_plural': 'Completion Trackings',
                'unique_together': {('student', 'course_content')},
            },
        ),
    ]
