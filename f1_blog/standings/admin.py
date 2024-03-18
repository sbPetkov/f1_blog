from django.contrib import admin
from .models import Driver, Team, Race, RaceResult


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'points']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'points']



@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'track_length', 'start_date', 'end_date']


@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ['race', 'driver', 'position', 'fastest_lap']
