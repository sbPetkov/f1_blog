from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def calculate_total_points(self):
        total_points = 0
        for driver in self.drivers.all():
            total_points += driver.points
        return total_points


class Driver(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='drivers')
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Race(models.Model):
    title = models.CharField(max_length=100)
    track_length = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='race_layout/')
    flag = models.ImageField(upload_to='race_layout/',
                             blank=True,
                             null=True)

    def __str__(self):
        return self.title


class RaceResult(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    position = models.IntegerField()  # Finishing position
    fastest_lap = models.BooleanField()  # True if the driver had the fastest lap

    def __str__(self):
        return f"{self.driver.name} - Race: {self.race}, Position: {self.position}, Fastest Lap: {self.fastest_lap}"
