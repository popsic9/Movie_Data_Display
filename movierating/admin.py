# Register your models here.
from django.contrib import admin

import movierating.models as models


@admin.register(models.AgeRange)
class AgeRangeAdmin(admin.ModelAdmin):
	fields = ['age_range_name']
	list_display = ['age_range_name']
	ordering = ['age_range_name']


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
	fields = ['genre_name']
	list_display = ['genre_name']
	ordering = ['genre_name']


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
	fields = ['rating']
	list_display = ['rating']
	ordering = ['rating']


@admin.register(models.Work)
class WorkAdmin(admin.ModelAdmin):
	fields = ['work_name']
	list_display = ['work_name']
	ordering = ['work_name']



# how to deal with many-to-many relationship
@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
	fields = [
		'movie_title',
		'imdbid',
		'tmdbid',
	]

	list_display = [
		'movie_title',
		'imdbid',
		'tmdbid',
	]



@admin.register(models.MovieGenre)
class MovieGenreAdmin(admin.ModelAdmin):
	fields = [
		'movie',
		'genre'
	]

	list_display = [
		'movie',
		'genre'
	]


@admin.register(models.MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
	fields = [
		'user',
		'movie',   
        'rating',
        'timestamp'
	]

	list_display = [
		'user',
		'movie',    
        'rating',
        'timestamp'
	]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
	fields = [
		'user',
		'movie',
        'tag',
        'timestamp'
	]

	list_display = [
		'user',
		'movie',
        'tag',
        'timestamp'
	]
	list_filter = ['user', 'movie', 'tag']

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
	fields = [
		'user_id',
		'gender',
        'age',
        'zipcode',
        'age_range',
        'work'
	]

	list_display = [
		'user_id',
		'gender',
        'age',
        'zipcode',
        'age_range',
        'work'
	]
	list_filter = ['gender', 'age_range', 'work']
