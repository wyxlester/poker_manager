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

    duration_hours = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calculate duration before saving
        time_difference = self.end_time - self.start_time
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # Save the duration
        self.duration_hours = hours
        self.duration_minutes = minutes

        super().save(*args, **kwargs)

    def get_player_session_count(self):
        return self.playersession_set.count()


class RebuyEvent(models.Model):
    player_session = models.ForeignKey(
        'PlayerSession',
        on_delete=models.CASCADE,
        related_name='rebuy_events',
    )
    rebuy_amount = models.IntegerField(validators=[MinValueValidator(1)])
    timestamp = models.DateTimeField(auto_now_add=True)


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
    cash_out = models.IntegerField(null=True, blank=True)

    def total_buy_in(self):
        if self.rebuy_events.exists():
            return self.buy_in + sum(rebuy.rebuy_amount for rebuy in self.rebuy_events.all())
        return self.buy_in

    def calculate_pnl(self):
        if self.cash_out is not None:
            return self.cash_out - self.total_buy_in()
        return "Cash Out Not Recorded"

    class Meta:
        # Added the unique_together option to enforce uniqueness of player_id and session_id pairs
        unique_together = ('player_id', 'session_id')
