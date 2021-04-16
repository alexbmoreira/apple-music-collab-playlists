# Generated by Django 3.1.5 on 2021-04-14 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_matchlistdislike_watchlistmovie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendslist',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='friendslist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='matchlist',
            name='friend',
        ),
        migrations.RemoveField(
            model_name='matchlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='MovieLike',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='FriendsList',
        ),
        migrations.DeleteModel(
            name='Matchlist',
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]