# Generated by Django 3.2.4 on 2021-07-02 17:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h1', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('url', models.SlugField()),
                ('text', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 7, 2, 17, 23, 56, 496674, tzinfo=utc))),
            ],
        ),
    ]
