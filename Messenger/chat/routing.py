from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<pk>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
