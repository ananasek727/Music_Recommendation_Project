# Generated by Django 4.2.7 on 2023-12-03 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('title', models.CharField(max_length=150)),
                ('artist_str', models.CharField(max_length=150)),
                ('duration', models.IntegerField()),
                ('image_url', models.CharField(max_length=150)),
                ('id', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('uri', models.CharField(max_length=150)),
            ],
        ),
    ]
