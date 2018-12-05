from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from movierating.models import Movie, Genre
from django.forms.widgets import CheckboxSelectMultiple


class MovieForm(forms.ModelForm):
	imdbid = forms.IntegerField(required=False)
	tmdbid = forms.IntegerField(required=False)
	

	class Meta:
		model = Movie
		fields = {'movie_title', 'imdbid', 'tmdbid', 'genre'}
		#fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['genre'].widget = CheckboxSelectMultiple()
		self.fields['genre'].queryset = Genre.objects.all()
		#self.fields['user_rating'].widget = forms.widgets.CheckboxSelectMultiple()
		#print(self.fields)

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))