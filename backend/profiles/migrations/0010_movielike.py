# Generated by Django 3.1.5 on 2021-01-23 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_matchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.IntegerField()),
                ('datetime_added', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
