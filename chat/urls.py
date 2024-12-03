from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat'),
    path('room/<int:room_id>/', views.chat_room, name='chat-room'),
]
