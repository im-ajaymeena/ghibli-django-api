from django.db import models
    
class Location(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    climate = models.CharField(max_length=255)
    terrain = models.CharField(max_length=255)
    surface_water = models.CharField(max_length=255)
    residents = models.ManyToManyField('Person', related_name='locations')
    url = models.URLField()

    def __str__(self):
        return self.name

class Species(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    eye_colors = models.CharField(max_length=255)
    hair_colors = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

class Person(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    eye_color = models.CharField(max_length=255)
    hair_color = models.CharField(max_length=255)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    vehicle_class = models.CharField(max_length=255)
    image = models.URLField()
    length = models.CharField(max_length=10)
    pilot = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='vehicles', null=True)
    url = models.URLField()

    def __str__(self):
        return self.name

class Film(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    original_title_romanised = models.CharField(max_length=255)
    image = models.URLField()
    movie_banner = models.URLField()
    description = models.TextField()
    director = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    release_date = models.CharField(max_length=4)  # Assuming it's a year as a string
    running_time = models.CharField(max_length=10) 
    rt_score = models.CharField(max_length=10)
    url = models.URLField()
    
    people = models.ManyToManyField(Person)
    species = models.ManyToManyField(Species)
    locations = models.ManyToManyField(Location)
    vehicles = models.ManyToManyField(Vehicle)

    def __str__(self):
        return self.title