from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Team, UserProfile, Activity, Leaderboard, Workout
from .serializers import (
    TeamSerializer,
    UserProfileSerializer,
    ActivitySerializer,
    LeaderboardSerializer,
    WorkoutSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['get'])
    def by_email(self, request):
        """Get user profile by email."""
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email parameter is required'}, status=400)
        
        try:
            profile = UserProfile.objects.get(email=email)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get all user profiles for a team."""
        team_name = request.query_params.get('team_name')
        if not team_name:
            return Response({'error': 'Team name parameter is required'}, status=400)
        
        profiles = UserProfile.objects.filter(team_name=team_name)
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing activities.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get all activities for a user by email."""
        user_email = request.query_params.get('user_email')
        if not user_email:
            return Response({'error': 'User email parameter is required'}, status=400)
        
        activities = Activity.objects.filter(user_email=user_email)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get all activities for a team."""
        team_name = request.query_params.get('team_name')
        if not team_name:
            return Response({'error': 'Team name parameter is required'}, status=400)
        
        team_members = UserProfile.objects.filter(team_name=team_name)
        member_emails = team_members.values_list('email', flat=True)
        activities = Activity.objects.filter(user_email__in=member_emails)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """Get activities within a date range."""
        from datetime import datetime
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response({'error': 'Both start_date and end_date parameters are required'}, status=400)
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            activities = Activity.objects.filter(date__gte=start, date__lte=end)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing leaderboards.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard for a specific team."""
        team_name = request.query_params.get('team_name')
        if not team_name:
            return Response({'error': 'Team name parameter is required'}, status=400)
        
        try:
            leaderboard = Leaderboard.objects.get(team_name=team_name)
            serializer = self.get_serializer(leaderboard)
            return Response(serializer.data)
        except Leaderboard.DoesNotExist:
            return Response({'error': 'Leaderboard not found'}, status=404)

    @action(detail=False, methods=['get'])
    def rankings(self, request):
        """Get all team rankings sorted by activity minutes."""
        leaderboards = Leaderboard.objects.all().order_by('-total_activity_minutes')
        serializer = self.get_serializer(leaderboards, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workout suggestions.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty level."""
        difficulty = request.query_params.get('difficulty')
        if not difficulty:
            return Response({'error': 'Difficulty parameter is required'}, status=400)
        
        workouts = Workout.objects.filter(difficulty=difficulty)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_duration(self, request):
        """Get workouts by maximum duration."""
        max_duration = request.query_params.get('max_duration')
        if not max_duration:
            return Response({'error': 'max_duration parameter is required'}, status=400)
        
        try:
            max_duration = int(max_duration)
            workouts = Workout.objects.filter(duration_minutes__lte=max_duration)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'max_duration must be a number'}, status=400)
