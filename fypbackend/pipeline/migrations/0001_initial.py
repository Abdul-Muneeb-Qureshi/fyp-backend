# Generated by Django 5.1.3 on 2024-12-02 07:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('url', models.URLField()),
                ('file_name', models.CharField(max_length=255)),
                ('published_date', models.DateTimeField()),
                ('duration', models.CharField(max_length=50)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='pipeline.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('entity', models.CharField(max_length=255)),
                ('chunk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='pipeline.chunk')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='pipeline.video')),
            ],
        ),
        migrations.AddField(
            model_name='chunk',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chunks', to='pipeline.video'),
        ),
    ]
