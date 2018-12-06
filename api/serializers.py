from movierating.models import AgeRange, Work, Genre, Rating, \
	Movie, MovieRating, Tag, MovieGenre, User
from rest_framework import response, serializers, status



class AgeRangeSerializer(serializers.ModelSerializer):

	class Meta:
		model = AgeRange
		fields = ('age_range_id', 'age_range_name')


class WorkSerializer(serializers.ModelSerializer):

	class Meta:
		model = Work
		fields = ('work_id', 'work_name')

class UserSerializer(serializers.ModelSerializer):
	age_range = AgeRangeSerializer(many=False, read_only=True)
	work = WorkSerializer(many=False, read_only=True)

	class Meta:
		model = User
		fields = (
			'user_id',
			'gender',
			'age',
			'zipcode',
			'age_range',
			'work')

class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre
		fields = ('genre_id', 'genre_name')


class RatingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Rating
		fields = ('rating_id', 'rating')


class MovieRatingSerializer(serializers.ModelSerializer):
	movie_id = serializers.ReadOnlyField(source='movie.movie_id')
	user = UserSerializer(many=False, read_only=True)
	rating = RatingSerializer(many=False, read_only=True)

	class Meta:
		model = MovieRating
		fields = ('movie_rating_id', 'user', 'movie_id', 'rating', 'timestamp')




class TagSerializer(serializers.ModelSerializer):
	user = UserSerializer(many=False, read_only=True)
	movie_id = serializers.ReadOnlyField(source='movie.movie_id')

	class Meta:
		model = Tag
		fields = (
			'tag_id',
			'user',
			'movie_id',
			'tag',
			'timestamp')




class MovieGenreSerializer(serializers.ModelSerializer):
	movie_id = serializers.ReadOnlyField(source='movie.movie_id')
	genre_id = serializers.ReadOnlyField(source='genre.genre_id')

	class Meta:
		model = MovieGenre
		fields = ('movie_id', 'genre_id')





class MovieSerializer(serializers.ModelSerializer):
	movie_title = serializers.CharField(
		allow_blank=False,
		max_length=255
	)
	imdbid = serializers.IntegerField(
	)
	tmdbid = serializers.IntegerField(
	)

	movie_genre = MovieGenreSerializer(
		source='movie_genre_set', # Note use of _set
		many=True,
		read_only=True
	)
	movie_genre_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=Genre.objects.all(),
		source='movie_genre'
	)

	user_rating = MovieRatingSerializer(
		source='movie_rating_set', # Note use of _set
		many=True,
		read_only=True
	)
	user_rating_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=User.objects.all(),
		source='movie_rating'
	)

	class Meta:
		model = Movie
		fields = (
			'movie_id',
			'movie_title',
			'imdbid',
			'tmdbid',
			'movie_genre',
			'movie_genre_ids',
			'user_rating',
			'user_rating_ids'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		genres = validated_data.pop('movie_genre')
		movie = Movie.objects.create(**validated_data)

		if genres is not None:
			for g in genres:
				MovieGenre.objects.create(
					movie=movie.movie_id,
					genre=g.genre_id
				)
		return movie

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		m_id = instance.movie_id
		new_genre = validated_data.pop('movie_genre')

		instance.movie_title = validated_data.get(
			'movie_title',
			instance.movie_title
		)
		instance.imdbid = validated_data.get(
			'imdbid',
			instance.imdbid
		)
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = MovieGenre.objects \
			.values_list('genre_id', flat=True) \
			.filter(movie_id__exact=m_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for g in new_genre:
			new_id = g.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieGenre.objects \
					.create(movie_id=m_id, genre_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieGenre.objects \
					.filter(movie_id=m_id, genre_id=old_id) \
					.delete()

		return instance