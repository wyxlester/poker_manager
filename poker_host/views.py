from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import UpdateCashOutForm

# Home page
def home(request):
    return render(request, "poker_host/home.html")


def player_list(request):
    players = Player.objects.all()
    return render(request, "poker_host/players.html", {"players": players})


def session_list(request):
    sessions = Session.objects.all()
    return render(request, "poker_host/sessions.html", {"sessions": sessions})


def session(request, player_session_id):
    session = Session.objects.get(pk=player_session_id)
    return render(request, "poker_host/session.html", {"session": session})


def update_cash_out(request, player_session_id):
    # player_session = get_object_or_404(PlayerSession, pk=player_session_id)
    player_session = PlayerSession.objects.get(pk=29)
    form = UpdateCashOutForm()

    if request.method == 'POST':
        form = UpdateCashOutForm(request.POST)

        if form.is_valid():
            # Update cash_out and save the PlayerSession instance
            player_session.cash_out = form.cleaned_data['cash_out']
            player_session.save()

            # Optionally, you can add a success message
            messages.success(request, 'Cash-out value updated successfully.')

            # Redirect to a relevant page
            return HttpResponseRedirect(reverse('poker_host:sessions'))

    # Render the form or relevant template
    return render(request, 'update_session.html', {'player_session': player_session})
