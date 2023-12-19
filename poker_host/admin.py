from django.contrib import admin
from .models import Player, Game, Session, RebuyEvent, PlayerSession

# Register your models here.
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "bankroll", "user_id")
    list_editable = ("name", "bankroll", "user_id")

class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "game_type", "small_blind", "big_blind", "user_id")
    list_editable = ("game_type", "small_blind", "big_blind", "user_id")

class SessionAdmin(admin.ModelAdmin):
    list_display = ("id", "game_id", "start_time", "end_time")
    list_editable = ("game_id", "start_time", "end_time")

class RebuyEventAdmin(admin.ModelAdmin):
    list_display = ("id", "player_session", "rebuy_amount", "timestamp")

class PlayerSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "player_id", "session_id", "buy_in", "cash_out")
    list_editable = ("buy_in", "cash_out")

admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(PlayerSession, PlayerSessionAdmin)
admin.site.register(RebuyEvent, RebuyEventAdmin)
