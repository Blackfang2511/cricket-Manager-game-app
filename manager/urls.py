from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views
from . import auth_views

app_name = 'manager'

router = DefaultRouter()
router.register(r'users', api_views.UserProfileViewSet)
router.register(r'teams', api_views.TeamViewSet)
router.register(r'players', api_views.PlayerViewSet)
router.register(r'auctions', api_views.AuctionViewSet)
router.register(r'matches', api_views.MatchViewSet)
router.register(r'personnel', api_views.PersonnelViewSet)
router.register(r'stadiums', api_views.StadiumConfigViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/auth/login/', auth_views.login, name='login'),
    path('api/auth/register/', auth_views.register, name='register'),
    path('api/', include(router.urls)),
]
