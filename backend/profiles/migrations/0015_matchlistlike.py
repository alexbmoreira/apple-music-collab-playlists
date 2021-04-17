# Generated by Django 3.1.5 on 2021-04-14 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0014_friendship'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchlistLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.IntegerField(blank=True, default=list)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_list_like_friend', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_list_like_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
