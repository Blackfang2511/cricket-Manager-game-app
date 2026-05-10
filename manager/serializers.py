from rest_framework import serializers
from .models import Auction, Match, Personnel, Player, Team, UserProfile, StadiumConfig

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class StadiumConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumConfig
        fields = '__all__'

class PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
