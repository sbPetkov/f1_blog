from django import forms
from .models import Race, Driver


class RaceResultForm(forms.Form):
    race = forms.ModelChoiceField(queryset=Race.objects.all(), empty_label=None)
    fastest_lap = forms.ModelChoiceField(queryset=Driver.objects.all(), empty_label=None, label='Driver with Fastest Lap')

    def __init__(self, *args, **kwargs):
        super(RaceResultForm, self).__init__(*args, **kwargs)
        drivers = Driver.objects.all()
        position_choices = [(i, f"-{i}-") for i in range(1, 21)]
        for driver in drivers:
            field_name = f"driver_{driver.id}"
            self.fields[field_name] = forms.ChoiceField(choices=position_choices, widget=forms.Select(attrs={'class': 'position-select'}), required=False)
            self.fields[field_name].label = driver.name  # Set label to driver's name
