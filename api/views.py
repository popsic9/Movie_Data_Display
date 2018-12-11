from movierating.models import Movie, MovieGenre, Genre
from api.serializers import MovieSerializer, GenreSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class MovieViewSet(viewsets.ModelViewSet):
	queryset = Movie.objects.all().order_by('movie_title')
	serializer_class = MovieSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		movie = self.get_object(pk)
		self.perform_destroy(self, movie)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()


# class GenreViewSet(viewsets.ModelViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer