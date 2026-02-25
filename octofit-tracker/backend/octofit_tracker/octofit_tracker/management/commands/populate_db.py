from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from octofit_tracker.models import UserProfile, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        self.stdout.write(self.style.WARNING('Deleting existing data...'))
        try:
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            UserProfile.objects.all().delete()
            Workout.objects.all().delete()
            Team.objects.all().delete()
            User.objects.exclude(username='admin').delete()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Deletion warning: {e}'))

        # Create Teams
        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='The mighty superhero team from Marvel Universe'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='The legendary superhero team from DC Universe'
        )

        # Marvel Heroes
        marvel_heroes = [
            {'username': 'spiderman', 'email': 'peter@marvel.com', 'hero_name': 'Spider-Man', 'bio': 'Friendly neighborhood Spider-Man'},
            {'username': 'ironman', 'email': 'tony@marvel.com', 'hero_name': 'Iron Man', 'bio': 'Genius, billionaire, playboy, philanthropist'},
            {'username': 'captainamerica', 'email': 'steve@marvel.com', 'hero_name': 'Captain America', 'bio': 'First Avenger'},
            {'username': 'blackwidow', 'email': 'natasha@marvel.com', 'hero_name': 'Black Widow', 'bio': 'Highly skilled spy and assassin'},
            {'username': 'hulk', 'email': 'bruce@marvel.com', 'hero_name': 'Hulk', 'bio': 'Green giant with incredible strength'},
        ]

        # DC Heroes
        dc_heroes = [
            {'username': 'batman', 'email': 'bruce@dc.com', 'hero_name': 'Batman', 'bio': 'The Dark Knight of Gotham'},
            {'username': 'superman', 'email': 'clark@dc.com', 'hero_name': 'Superman', 'bio': 'Man of Steel'},
            {'username': 'wonderwoman', 'email': 'diana@dc.com', 'hero_name': 'Wonder Woman', 'bio': 'Princess of the Amazons'},
            {'username': 'flash', 'email': 'barry@dc.com', 'hero_name': 'Flash', 'bio': 'The Fastest Man Alive'},
            {'username': 'aquaman', 'email': 'arthur@dc.com', 'hero_name': 'Aquaman', 'bio': 'King of the Seas'},
        ]

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users_marvel = self._create_users(marvel_heroes, team_marvel.name)
        users_dc = self._create_users(dc_heroes, team_dc.name)

        # Create Activities
        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        self._create_activities(users_marvel + users_dc)

        # Create Leaderboards
        self.stdout.write(self.style.SUCCESS('Creating leaderboards...'))
        self._create_leaderboards(team_marvel, team_dc)

        # Create Workouts
        self.stdout.write(self.style.SUCCESS('Creating workout suggestions...'))
        self._create_workouts()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database!'))

    def _create_users(self, heroes, team_name):
        """Create users and user profiles."""
        users = []
        for hero in heroes:
            # Create user
            user, created = User.objects.get_or_create(
                username=hero['username'],
                defaults={
                    'email': hero['email'],
                    'first_name': hero['hero_name'].split()[0] if hero['hero_name'] else '',
                    'last_name': hero['hero_name'].split()[-1] if len(hero['hero_name'].split()) > 1 else ''
                }
            )
            user.set_password('password123')
            user.save()

            # Create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'email': hero['email'],
                    'team_name': team_name,
                    'hero_name': hero['hero_name'],
                    'bio': hero['bio']
                }
            )
            users.append(profile)
        return users

    def _create_activities(self, users):
        """Create activities for users."""
        activity_types = ['running', 'cycling', 'swimming', 'strength', 'yoga', 'crossfit']
        intensities = ['low', 'medium', 'high']
        base_date = datetime.now().date() - timedelta(days=30)

        for user in users:
            for i in range(15):  # 15 activities per user
                date = base_date + timedelta(days=i*2)
                activity_type = activity_types[i % len(activity_types)]
                intensity = intensities[i % len(intensities)]

                Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration_minutes=30 + (i * 5),
                    distance_km=5.0 + (i * 0.5),
                    calories_burned=200 + (i * 20),
                    intensity=intensity,
                    notes=f"Great {activity_type} session!",
                    date=date
                )

    def _create_leaderboards(self, team_marvel, team_dc):
        """Create leaderboards for teams."""
        # Calculate Marvel team stats
        marvel_members = UserProfile.objects.filter(team_name='Team Marvel')
        marvel_total_minutes = sum(
            activity.duration_minutes for member in marvel_members
            for activity in Activity.objects.filter(user_email=member.email)
        )
        marvel_total_calories = sum(
            activity.calories_burned or 0 for member in marvel_members
            for activity in Activity.objects.filter(user_email=member.email)
        )

        # Calculate DC team stats
        dc_members = UserProfile.objects.filter(team_name='Team DC')
        dc_total_minutes = sum(
            activity.duration_minutes for member in dc_members
            for activity in Activity.objects.filter(user_email=member.email)
        )
        dc_total_calories = sum(
            activity.calories_burned or 0 for member in dc_members
            for activity in Activity.objects.filter(user_email=member.email)
        )

        Leaderboard.objects.get_or_create(
            team_name='Team Marvel',
            defaults={
                'total_activity_minutes': marvel_total_minutes,
                'total_calories_burned': marvel_total_calories,
                'member_count': marvel_members.count()
            }
        )

        Leaderboard.objects.get_or_create(
            team_name='Team DC',
            defaults={
                'total_activity_minutes': dc_total_minutes,
                'total_calories_burned': dc_total_calories,
                'member_count': dc_members.count()
            }
        )

    def _create_workouts(self):
        """Create personalized workout suggestions."""
        workouts = [
            {
                'name': 'Beginner Running Program',
                'description': 'A perfect starting point for running enthusiasts',
                'difficulty': 'beginner',
                'duration_minutes': 30,
                'exercises': [
                    {'name': 'Light Warm-up', 'duration': 5},
                    {'name': 'Running', 'duration': 20},
                    {'name': 'Cool-down Stretching', 'duration': 5}
                ]
            },
            {
                'name': 'Intermediate Strength Training',
                'description': 'Build muscle and strength with this program',
                'difficulty': 'intermediate',
                'duration_minutes': 45,
                'exercises': [
                    {'name': 'Warm-up Cardio', 'duration': 5},
                    {'name': 'Bench Press', 'sets': 4, 'reps': 8},
                    {'name': 'Squats', 'sets': 4, 'reps': 8},
                    {'name': 'Deadlifts', 'sets': 3, 'reps': 5},
                    {'name': 'Cool-down', 'duration': 5}
                ]
            },
            {
                'name': 'Advanced CrossFit WOD',
                'description': 'Challenge yourself with this high-intensity workout',
                'difficulty': 'advanced',
                'duration_minutes': 60,
                'exercises': [
                    {'name': 'Warm-up', 'duration': 10},
                    {'name': 'Power Cleans', 'reps': 10},
                    {'name': 'Burpees', 'reps': 20},
                    {'name': 'Pull-ups', 'reps': 15},
                    {'name': 'Row 500m', 'reps': 3}
                ]
            },
            {
                'name': 'Yoga for Flexibility',
                'description': 'Improve flexibility and reduce stress',
                'difficulty': 'beginner',
                'duration_minutes': 40,
                'exercises': [
                    {'name': 'Breathing Exercises', 'duration': 5},
                    {'name': 'Stretching', 'duration': 15},
                    {'name': 'Yoga Poses', 'duration': 15},
                    {'name': 'Meditation', 'duration': 5}
                ]
            },
            {
                'name': 'Swimming Endurance',
                'description': 'Build swimming endurance and technique',
                'difficulty': 'intermediate',
                'duration_minutes': 50,
                'exercises': [
                    {'name': 'Warm-up Swim', 'distance': '200m'},
                    {'name': 'Freestyle Laps', 'distance': '1000m'},
                    {'name': 'Breaststroke', 'distance': '500m'},
                    {'name': 'Cool-down', 'distance': '200m'}
                ]
            }
        ]

        for workout_data in workouts:
            Workout.objects.get_or_create(
                name=workout_data['name'],
                defaults={
                    'description': workout_data['description'],
                    'difficulty': workout_data['difficulty'],
                    'duration_minutes': workout_data['duration_minutes'],
                    'exercises': workout_data['exercises']
                }
            )
