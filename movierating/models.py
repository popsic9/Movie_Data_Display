# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


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
        if self.rating == None:
            return ""
        else:
            return str(self.rating)


            
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'genre'
        ordering = ['genre_name']
        verbose_name = 'Movie Genre Classification'
        verbose_name_plural = 'Movie Genre Classification'

    def __str__(self):
        return self.genre_name


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tag'
        ordering = ['tag_name']
        verbose_name = 'Movie Tag Classification'
        verbose_name_plural = 'Movie Tag Classification'

    def __str__(self):
        return self.tag_name



class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=100)
    imdbid = models.IntegerField(blank=True, null=True)
    tmdbid = models.IntegerField(blank=True, null=True)
    genre = models.ManyToManyField('Genre', through='MovieGenre')
    tag = models.ManyToManyField('Tag', through='MovieTag')
    user_rating = models.ManyToManyField('User', through='MovieRating')

    class Meta:
        managed = False
        db_table = 'movie'
        ordering = ['movie_title']
        verbose_name = 'Movie Description'
        verbose_name_plural = 'Movie Description'

    def __str__(self):
        return self.movie_title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk':self.pk})
    
    @property
    def genre_names(self):
        genres = self.genre.order_by('genre_name')
        names = []
        for g in genres:
            name = g.genre_name
            if name is None:
                continue
            if name not in names:
                names.append(name)
        names.sort()
        return ', '.join(names)

    @property
    def tag_names(self):
        tags = self.tag.order_by('tag_name')
        names = []
        for t in tags:
            name = t.tag_name
            if name is None:
                continue
            if name not in names:
                names.append(name)
        names.sort()
        return ', '.join(names)

    


class MovieRating(models.Model):
    movie_rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = 'movie_rating'
        ordering = ['user', 'movie', 'rating']
        verbose_name = 'User Movie Rating'
        verbose_name_plural = 'User Movie Rating'
    



class MovieGenre(models.Model):
    movie_genre_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'movie_genre'
        ordering = ['movie', 'genre']
        verbose_name = 'Movie Genres'
        verbose_name_plural = 'Movie Genres'


class MovieTag(models.Model):
    movie_tag_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'movie_tag'
        ordering = ['movie', 'tag']
        verbose_name = 'Movie Tags'
        verbose_name_plural = 'Movie Tags'





class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=45, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    zipcode = models.CharField(max_length=45, blank=True, null=True)
    age_range = models.ForeignKey(AgeRange, on_delete=models.PROTECT, blank=True, null=True)
    work = models.ForeignKey('Work', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        ordering = ['user_id']
        verbose_name = 'User Description'
        verbose_name_plural = 'User Description'

    def __str__(self):
        return str(self.user_id)



