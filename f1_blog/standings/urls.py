from django.urls import path
from .views import DriverStandingsView, submit_race_result, RaceView, TrackResultView

urlpatterns = [
    path('', DriverStandingsView.as_view(), name='driver-standings'),
    path('submit-race-result/', submit_race_result, name='submit-race-result'),
    path('tracks/', RaceView.as_view(), name='tracks'),
    path('track/results/<int:pk>', TrackResultView.as_view(), name='track-result')
]
