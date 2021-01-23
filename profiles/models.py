import random

from django.dispatch import Signal
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


friend_request_accepted = Signal()
movie_updated = Signal()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class FriendsList(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='friends_list_user')
    friends = models.ManyToManyField(User, blank=True, related_name='friends_list_friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, new_friend):
        if new_friend not in self.friends.all():
            self.friends.add(new_friend)

    def friend(self, new_friend):
        self.add_friend(new_friend)

        other_list = FriendsList.objects.get(user=new_friend)
        other_list.add_friend(self.user)

    def remove_friend(self, friend):
        if friend in self.friends.all():
            self.friends.remove(friend)

    def unfriend(self, friend):
        self.remove_friend(friend)

        other_list = FriendsList.objects.get(user=friend)
        other_list.remove_friend(self.user)


class FriendRequest(models.Model):

    creator = models.ForeignKey(User, related_name='request_creator', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='request_friend', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def accept(self):
        creator_list = FriendsList.objects.get(user=self.creator)
        creator_list.friend(self.receiver)
        self.active = False
        self.save()
        friend_request_accepted.send(sender=self.__class__, creator=self.creator, receiver=self.receiver)

    def decline(self):
        self.active = False
        self.save()

    def cancel(self):
        self.active = False
        self.save()


class Watchlist(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watch_list_user')
    watchlist = ArrayField(models.IntegerField(), blank=True, default=list)

    def add_movie(self, movie_id):
        if movie_id not in self.watchlist:
            self.watchlist.append(movie_id)
            self.save()
            movie_updated.send(sender=self.__class__, user=self.user)

    def remove_movie(self, movie_id):
        if movie_id in self.watchlist:
            self.watchlist.remove(movie_id)
            self.save()
            movie_updated.send(sender=self.__class__, user=self.user)

    def __str__(self):
        return f"{self.user}'s watchlist"


class JointWatchlist(models.Model):

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joint_watch_list_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joint_watch_list_user2')
    shared_watchlist = ArrayField(models.IntegerField(), blank=True, default=list)
    indiv_watchlist = ArrayField(models.IntegerField(), blank=True, default=list)

    def save(self, *args, **kwargs):
        user1_wlist = Watchlist.objects.get(user=self.user1).watchlist
        user2_wlist = Watchlist.objects.get(user=self.user2).watchlist

        self.shared_watchlist = [movie for movie in user1_wlist if movie in user2_wlist]
        self.indiv_watchlist = [movie for movie in user1_wlist if movie not in user2_wlist] + \
            [movie for movie in user2_wlist if movie not in user1_wlist]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user1}'s and {self.user2}'s watchlist"
