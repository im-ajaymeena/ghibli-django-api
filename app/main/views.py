from rest_framework import generics
from main.models import Film
from main.serializers import FilmSerializer
from rest_framework.response import Response
from django.conf import settings


class FilmListView(generics.ListAPIView):
    serializer_class = FilmSerializer
    queryset = Film.objects.all()

    def list(self, request, *args, **kwargs):
        secret_key = request.META.get("HTTP_X_SECRET_KEY")
        
        if secret_key == settings.GHIBLIKEY:
            queryset = Film.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Access Denied - Unauthorized"}, status=403)