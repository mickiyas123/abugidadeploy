from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name="home"),
    # path('about', views.about, name="about"),
    # path('course', views.course, name="course"),
    path('', views.discussions, name="discussions"),
    # path('topic/', views.topic, name="topic"),
    # path('profile/<str:pk>', views.profile, name="profile"),
    path('rooms/', views.rooms, name="rooms"),
    path('room/<str:pk>', views.room, name="room"),
    path('create-room', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('create-question/', views.createQuestion, name="create-question"),
    path('create-question/<str:pk>', views.createroomQuestion, name="create-room-question"),
    path('update-question/<str:pk>', views.updateQuestion, name="update-question"),
    path('delete-question/<str:pk>', views.deleteQuestion, name="delete-question"),
    path('create-answer/<str:pk>', views.createAnswer, name="create-answer"),
    path('update-answer/<str:pk>', views.updateAnswer, name="update-answer"),
    path('delete-answer/<str:pk>', views.deleteAnswer, name="delete-answer")
]