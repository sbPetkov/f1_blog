from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView

from .models import Race, Driver, RaceResult
from .forms import RaceResultForm


class DriverStandingsView(ListView):
    model = Driver
    template_name = 'standings/driver_standings.html'
    context_object_name = 'drivers'

    def get_queryset(self):
        return Driver.objects.order_by('-points')


def get_points(position):
    points = 0
    if position == 1:
        points = 25
    elif position == 2:
        points = 18
    elif position == 3:
        points = 15
    elif position == 4:
        points = 12
    elif position == 5:
        points = 10
    elif position == 6:
        points = 8
    elif position == 7:
        points = 6
    elif position == 8:
        points = 4
    elif position == 9:
        points = 2
    elif position == 10:
        points = 1
    return points


def submit_race_result(request):
    races = Race.objects.all()
    drivers = Driver.objects.all()
    if request.method == 'POST':
        form = RaceResultForm(request.POST)
        if form.is_valid():
            race = form.cleaned_data['race']
            fastest_lap_owner = form.cleaned_data['fastest_lap']
            for driver in drivers:
                position = form.cleaned_data[f"driver_{driver.id}"]
                if position:
                    driver_position = int(position)
                    driver_result = RaceResult.objects.create(
                        race=race,
                        driver=driver,
                        position=driver_position,
                        fastest_lap=(driver == fastest_lap_owner)
                    )
                    driver.points += get_points(driver_position)
                    if driver == fastest_lap_owner:
                        driver.points += 1
                    driver.save()
            return redirect('driver-standings')
    else:
        form = RaceResultForm()

    context = {
        'form': form,
        'races': races,
        'drivers': drivers
    }

    return render(request, 'standings/submit_race_result.html', context)


class RaceView(ListView):
    model = Race
    template_name = 'standings/races.html'
    context_object_name = 'races'

    def get_past_races(self):
        return Race.objects.filter(end_date__lt=timezone.now()).order_by('-end_date')

    def get_next_race(self):
        return Race.objects.filter(start_date__gte=timezone.now()).order_by('start_date').first()

    def get_other_races(self):
        next_race = self.get_next_race()
        if next_race:
            return Race.objects.exclude(pk=next_race.pk).exclude(end_date__lt=timezone.now()).order_by('start_date')
        else:
            return Race.objects.exclude(end_date__lt=timezone.now()).order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['past_races'] = self.get_past_races()
        context['next_race'] = self.get_next_race()
        context['other_races'] = self.get_other_races()
        return context


class TrackResultView(ListView):
    model = RaceResult
    template_name = 'standings/track_result.html'

    def get_race_results(self):
        pk = self.kwargs.get('pk')
        return RaceResult.objects.filter(race_id=pk).order_by('position')

    def get_race(self):
        pk = self.kwargs.get('pk')
        return Race.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race_results'] = self.get_race_results()
        context['race'] = self.get_race()
        return context

