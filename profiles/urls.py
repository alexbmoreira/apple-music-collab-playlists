from django.urls import path

from .views import (FriendActionAPIView, FriendRequestsAPIView,
                    JointWatchlistAPIView, MatchlistActionAPIView,
                    MatchlistAPIView, ProfileAPIView, ProfileDetailAPIView,
                    ProfileFriendsAPIView, ProfileWatchlistAPIView,
                    RequestActionAPIView, WatchlistActionAPIView)

profile_api = ProfileAPIView.as_view()
profile_detail_api = ProfileDetailAPIView.as_view()
profile_friends_api = ProfileFriendsAPIView.as_view()
profile_watchlist_api = ProfileWatchlistAPIView.as_view()
watchlist_action_api = WatchlistActionAPIView.as_view()
joint_watchlist_api = JointWatchlistAPIView.as_view()
friend_action_api = FriendActionAPIView.as_view()
user_requests_api = FriendRequestsAPIView.as_view()
request_action_api = RequestActionAPIView.as_view()
matchlist_api = MatchlistAPIView.as_view()
matchlist_action_api = MatchlistActionAPIView.as_view()

urlpatterns = [
    path("profiles/search/", profile_api, name="profiles"),
    path("profiles/search/<str:search>", profile_api, name="profiles_search"),
    path("profiles/<int:user_id>/", profile_detail_api, name="profile_detail_api"),
    path("profiles/<int:user_id>/friends/", profile_friends_api, name="profile_friends_list"),
    path("profiles/<int:user_id>/watchlist/", profile_watchlist_api, name="profile_watchlist_list"),
    path("user/friends/<str:operation>/<int:user_id>/", friend_action_api, name="update_friends"),
    path("user/requests/", user_requests_api, name="update_requests"),
    path("user/requests/<str:operation>/<int:request_id>/", request_action_api, name="update_requests"),
    path("user/watchlist/<str:operation>/", watchlist_action_api, name="update_watchlist"),
    path("user/joint-watchlist/<int:user_id>/", joint_watchlist_api, name="joint_watchlist"),
    path("user/matchlist/<int:user_id>/", matchlist_api, name="matchlist"),
    path("user/matchlist/<str:operation>/<int:user_id>/", matchlist_action_api, name="update_matchlist"),
]
