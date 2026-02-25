from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """Team model for superhero team groups."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'octofit_tracker'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile for fitness tracking."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    team_name = models.CharField(max_length=100, blank=True, default='')  # Store team name instead of FK
    hero_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'octofit_tracker'

    def __str__(self):
        return f"{self.user.username} - {self.hero_name}"


class Activity(models.Model):
    """Activity model for logging fitness activities."""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('strength', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('crossfit', 'CrossFit'),
        ('other', 'Other'),
    ]

    user_email = models.EmailField()  # Store user email instead of FK
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    duration_minutes = models.IntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    calories_burned = models.IntegerField(null=True, blank=True)
    intensity = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    notes = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'octofit_tracker'

    def __str__(self):
        return f"{self.user_email} - {self.activity_type} on {self.date}"


class Leaderboard(models.Model):
    """Leaderboard model for competitive rankings."""
    team_name = models.CharField(max_length=100, unique=True)
    total_activity_minutes = models.IntegerField(default=0)
    total_calories_burned = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'octofit_tracker'

    def __str__(self):
        return f"{self.team_name} - Leaderboard"


class Workout(models.Model):
    """Personalized workout suggestions."""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration_minutes = models.IntegerField()
    exercises = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'octofit_tracker'

    def __str__(self):
        return self.name
