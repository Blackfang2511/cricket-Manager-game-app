from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Auction, Match, Personnel, Player, Team, UserProfile, StadiumConfig
from .serializers import (
    AuctionSerializer, MatchSerializer, PersonnelSerializer,
    PlayerSerializer, TeamSerializer, UserProfileSerializer, StadiumConfigSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def advance_day(self, request, pk=None):
        team = self.get_object()
        if team.owner != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        team.currency += 500
        team.save()
        
        for player in team.players.all():
            if player.contract_expiry > 0:
                player.contract_expiry -= 1
                player.save()
            else:
                player.is_for_auction = True
                player.team = None
                player.save()
        
        return Response({'message': 'Day advanced', 'team': TeamSerializer(team).data})

    @action(detail=True, methods=['post'])
    def hire_personnel(self, request, pk=None):
        team = self.get_object()
        if team.owner != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        personnel_id = request.data.get('personnel_id')
        role = request.data.get('role')  # 'coach', 'scout', 'medical'
        personnel = get_object_or_404(Personnel, id=personnel_id)
        
        if team.currency < personnel.cost:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        
        team.currency -= personnel.cost
        
        if role == 'coach':
            team.coach = personnel
        elif role == 'scout':
            team.scout = personnel
        elif role == 'medical':
            team.medical = personnel
        
        team.save()
        return Response({'message': 'Personnel hired', 'team': TeamSerializer(team).data})


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def train(self, request, pk=None):
        player = self.get_object()
        if player.team is None or player.team.owner != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        team = player.team
        if team.currency < 500:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        
        team.currency -= 500
        team.save()
        
        if player.role == 'Batsman' or player.role == 'Wicketkeeper':
            player.batting = min(99, player.batting + team.training_camp_level)
        elif player.role == 'Bowler':
            player.bowling = min(99, player.bowling + team.training_camp_level)
        else:
            player.batting = min(99, player.batting + team.training_camp_level // 2)
            player.bowling = min(99, player.bowling + team.training_camp_level // 2)
        
        player.save()
        return Response({'message': 'Player trained', 'player': PlayerSerializer(player).data})

    @action(detail=True, methods=['post'])
    def renew_contract(self, request, pk=None):
        player = self.get_object()
        if player.team is None or player.team.owner != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        cost = int(player.value * 0.15)
        team = player.team
        
        if team.currency < cost:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        
        team.currency -= cost
        team.save()
        
        player.contract_expiry += 15
        player.save()
        
        return Response({'message': 'Contract renewed', 'player': PlayerSerializer(player).data})


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def place_bid(self, request, pk=None):
        auction = self.get_object()
        bid_amount = request.data.get('bid')
        
        if bid_amount <= auction.current_bid:
            return Response({'error': 'Bid must be higher than current bid'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_team = Team.objects.filter(owner=request.user).first()
        if not user_team or user_team.currency < bid_amount:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        
        auction.current_bid = bid_amount
        auction.high_bidder = request.user
        auction.save()
        
        return Response({'message': 'Bid placed', 'auction': AuctionSerializer(auction).data})


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def simulate(self, request, pk=None):
        match = self.get_object()
        if match.status != 'Scheduled':
            return Response({'error': 'Match cannot be simulated'}, status=status.HTTP_400_BAD_REQUEST)
        
        match.status = 'Live'
        match.save()
        
        return Response({'message': 'Match simulation started', 'match': MatchSerializer(match).data})


class PersonnelViewSet(viewsets.ModelViewSet):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = [IsAuthenticated]


class StadiumConfigViewSet(viewsets.ModelViewSet):
    queryset = StadiumConfig.objects.all()
    serializer_class = StadiumConfigSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def upgrade_seats(self, request, pk=None):
        stadium = self.get_object()
        cost = stadium.seats_level * 5000
        team = Team.objects.filter(stadium=stadium).first()
        
        if not team or team.currency < cost:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        
        team.currency -= cost
        team.save()
        
        stadium.seats_level += 1
        stadium.capacity += 2500
        stadium.save()
        
        return Response({'message': 'Seats upgraded', 'stadium': StadiumConfigSerializer(stadium).data})

    @action(detail=True, methods=['post'])
    def upgrade_food(self, request, pk=None):
        stadium = self.get_object()
        cost = stadium.food_level * 5000
        team = Team.objects.filter(stadium=stadium).first()
        
        if not team or team.currency < cost:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        
        team.currency -= cost
        team.save()
        
        stadium.food_level += 1
        stadium.save()
        
        return Response({'message': 'Food facilities upgraded', 'stadium': StadiumConfigSerializer(stadium).data})
