from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
# from . import forms

# Home page
def home(request):
    return render(request, "poker_host/home.html")


def player_list(request):
    players = Player.objects.all()
    return render(request, "poker_host/players.html", {"players": players})


def time_cleaning(time_difference):
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    time_difference_dict = {
        "hours": hours,
        "minutes": minutes
    }
    return time_difference_dict


def session_list(request):
    sessions = Session.objects.all()
    return render(request, "poker_host/sessions.html", {
        "sessions": sessions,
    })
