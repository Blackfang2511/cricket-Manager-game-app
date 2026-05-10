from django.contrib import admin
from .models import Auction, Match, Personnel, Player, Team, UserProfile, StadiumConfig

admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Auction)
admin.site.register(Match)
admin.site.register(Personnel)
admin.site.register(StadiumConfig)
