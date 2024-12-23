from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Update WebSocket URL pattern to include user_id
    re_path(r'ws/notifications/(?P<user_id>\d+)/$', consumers.NotificationConsumer.as_asgi()),
]