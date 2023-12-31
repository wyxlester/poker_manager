from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError

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
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Calculate duration before saving
        time_difference = self.end_time - self.start_time
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # Save the duration
        self.duration_hours = hours
        self.duration_minutes = minutes

        # Check if any PlayerSession is not completed
        self.completed = self.is_completed()

        # Check if total buy-in equals total cash-out
        total_buy_in = sum(player_session.total_buy_in() for player_session in self.player_sessions.all())
        total_cash_out = sum(player_session.cash_out for player_session in self.player_sessions.all() if player_session.cash_out is not None)

        if total_buy_in != total_cash_out:
            raise ValidationError("Total buy-in does not equal total cash-out.")

        super().save(*args, **kwargs)

    def get_player_session_count(self):
        return self.player_sessions.count()

    def is_completed(self):
        # Check if any PlayerSession is not completed
        if self.player_sessions.filter(cash_out__isnull=True, pnl__isnull=True).exists():
            return False

        # Check if total buy-in equals total cash-out
        total_buy_in = sum(player_session.total_buy_in() for player_session in self.player_sessions.all())
        total_cash_out = sum(player_session.cash_out for player_session in self.player_sessions.all() if player_session.cash_out is not None)

        return total_buy_in == total_cash_out


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
        related_name='player_sessions',  # Use a proper related_name
    )
    buy_in = models.IntegerField(validators=[MinValueValidator(1)])
    cash_out = models.IntegerField(null=True, blank=True)
    pnl = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate PNL before saving if cash_out is provided
        if self.cash_out is not None:
            self.pnl = self.calculate_pnl()

        super().save(*args, **kwargs)

    def total_buy_in(self):
        if self.rebuy_events.exists():
            return self.buy_in + sum(rebuy.rebuy_amount for rebuy in self.rebuy_events.all())
        return self.buy_in

    def calculate_pnl(self):
        # Calculate PNL based on cash_out and total_buy_in
        return self.cash_out - self.total_buy_in() if self.cash_out is not None else None
    class Meta:
        unique_together = ('player_id', 'session_id')
