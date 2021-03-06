from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (FriendRequest, Friendship, MatchlistDislike,
                     MatchlistLike, Profile, WatchlistMovie)
from .serializers import (FriendRequestSerializer, FriendshipSerializer,
                          MatchlistDislikeSerializer, MatchlistLikeSerializer,
                          ProfileSerializer, UserSerializer,
                          WatchlistMovieSerializer)


class UserAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data)


class ProfileAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profiles = Profile.objects.all()

        search = request.GET.get('search', '')

        if search != "":
            profiles = profiles.filter(user__username__icontains=search)

        serializer = ProfileSerializer(profiles, many=True)

        return Response(serializer.data)


class ProfileDetailAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user__id=user_id)
        serializer = ProfileSerializer(profile)

        return Response(data=serializer.data)


class FriendRequestAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        kind = request.GET.get('kind', '')

        if kind == 'sent':
            friend_requests = FriendRequest.objects.filter(creator=request.user)
            serializer = FriendRequestSerializer(friend_requests, many=True)
            return Response(data=serializer.data)
        elif kind == 'received':
            friend_requests = FriendRequest.objects.filter(receiver=request.user)
            serializer = FriendRequestSerializer(friend_requests, many=True)
            return Response(data=serializer.data)

        return Response(data={'error': 'invalid friend request kind'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        request.data['creator'] = request.user.id
        request.data['active'] = True
        serializer = FriendRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        friend_request = FriendRequest.objects.get(id=request.data['id'])
        if request.data['action'] == 'accept' and request.user == friend_request.receiver:
            friend_request.accept()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.data['action'] == 'cancel' and request.user == friend_request.creator:
            friend_request.cancel()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.data['action'] == 'decline' and request.user == friend_request.receiver:
            friend_request.decline()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class FriendshipAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id=-1):
        user = request.user if user_id < 0 else get_object_or_404(User, id=user_id)
        friends = Friendship.objects.filter(Q(user=user) | Q(friend=user))
        serializer = FriendshipSerializer(friends, many=True, context={'user_id': user.id})
        return Response(data=serializer.data)

    def delete(self, request):
        friendship = get_object_or_404(Friendship, id=request.data['id'])
        if friendship.user != request.user and friendship.friend != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchlistAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        watchlist = request.user.watchlistmovie_set.all()
        serializer = WatchlistMovieSerializer(watchlist, many=True)
        data = {}
        data['user'] = ProfileSerializer(request.user.profile).data
        data['watchlist'] = serializer.data
        return Response(data=data)

    def post(self, request):
        serializer = WatchlistMovieSerializer(data=request.data, context={'user_id': request.user.id})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        watchlist_movie = get_object_or_404(WatchlistMovie, id=request.data['id'])
        watchlist_movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MatchlistLikeAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        likes = request.user.matchlist_likes.all()

        friend = request.GET.get('friend', '')

        if friend != "":
            likes = likes.filter(friend__id=friend)

        serializer = MatchlistLikeSerializer(likes, many=True)
        data = {}
        data['user'] = ProfileSerializer(request.user.profile).data
        data['likes'] = serializer.data
        return Response(data=data)

    def post(self, request):
        serializer = MatchlistLikeSerializer(data=request.data, context={'user_id': request.user.id})

        if serializer.is_valid():
            if self.check_conflict(request):
                return Response(status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        matchlist_like = get_object_or_404(MatchlistLike, id=request.data['id'])
        matchlist_like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def check_conflict(self, request):
        friend = User.objects.get(id=request.data['friend'])
        try:
            return MatchlistDislike.objects.get(user=request.user, friend=friend, movie=request.data['movie'])
        except Exception:
            return None


class MatchlistDislikeAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        dislikes = request.user.matchlist_dislikes.all()

        friend = request.GET.get('friend', '')

        if friend != "":
            dislikes = dislikes.filter(friend__id=friend)

        serializer = MatchlistDislikeSerializer(dislikes, many=True)
        data = {}
        data['user'] = ProfileSerializer(request.user.profile).data
        data['dislikes'] = serializer.data
        return Response(data=data)

    def post(self, request):
        serializer = MatchlistDislikeSerializer(data=request.data, context={'user_id': request.user.id})

        if serializer.is_valid():
            if self.check_conflict(request):
                return Response(status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        matchlist_dislike = get_object_or_404(MatchlistDislike, id=request.data['id'])
        matchlist_dislike.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def check_conflict(self, request):
        friend = User.objects.get(id=request.data['friend'])
        try:
            return MatchlistLike.objects.get(user=request.user, friend=friend, movie=request.data['movie'])
        except Exception:
            return None


class MatchlistMatchAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        friend = get_object_or_404(User, id=request.GET.get('friend', ''))
        user_likes = request.user.matchlist_likes.all()
        friend_likes = [ml.movie for ml in friend.matchlist_likes.all()]
        matches = [ml for ml in user_likes if ml.movie in friend_likes]
        serializer = MatchlistLikeSerializer(matches, many=True)
        data = {}
        data['user'] = ProfileSerializer(request.user.profile).data
        data['matches'] = serializer.data
        return Response(data=data)


class JointWatchlistAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        friend = get_object_or_404(User, id=request.GET.get('friend', ''))
        joint_watchlist = Profile.objects.get_joint_watchlist(request.user, friend)
        serializer = WatchlistMovieSerializer(joint_watchlist, many=True)
        data = {}
        data['user'] = ProfileSerializer(request.user.profile).data
        data['joint_watchlist'] = serializer.data
        return Response(data=data)
