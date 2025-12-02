from django.urls import path
from api import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('check', views.CheckApiAPIView.as_view()),
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('team/info', views.TeamInfoApiAPIView.as_view()),
    path('team/matches', views.TeamMatchesApiAPIView.as_view()),

    path('player/search', views.SearchPlayerApiAPIView.as_view()),
    path('player/profile', views.PlayerProfileApiAPIView.as_view()),
    path('player/statistics', views.PlayerStatApiAPIView.as_view()),

    path('matches/upcoming', views.GetUpcomingMatchesApiAPIView.as_view()),
    path('matches/details', views.GetMatchDetailsApiAPIView.as_view()),

    path('tableau/tside', views.GetTableauTSideApiAPIView.as_view()),
    path('tableau/ctside', views.GetTableauCTSideApiAPIView.as_view()),
]
