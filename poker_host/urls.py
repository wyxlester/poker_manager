from django.urls import path

from . import views

app_name = "poker_host"

urlpatterns = [
    path("", views.home, name="home"),
    path("players/", views.player_list, name="players"),
    path("sessions/", views.session_list, name="sessions"),
]
