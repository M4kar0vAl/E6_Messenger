from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Chat, Message


class ChatSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    participants = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    type = serializers.ChoiceField(choices=Chat.TYPE_CHOICES, read_only=True, default=Chat.GROUP)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'participants', 'creator', 'type']


class UserSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField(allow_empty_file=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar']


class MessageSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    chat = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'text', 'user', 'chat', 'created']
