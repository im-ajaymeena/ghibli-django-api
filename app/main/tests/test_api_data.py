from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from main.models import Film, Person, Species
import uuid

class FilmListDataTest(TestCase):
    def setUp(self):
        self.species = Species.objects.create(
            id=uuid.UUID("af3910a6-429f-4c74-9ad5-dfe1c4aa04f2"),
            name='Human',
            classification='Mammal',
            eye_colors='Black, Blue, Brown, Grey, Green, Hazel',
            hair_colors='Black, Blonde, Brown, Grey, White',
            url='https://ghibli.rest/species?id=af3910a6-429f-4c74-9ad5-dfe1c4aa04f2'
        )

        self.people = Person.objects.create(
            id=uuid.UUID("598f7048-74ff-41e0-92ef-87dc1ad980a9"),
            name='Lusheeta Toel Ul Laputa',
            gender='Female',
            age='13',
            eye_color='Black',
            hair_color='Black',
            species=self.species,
            url='https://ghibli.rest/people?id=598f7048-74ff-41e0-92ef-87dc1ad980a9'
        )

        self.film = Film.objects.create(
            id=uuid.UUID("2baf70d1-42bb-4437-b551-e5fed5a87abe"),
            title='Castle in the Sky',
            original_title='天空の城ラピュタ',
            original_title_romanised='Tenkū no shiro Rapyuta',
            image='https://image.tmdb.org/t/p/w600_and_h900_bestv2/npOnzAbLh6VOIu3naU5QaEcTepo.jpg',
            movie_banner='https://image.tmdb.org/t/p/w533_and_h300_bestv2/3cyjYtLWCBE1uvWINHFsFnE8LUK.jpg',
            description='The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of Laputa...',
            director='Hayao Miyazaki',
            producer='Isao Takahata',
            release_date='1986',
            running_time='124',
            rt_score='95',
        )
        self.film.people.add(self.people)

        # authenticate the api with the secret key
        self.valid_secret_key = settings.GHIBLIKEY
        self.client.defaults['HTTP_X_SECRET_KEY'] = self.valid_secret_key

    def test_film_api_format(self):
        response = self.client.get(reverse('film-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data[0]['id'], '2baf70d1-42bb-4437-b551-e5fed5a87abe')
        self.assertEqual(data[0]['title'], 'Castle in the Sky')
        self.assertEqual(data[0]['original_title'], '天空の城ラピュタ')
        self.assertEqual(data[0]['original_title_romanised'], 'Tenkū no shiro Rapyuta')
        self.assertEqual(data[0]['image'], 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/npOnzAbLh6VOIu3naU5QaEcTepo.jpg')
        self.assertEqual(data[0]['movie_banner'], 'https://image.tmdb.org/t/p/w533_and_h300_bestv2/3cyjYtLWCBE1uvWINHFsFnE8LUK.jpg')
        self.assertEqual(data[0]['description'], 'The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of Laputa...')
        self.assertEqual(data[0]['director'], 'Hayao Miyazaki')
        self.assertEqual(data[0]['producer'], 'Isao Takahata')
        self.assertEqual(data[0]['release_date'], '1986')
        self.assertEqual(data[0]['running_time'], '124')
        self.assertEqual(data[0]['rt_score'], '95')

        # Check the actors field format
        actors = data[0]['actors']
        self.assertEqual(len(actors), 1)
        actor = actors[0]
        self.assertEqual(actor['id'], '598f7048-74ff-41e0-92ef-87dc1ad980a9')
        self.assertEqual(actor['name'], 'Lusheeta Toel Ul Laputa')
        self.assertEqual(actor['species'], 'Human')
        self.assertEqual(actor['url'], 'https://ghibli.rest/people?id=598f7048-74ff-41e0-92ef-87dc1ad980a9')
