from django.contrib import admin
from main.models import Film, Species, Vehicle, Location, Person
# Register your models here.

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'climate', 'terrain', 'surface_water')
    list_filter = ('climate', 'terrain')
    search_fields = ('name', 'climate', 'terrain')

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification', 'eye_colors', 'hair_colors')
    list_filter = ('classification',)
    search_fields = ('name', 'classification')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'age', 'eye_color', 'hair_color')
    list_filter = ('gender', 'eye_color', 'hair_color')
    search_fields = ('name', 'gender', 'eye_color', 'hair_color')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'vehicle_class', 'length')
    list_filter = ('vehicle_class',)
    search_fields = ('name', 'vehicle_class')

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_title', 'release_date', 'director')
    list_filter = ('release_date', 'director', 'producer')
    search_fields = ('title', 'director', 'producer')
