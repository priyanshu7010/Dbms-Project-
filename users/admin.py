from django.contrib import admin
from users.models import User, Game

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'country', 'u_age', 'pincode', 'city', 'passwords')
    search_fields = ('user_name', 'country', 'city')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'user_id', 'game_name', 'game_type', 'age_rest', 'rate')
