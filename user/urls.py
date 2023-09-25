from django.urls import path
from .views import (UserRegistrationView, UserLoginView, UserLogoutView, SuggestedFriendsView)


urlpatterns = [
    path("api/register/", UserRegistrationView.as_view(), name='user_registration'),
    path("api/login/", UserLoginView.as_view(), name='user_login'),
    path("api/logout/", UserLogoutView.as_view(), name='user_logout'),
    path("api/suggested-friends/<int:user_id>/", SuggestedFriendsView.as_view(), name='suggested-friends'),
]
