from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginUser, RegisterUser, UserProfile, UserList

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='registration'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('users/', UserList.as_view(), name='users'),
    path('users_to_add/', UserList.as_view(), name='add_users'),
]