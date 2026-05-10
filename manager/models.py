from django.conf import settings
from django.db import models

ROLE_CHOICES = [
    ('Batsman', 'Batsman'),
    ('Bowler', 'Bowler'),
    ('Allrounder', 'Allrounder'),
    ('Wicketkeeper', 'Wicketkeeper'),
]

BOWLING_TYPE_CHOICES = [
    ('Fast', 'Fast'),
    ('Spin', 'Spin'),
    ('Medium', 'Medium'),
    ('None', 'None'),
]

PERSONNEL_ROLE_CHOICES = [
    ('Coach', 'Coach'),
    ('Scout', 'Scout'),
    ('Medical', 'Medical'),
    ('Marketing', 'Marketing'),
]

CURRENCY_CHOICES = [
    ('$', '$'),
    ('£', '£'),
    ('€', '€'),
    ('¥', '¥'),
    ('₹', '₹'),
]

MATCH_STATUS_CHOICES = [
    ('Scheduled', 'Scheduled'),
    ('Live', 'Live'),
    ('Completed', 'Completed'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    avatar = models.URLField(blank=True)
    manager_level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class StadiumConfig(models.Model):
    ticket_price = models.PositiveIntegerField(default=50)
    pitch_type = models.CharField(max_length=50, default='Flat')
    soil_type = models.CharField(max_length=10, choices=[('Red', 'Red'), ('Black', 'Black')], default='Red')
    merchandise_revenue = models.PositiveIntegerField(default=1000)
    capacity = models.PositiveIntegerField(default=8000)
    seats_level = models.PositiveIntegerField(default=1)
    food_level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Stadium ({self.pitch_type} / {self.soil_type})"

class Personnel(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=PERSONNEL_ROLE_CHOICES)
    level = models.PositiveIntegerField(default=1)
    cost = models.PositiveIntegerField(default=10000)
    bonus = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Team(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=10)
    logo_url = models.URLField(blank=True)
    jersey_color = models.CharField(max_length=20, blank=True)
    currency_unit = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='$')
    fame = models.IntegerField(default=0)
    currency = models.IntegerField(default=100000)
    training_camp_level = models.PositiveIntegerField(default=1)
    stadium = models.OneToOneField(StadiumConfig, on_delete=models.CASCADE, null=True, blank=True)
    coach = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='coach_teams')
    scout = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='scout_teams')
    medical = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='medical_teams')

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=120)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    age = models.PositiveIntegerField(default=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bowling_type = models.CharField(max_length=10, choices=BOWLING_TYPE_CHOICES, default='None')
    batting = models.PositiveIntegerField(default=50)
    bowling = models.PositiveIntegerField(default=50)
    stamina = models.PositiveIntegerField(default=50)
    fielding = models.PositiveIntegerField(default=50)
    value = models.PositiveIntegerField(default=10000)
    is_for_auction = models.BooleanField(default=False)
    contract_expiry = models.PositiveIntegerField(default=30)
    career_stats = models.JSONField(default=dict)

    def __str__(self):
        return self.name

class Auction(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='auctions')
    current_bid = models.PositiveIntegerField(default=0)
    high_bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    end_time = models.DateTimeField()
    starting_bid = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Auction for {self.player.name}"

class Match(models.Model):
    league_id = models.CharField(max_length=100, blank=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES, default='Scheduled')
    score = models.JSONField(default=dict)
    pitch_type = models.CharField(max_length=50, default='Flat')
    soil_type = models.CharField(max_length=10, choices=[('Red', 'Red'), ('Black', 'Black')], default='Red')
    scheduled_time = models.DateTimeField()
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
