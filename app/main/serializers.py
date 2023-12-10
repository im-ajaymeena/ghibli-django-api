from rest_framework import serializers
from main.models import Film, Person

class ActorSerializer(serializers.ModelSerializer):
    species = serializers.SerializerMethodField(read_only=True)

    def get_species(self, obj):
        if obj.species:
            return obj.species.name
        return None

    class Meta:
        model = Person
        fields = ('id', 'name', 'species', 'url')

class FilmSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, source='people')

    class Meta:
        model = Film
        exclude = ('people',)