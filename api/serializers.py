from movierating.models import AgeRange, Work, Genre, Rating, Movie, MovieRating, Tag, MovieGenre, User, MovieTag
from rest_framework import response, serializers, status






class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('tag_id', 'tag_name')


class MovieTagSerializer(serializers.ModelSerializer):
	tag_id = serializers.ReadOnlyField(source='tag.tag_id')
	tag_name = serializers.ReadOnlyField(source='tag.tag_name')

	class Meta:
		model = MovieTag
		fields = ('tag_id', 'tag_name')




class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre
		fields = ('genre_id', 'genre_name')


class MovieGenreSerializer(serializers.ModelSerializer):
	genre_id = serializers.ReadOnlyField(source='genre.genre_id')
	genre_name = serializers.ReadOnlyField(source='genre.genre_name')

	class Meta:
		model = MovieGenre
		fields = ('genre_id', 'genre_name')

class AgeRangeSerializer(serializers.ModelSerializer):

	class Meta:
		model = AgeRange
		fields = ('age_range_id', 'age_range_name')


class WorkSerializer(serializers.ModelSerializer):

	class Meta:
		model = Work
		fields = ('work_id', 'work_name')


class RatingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Rating
		fields = ('rating_id', 'rating')

class UserSerializer(serializers.ModelSerializer):
	age_range = AgeRangeSerializer(many=False, read_only=True)
	work = WorkSerializer(many=False, read_only=True)

	class Meta:
		model = User
		fields = ('user_id','gender','age','zipcode','age_range','work')


class MovieRatingSerializer(serializers.ModelSerializer):
	user = UserSerializer(many = False)
	rating = RatingSerializer(many=False, read_only=True)

	class Meta:
		model = MovieRating
		fields = ('user','rating')





class MovieRatingUserSerializer(serializers.Serializer):
	user_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=User.objects.all(), source='movieuser')
	rating_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Rating.objects.all(), source='movierate')





class MovieSerializer(serializers.ModelSerializer):
	movie_title = serializers.CharField(allow_blank=False,max_length=255)
	imdbid = serializers.IntegerField()
	tmdbid = serializers.IntegerField()
	movie_genres = MovieGenreSerializer(source='moviegenre_set',many=True,read_only=True)
	movie_genre_ids = serializers.PrimaryKeyRelatedField(many=True,write_only=True,queryset=Genre.objects.all(),source='moviegenre')
	movie_tags = MovieTagSerializer(source='movietag_set',many=True,read_only=True)
	movie_tag_ids = serializers.PrimaryKeyRelatedField(many=True,write_only=True,queryset=Tag.objects.all(),source='movietag')
	movie_rating = MovieRatingSerializer(source='movierating_set', many=True, read_only=True)


	movie_rating_ids = MovieRatingUserSerializer(many=True, write_only=True, source='movierating')


	class Meta:
		model = Movie
		fields = (
			'movie_id',
			'movie_title',
			'imdbid',
			'tmdbid',
			'movie_genres',
			'movie_genre_ids',
			'movie_tags',
			'movie_tag_ids',
			'movie_rating',
			'movie_rating_ids'
		)

	def create(self, validated_data):
		genres = validated_data.pop('moviegenre')
		tags = validated_data.pop('movietag')
		rating = validated_data.pop('movierating')
		newmovie = Movie.objects.create(**validated_data)

		if genres is not None:
			for g in genres:
				MovieGenre.objects.create(
					movie=newmovie,
					genre=g
				)
		
		if tags is not None:
			for t in tags:
				MovieTag.objects.create(
					movie=newmovie,
					tag=t
				)
		
		if rating is not None:
			for r in rating:
				movieuser = r['movieuser']
				movierate = r['movierate']
				MovieRating.objects.create(movie=newmovie, user=movieuser, rating=movierate)
					
		return newmovie

	def update(self, instance, validated_data):
		m_id = instance.movie_id
		new_genre = validated_data.pop('moviegenre')
		new_tag = validated_data.pop('movietag')
		new_rating = validated_data.pop('movierating')


		instance.movie_title = validated_data.get(
			'movie_title',
			instance.movie_title
		)
		
		instance.imdbid = validated_data.get(
			'imdbid',
			instance.imdbid
		)

		instance.tmdbid = validated_data.get(
			'tmdbid',
			instance.tmdbid
		)
		instance.save()

		# If any existing elements are not in updated list, delete them
		new_ids = []
		old_ids = MovieGenre.objects.values_list('genre_id', flat=True).filter(movie_id__exact=m_id)

		new_tag_ids = []
		old_tag_ids = MovieTag.objects.values_list('tag_id', flat=True).filter(movie_id__exact=m_id)

		new_user_ids = []
		#[tuple(user_id, rating_id)]
		old_user_ids = MovieRating.objects.values_list('user_id', 'rating_id').filter(movie_id__exact=m_id)


		# Insert new unmatched entries
		for g in new_genre:
			new_id = g.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieGenre.objects.create(movie_id=m_id, genre_id=new_id)

		for t in new_tag:
			new_id = t.tag_id
			new_tag_ids.append(new_id)
			if new_id in old_tag_ids:
				continue
			else:
				MovieTag.objects.create(movie_id=m_id, tag_id=new_id)
		
		for r in new_rating:
			movierate = r["movierate"]
			movieuser = r["movieuser"]
			new_rate_id = movierate.rating_id
			new_user_id = movieuser.user_id
			new_tuple = (new_user_id, new_rate_id)
			new_user_ids.append(new_tuple)
			if new_tuple in old_user_ids:
				continue
			else:
				MovieRating.objects.create(movie_id=m_id, user_id = new_user_id, rating_id = new_rate_id)


		# Delete old unmatched entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieGenre.objects.filter(movie_id=m_id, genre_id=old_id).delete()

		for old_id in old_tag_ids:
			if old_id in new_tag_ids:
				continue
			else:
				MovieTag.objects.filter(movie_id=m_id, tag_id=old_id).delete()

		for old_id in old_user_ids:
			if old_id in new_user_ids:
				continue
			else:
				MovieRating.objects.filter(movie_id=m_id, user_id = old_id[0], rating_id = old_id[1]).delete()


		return instance