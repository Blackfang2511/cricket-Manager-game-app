import random
from datetime import datetime, timedelta
from .models import Player, Team

ROLE_STAT_PENALTIES = {
    'Batsman': {'bowling': -30, 'batting': 0},
    'Bowler': {'batting': -30, 'bowling': 0},
    'Allrounder': {'batting': -10, 'bowling': -10},
    'Wicketkeeper': {'bowling': -20, 'batting': 0},
}

PLAYER_ROLES = ['Batsman', 'Bowler', 'Allrounder', 'Wicketkeeper']
BOWLING_TYPES = ['Fast', 'Spin', 'Medium', 'None']


def generate_player(name: str, role: str = None, team=None) -> Player:
    role = role or random.choice(PLAYER_ROLES)
    bowling_type = 'None' if role == 'Batsman' else random.choice(BOWLING_TYPES)
    base = random.randint(40, 75)
    is_star = random.random() < 0.1
    if is_star:
        base = random.randint(75, 95)

    penalties = ROLE_STAT_PENALTIES.get(role, {})
    batting = max(1, min(99, base + penalties.get('batting', 0)))
    bowling = max(1, min(99, base + penalties.get('bowling', 0)))
    stamina = max(1, min(99, random.randint(base - 10, base + 10)))
    fielding = max(1, min(99, random.randint(base - 10, base + 10)))

    value = 10000 + (batting + bowling + stamina + fielding) * 250
    expiry = random.randint(20, 40)

    player = Player(
        name=name,
        role=role,
        bowling_type=bowling_type,
        batting=batting,
        bowling=bowling,
        stamina=stamina,
        fielding=fielding,
        value=value,
        contract_expiry=expiry,
        career_stats={'matches': 0, 'runs': 0, 'wickets': 0},
    )
    if team is not None:
        player.team = team
    return player


def advance_day(team: Team):
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
