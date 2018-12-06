from movierating.models import Movie, MovieGenre
from api.serializers import MovieSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class MovieViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet provides both 'list' and 'detail' views.
	"""
	queryset = Movie.objects.order_by('movie_title')
	serializer_class = MovieSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		movie = self.get_object(pk)
		self.perform_destroy(self, movie)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()