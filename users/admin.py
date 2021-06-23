from django.contrib import admin
from users.models import Profile, FavoriteGames


class FavoriteGamesInline(admin.TabularInline):
    model = FavoriteGames


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        FavoriteGamesInline,
    ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(FavoriteGames)
