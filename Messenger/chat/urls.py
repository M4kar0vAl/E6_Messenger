from django.urls import path
from .views import ChatList, CreateChat, ChatDetail, EditChat, DeleteChat, manage_participants

urlpatterns = [
    path('', ChatList.as_view(), name='chats'),
    path('user_chats', ChatList.as_view(), name='user_chats'),
    path('<int:pk>/', ChatDetail.as_view(), name='chat'),
    path('add/', CreateChat.as_view(), name='add_group_chat'),
    path('add_personal/', CreateChat.as_view(), name='add_personal_chat'),
    path('edit/<int:pk>/', EditChat.as_view(), name='edit_chat'),
    path('delete/<int:pk>/', DeleteChat.as_view(), name='delete_chat'),
    path('manage_participants/', manage_participants, name='manage'),
]
