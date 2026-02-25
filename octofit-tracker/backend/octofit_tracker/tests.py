from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Team, UserProfile, Activity, Leaderboard, Workout
from django.contrib.auth.models import User

class OctoFitTrackerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Test Team', description='A test team')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.profile = UserProfile.objects.create(user=self.user, email='test@example.com', team_name=self.team.name, hero_name='Test Hero', bio='Test bio')
        self.activity = Activity.objects.create(user_email=self.profile.email, activity_type='running', duration_minutes=30, distance_km=5.0, calories_burned=300, intensity='medium', notes='Test run', date='2026-01-01')
        self.leaderboard = Leaderboard.objects.create(team_name=self.team.name, total_activity_minutes=30, total_calories_burned=300, member_count=1)
        self.workout = Workout.objects.create(name='Test Workout', description='Test workout desc', difficulty='beginner', duration_minutes=20, exercises=[{"name": "Jumping Jacks", "duration": 5}])

    def test_team_list(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_userprofile_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_activity_list(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_leaderboard_list(self):
        response = self.client.get('/api/leaderboards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_workout_list(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
