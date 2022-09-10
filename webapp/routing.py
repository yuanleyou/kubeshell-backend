from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import re_path
from medivh.consumers import SSHConsumer, LogConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^api/v1/webshell/', SSHConsumer.as_asgi()),
            re_path(r'^api/v1/logs/', LogConsumer.as_asgi()),
        ])
    ),
})
