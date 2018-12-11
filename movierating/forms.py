from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from movierating.models import Movie, Genre, MovieRating, Rating, Tag
from django.forms.widgets import CheckboxSelectMultiple
from django.core.validators import MaxValueValidator, MinValueValidator


class MovieForm(forms.ModelForm):
	imdbid = forms.IntegerField(required=False)
	tmdbid = forms.IntegerField(required=False)
	#CHOICES = [x.tag_name for x in Tag.objects.all()]
	#tag = forms.CharField(required=False)
	#tag = forms.MultipleChoiceField(choices=CHOICES, widget=forms.SelectMultiple, required=False)
	

	class Meta:
		model = Movie
		fields = {'movie_title', 'imdbid', 'tmdbid', 'genre', 'tag'}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['genre'].widget = CheckboxSelectMultiple()
		self.fields['genre'].queryset = Genre.objects.all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))


class MovieRatingForm(forms.ModelForm):
	timestamp = forms.IntegerField(required=False)

	class Meta:
		model = MovieRating
		fields = {'user', 'rating', 'timestamp'}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))

	