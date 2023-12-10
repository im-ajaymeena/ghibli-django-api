from django.core.management.base import BaseCommand
from main.models import Film, Person, Vehicle, Species, Location
import requests
from urllib.parse import urlparse, parse_qs
from django.db import transaction


class Command(BaseCommand):
    def find_object_by_id(self, object_list, object_id):
        for obj in object_list:
            if obj["id"] == object_id:
                return obj
        return None

    def extract_id_from_url(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        id_value = query_params.get("id", [None])[0]
        return id_value

    def handle(self, *args, **options):

        with transaction.atomic():
            response = requests.get("https://ghibli.rest/films")
            films_list_response = response.json()

            species_list_response = requests.get("https://ghibli.rest/species")
            self.species_list = species_list_response.json()

            locations_list_response = requests.get("https://ghibli.rest/locations")
            self.locations_list = locations_list_response.json()

            vehicles_list_response = requests.get("https://ghibli.rest/vehicles")
            self.vehicles_list = vehicles_list_response.json()

            people_list_response = requests.get("https://ghibli.rest/people")
            self.people_list = people_list_response.json()

            new_films = []

            for api_film in films_list_response:
                film_id = api_film["id"]

                # Check if the film already exists in the database
                try:
                    film = Film.objects.get(id=film_id)
                except Film.DoesNotExist:
                    # If it doesn't exist, create a new film object
                    # Update film fields from the API data
                    film = Film(id=film_id)
                    film.title = api_film["title"]
                    film.original_title = api_film["original_title"]
                    film.original_title_romanised = api_film["original_title_romanised"]
                    film.image = api_film["image"]
                    film.movie_banner = api_film["movie_banner"]
                    film.description = api_film["description"]
                    film.director = api_film["director"]
                    film.producer = api_film["producer"]
                    film.release_date = api_film["release_date"]
                    film.running_time = api_film["running_time"]
                    film.rt_score = api_film["rt_score"]
                    film.url = api_film["url"]
                    film.save()

                    species_objs = self.get_related_species(api_film["species"])
                    if species_objs:
                        film.species.add(*species_objs)

                    person_objs = self.get_related_people(api_film["people"])

                    if person_objs:
                        film.people.add(*person_objs)

                    locations_objs = self.get_related_locations(api_film["locations"])
                    if locations_objs:
                        film.locations.add(*locations_objs)

                    vehicles_objs = self.get_related_vehicles(api_film["vehicles"])
                    if vehicles_objs:
                        film.vehicles.add(*vehicles_objs)
                    film.save()

                    new_films.append(film)
            
            # Delete films that are not present in the API
            Film.objects.exclude(
                id__in=[api_film["id"] for api_film in films_list_response]
            ).delete()

    def get_related_species(self, api_species_url_list):
        species_objs = []
        new_species_objs = []

        for api_species_url in api_species_url_list:
            species_id = self.extract_id_from_url(api_species_url)
            if not species_id:
                continue
            api_species = self.find_object_by_id(self.species_list, species_id)

            try:
                species = Species.objects.get(id=species_id)
            except Species.DoesNotExist:
                species = Species(id=species_id)
                species.name = api_species["name"]
                species.classification = api_species["classification"]
                species.eye_colors = api_species["eye_colors"]
                species.hair_colors = api_species["hair_colors"]
                species.url = api_species["url"]

                new_species_objs.append(species)

            species_objs.append(species)

        Species.objects.bulk_create(new_species_objs)

        return species_objs

    def get_related_locations(self, api_location_url_list):
        location_objs = []
        new_location_objs = []

        for api_location_url in api_location_url_list:
            location_id = self.extract_id_from_url(api_location_url)
            if not location_id:
                continue
            api_location = self.find_object_by_id(self.locations_list, location_id)

            try:
                location = Location.objects.get(id=location_id)
            except Location.DoesNotExist:
                location = Location(id=location_id)
                location.name = api_location["name"]
                location.climate = api_location["climate"]
                location.terrain = api_location["terrain"]
                location.surface_water = api_location["surface_water"]
                location.url = api_location["url"]
                people_objs = self.get_related_people(api_location["residents"])
                location.residents.add(*people_objs)

                new_location_objs.append(location)

            location_objs.append(location)

        Location.objects.bulk_create(new_location_objs)

        return location_objs

    def get_related_vehicles(self, api_vehicle_url_list):
        vehicle_objs = []
        new_vehicle_objs = []

        for api_vehicle_url in api_vehicle_url_list:
            vehicle_id = self.extract_id_from_url(api_vehicle_url)
            if not vehicle_id:
                continue
            api_vehicle = self.find_object_by_id(self.vehicles_list, vehicle_id)

            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
            except Vehicle.DoesNotExist:
                vehicle = Vehicle(id=vehicle_id)
                vehicle.name = api_vehicle["name"]
                vehicle.description = api_vehicle["description"]
                vehicle.vehicle_class = api_vehicle["vehicle_class"]
                vehicle.image = api_vehicle["image"]
                vehicle.length = api_vehicle["length"]
                vehicle.url = api_vehicle["url"]
                pilot = self.get_related_people([api_vehicle["pilot"]])
                if pilot:
                    vehicle.pilot = pilot[0]

                new_vehicle_objs.append(vehicle)

            vehicle_objs.append(vehicle)

        Vehicle.objects.bulk_create(new_vehicle_objs)

        return vehicle_objs

    def get_related_people(self, api_person_url_list):
        person_objs = []
        new_person_objs = []

        for api_person_url in api_person_url_list:
            person_id = self.extract_id_from_url(api_person_url)
            if not person_id:
                continue
            api_person = self.find_object_by_id(self.people_list, person_id)

            try:
                person = Person.objects.get(id=person_id)
            except Person.DoesNotExist:
                person = Person(id=person_id)
                person.name = api_person["name"]
                person.gender = api_person["gender"]
                person.age = api_person["age"]
                person.eye_color = api_person["eye_color"]
                person.hair_color = api_person["hair_color"]
                person.url = api_person["url"]
                species_objs = self.get_related_species([api_person["species"]])
                if species_objs:
                    person.species = species_objs[0]

                new_person_objs.append(person)

            person_objs.append(person)

        Person.objects.bulk_create(new_person_objs)

        return person_objs
