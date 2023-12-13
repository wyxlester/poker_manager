from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)
    bankroll = models.IntegerField(default=0)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return f"Name: {self.name}, Bankroll: {self.bankroll}, Belongs to: {self.user_id}"

class Game(models.Model):
    GAME_FORMATS = [
        ("NLHE", "No-Limit Hold'em"),
        ("LHE", "Limit Hold'em"),
        ("PLO-4", "Pot-Limit Omaha (4 cards)"),
        ("PLO-5", "Pot-Limit Omaha (5 cards)"),
        ("PLO-6", "Pot-Limit Omaha (6 cards)"),
        ("PLO hi/lo-4", "Pot-Limit Omaha Hi/Lo (4 cards)"),
        ("PLO hi/lo-5", "Pot-Limit Omaha Hi/Lo (5 cards)"),
        ("Dealer's Choice", "Dealer's Choice"),
    ]
    game_type = models.CharField(max_length=100, choices=GAME_FORMATS)
    small_blind = models.IntegerField(validators=[MinValueValidator(1)])
    big_blind = models.IntegerField(validators=[MinValueValidator(1)])
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Session(models.Model):
    game_id = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class PlayerSession(models.Model):
    player_id = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
    )
    session_id = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
    )
    buy_in = models.IntegerField(validators=[MinValueValidator(1)])
    cash_out = models.IntegerField(default=0)
    rebuy = models.IntegerField(default=0)
    notes = models.TextField(max_length=1000, blank=True, null=True)
