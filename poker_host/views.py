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
    return render(request, "poker_host/player_list.html", {"players": players})
