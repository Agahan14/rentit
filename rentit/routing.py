from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    'websocket':
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ,
})
# from channels.routing import ProtocolTypeRouter, URLRouter
# # import app.routing
# from django.urls import re_path
# from chat.consumers import ChatConsumer
# websocket_urlpatterns = [
#     re_path(r'^ws/(?P<room_name>[^/]+)/$', ChatConsumer.as_asgi()),
# ]
# # the websocket will open at 127.0.0.1:8000/ws/<room_name>
# application = ProtocolTypeRouter({
#     'websocket':
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ,
# })