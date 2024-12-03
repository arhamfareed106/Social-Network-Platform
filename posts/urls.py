from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.create_post, name='post-create'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/like/', views.like_post, name='post-like'),
]
