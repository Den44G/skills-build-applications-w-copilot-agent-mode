from django.contrib import admin
from .models import Team, UserProfile, Activity, Leaderboard, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('hero_name', 'user', 'email', 'team_name', 'created_at')
    list_filter = ('team_name', 'created_at')
    search_fields = ('hero_name', 'email')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'activity_type', 'date', 'duration_minutes', 'intensity')
    list_filter = ('activity_type', 'intensity', 'date')
    search_fields = ('user_email', 'activity_type')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'total_activity_minutes', 'total_calories_burned', 'member_count', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('team_name',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'duration_minutes', 'created_at')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('name', 'description')
