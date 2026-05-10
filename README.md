# Cricket Dynasty Manager - Python/Django Version

A Django-based cricket franchise management simulation game with real-time WebSocket support. This is a Python replication of the original React/Firebase application, implementing all core features: squad management, player auctions, match simulations, stadium customization, and AI-driven player generation.

## Features

- **Team Management**: Create and manage cricket teams with budgets, fame levels, and training facilities
- **Player System**: Generate, recruit, train, and manage player squads
- **Auction System**: Real-time bidding on players via WebSockets
- **Match Simulation**: Dynamic cricket match engine with pitch/soil modifiers
- **Stadium Management**: Customize facilities and manage revenue
- **Personnel Hiring**: Recruit coaches, scouts, medical staff, and marketers
- **Day Advancement**: Time progression system with contract expirations and auto-auctions
- **AI Integration**: Google Gemini API for player generation and logo creation
- **Real-time Updates**: WebSocket support for live auctions and match commentary

## Tech Stack

- **Framework**: Django 6.0.5
- **API**: Django REST Framework 3.17.1
- **Real-time**: Django Channels 4.3.2 with Redis
- **Database**: MSSQL/SQLite (configurable via environment)
- **AI**: Google Generative AI (Gemini)
- **Python**: 3.10+

## Project Structure

```
cricket-dynasty-manager-python/
├── cricket_dynasty/           # Main Django project
│   ├── settings.py           # Configuration (database, Channels, apps)
│   ├── urls.py              # URL routing
│   ├── asgi.py              # ASGI config for Channels
│   ├── wsgi.py              # WSGI config
│   └── __init__.py
├── manager/                  # Core application
│   ├── models.py            # Data models (Team, Player, Match, etc.)
│   ├── views.py             # View logic
│   ├── serializers.py       # REST Framework serializers
│   ├── consumers.py         # WebSocket consumers (auctions, matches)
│   ├── routing.py           # WebSocket URL routing
│   ├── services.py          # Business logic (player generation, day advancement)
│   ├── admin.py             # Django admin registration
│   ├── urls.py              # App-level URL patterns
│   └── migrations/          # Database migrations
├── templates/               # Django templates
│   └── manager/
│       └── index.html       # Main template
├── static/                  # Static files (CSS, JS)
├── manage.py               # Django CLI
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Redis server (for WebSocket support)
- Git
- Virtual environment manager (venv)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cricket-dynasty-manager-python
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your settings:
   - `DJANGO_SECRET_KEY`: Generate a secure key
   - `DEBUG`: Set to False in production
   - `DATABASE_*`: Configure MSSQL or SQLite
   - `REDIS_URL`: Redis connection string
   - `GEMINI_API_KEY`: Your Google Gemini API key

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (for Django admin)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

   For WebSocket support, use Daphne ASGI server:
   ```bash
   pip install daphne
   daphne -b 0.0.0.0 -p 8000 cricket_dynasty.asgi:application
   ```

## API Endpoints

### WebSocket Endpoints

- `ws://localhost:8000/ws/auctions/` - Real-time auction updates
- `ws://localhost:8000/ws/matches/` - Live match simulation commentary

### REST API (to be implemented)

- `/api/teams/` - Team management
- `/api/players/` - Player roster
- `/api/auctions/` - Auction listings
- `/api/matches/` - Match schedules and results
- `/api/stadium/` - Stadium management
- `/api/personnel/` - Staff hiring

## Data Models

### Core Models

- **UserProfile**: User account and manager stats
- **Team**: Cricket franchise with budget, fame, and facilities
- **Player**: Team member with stats, role, and contract
- **Auction**: Active player auctions with bidding
- **Match**: Cricket match fixtures and results
- **Stadium**: Venue configuration and revenue management
- **Personnel**: Coaching and support staff
- **StadiumConfig**: Stadium specifications and upgrades

## Business Logic

### Match Simulation Engine

- 20 overs per innings, 6 balls per over
- 10 wicket maximum per team
- Dynamic pitch modifiers (Green, Dust Bowl, Flat, Hard, Soft, etc.)
- Soil type modifiers (Red, Black)
- Powerplay bonus (overs 1-6: 1.4x aggression)
- Fatigue factor progression through match
- Probabilistic outcome distribution (wicket, dot, single, 4, 6)

### Player Generation Algorithm

- 10% star players (75-95 stats), 90% regular (40-75)
- Role-specific stat penalties (Bowlers: -30 batting, etc.)
- Randomized career stats and contract duration (20-40 days)
- Marketplace maintains ~100 active auctions with auto-replenishment

### Day Advancement System

- Manual trigger (future: scheduled nightly tasks)
- Contract expiry countdown (-1 per day)
- Automatic auction creation when contract expires
- Stadium revenue calculation based on fame, attendance, facilities
- Base subsidy + stadium income deposit

## Development

### Running Tests

```bash
python manage.py test
```

### Django Admin

Access admin panel at: `http://localhost:8000/admin/`

### Database Migrations

Create new migrations after model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Configuration

### Database Options

**SQLite (default for development):**
```env
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

**MSSQL:**
```env
DATABASE_ENGINE=mssql
DATABASE_NAME=cricket_dynasty
DATABASE_USER=sa
DATABASE_PASSWORD=YourPassword
DATABASE_HOST=localhost
DATABASE_PORT=1433
DATABASE_DRIVER=ODBC Driver 18 for SQL Server
```

### Redis Configuration

```env
REDIS_URL=redis://127.0.0.1:6379
```

For production, use a managed Redis service (AWS ElastiCache, Azure Cache, etc.)

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Generate secure `DJANGO_SECRET_KEY`
- [ ] Configure MSSQL or PostgreSQL
- [ ] Set up Redis for production
- [ ] Configure allowed hosts
- [ ] Enable HTTPS/SSL
- [ ] Run `python manage.py collectstatic`
- [ ] Use gunicorn/uWSGI + daphne for ASGI
- [ ] Set up background task queue (Celery for scheduled tasks)

### Docker Deployment

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "cricket_dynasty.asgi:application"]
```

## Roadmap

- [ ] Complete REST API endpoints
- [ ] Frontend integration (React or Django templates)
- [ ] Match visualization with live graphics
- [ ] Gemini AI player generation
- [ ] Scheduled day advancement (APScheduler)
- [ ] Player stat decay over time
- [ ] League management and rankings
- [ ] Mobile app support
- [ ] Multi-language support
- [ ] Payment integration for premium features

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add feature description"`
3. Push to branch: `git push origin feature/your-feature`
4. Open a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please open a GitHub issue or contact the development team.

## Related Projects

- Original React/Firebase version: [cricket-dynasty-manager](https://github.com/user/cricket-dynasty-manager)
- AI Playground: https://ai.studio/apps/47ae0e92-7133-41bf-94a2-8821e3d71b69
