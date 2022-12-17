from django.urls import path
from rest_framework import routers

from chat.api.views import MessageViewSet, RoomViewSet
from . import views

chat_router = routers.DefaultRouter()
chat_router.register(r'chat-room', RoomViewSet, basename='chat-room')
chat_router.register(r'chat-message', MessageViewSet, basename='chat-message')
urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('<int:id>/', views.room_view, name='chat-room'),
]
