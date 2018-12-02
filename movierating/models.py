# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AgeRange(models.Model):
    age_range_id = models.AutoField(primary_key=True)
    age_range_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'age_range'
        ordering = ['age_range_name']
        verbose_name = 'User Age Range Classification'
        verbose_name_plural = 'User Age Range Classification'

    def __str__(self):
        return self.age_range_name


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'genre'
        ordering = ['genre_name']
        verbose_name = 'Movie Genre Classification'
        verbose_name_plural = 'Movie Genre Classification'

    def __str__(self):
        return self.genre_name


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rating = models.FloatField(unique=True)

    class Meta:
        managed = False
        db_table = 'rating'
        ordering = ['rating']
        verbose_name = 'Movie Rating Classification'
        verbose_name_plural = 'Movie Rating Classification'

    def __str__(self):
        return self.rating


class Work(models.Model):
    work_id = models.AutoField(primary_key=True)
    work_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'work'
        ordering = ['work_name']
        verbose_name = 'User Work Classification'
        verbose_name_plural = 'User Work Classification'

    def __str__(self):
        return self.work_name



class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    movie_title = models.CharField(max_length=100)
    imdbid = models.IntegerField(blank=True, null=True)
    tmdbid = models.IntegerField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='MovieGenre')
    rating = models.ManyToManyField(Rating, through='MovieRating')
    

    class Meta:
        managed = False
        db_table = 'movie'
        ordering = ['movie_title']
        verbose_name = 'Movie Description'
        verbose_name_plural = 'Movie Description'

    def __str__(self):
        return self.movie_title


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    genre = models.ForeignKey(Genre, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'movie_genre'
        ordering = ['movie', 'genre']
        verbose_name = 'Movie Genres'
        verbose_name_plural = 'Movie Genres'


class MovieRating(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    rating = models.ForeignKey('Rating', models.DO_NOTHING)
    timestamp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_rating'
        ordering = ['user', 'movie', 'rating']
        verbose_name = 'User Movie Rating'
        verbose_name_plural = 'User Movie Rating'





class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    tag = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tag'
        ordering = ['user', 'movie', 'tag']
        verbose_name = 'User Movie Tag'
        verbose_name_plural = 'User Movie Tag'

    def __str__(self):
        return self.user + "'s tag for movie " + self.movie + " is " + self.tag


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=45, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    zipcode = models.CharField(max_length=45, blank=True, null=True)
    age_range = models.ForeignKey(AgeRange, models.DO_NOTHING, blank=True, null=True)
    work = models.ForeignKey('Work', models.DO_NOTHING, blank=True, null=True)
    rating = models.ManyToManyField(Rating, through='MovieRating')

    class Meta:
        managed = False
        db_table = 'user'
        ordering = ['user_id']
        verbose_name = 'User Description'
        verbose_name_plural = 'User Description'

    def __str__(self):
        return self.user_id



