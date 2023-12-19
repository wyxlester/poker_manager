from django.urls import path

from . import views

app_name = "poker_host"

urlpatterns = [
    path("", views.home, name="home"),
    path("player_list/", views.player_list, name="player_list"),
]
