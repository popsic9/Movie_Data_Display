from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy

from .models import User
from .models import Movie



def index(request):
   return HttpResponse("Hello, world. You're at the Movie Rating Display Sites Index.")

class AboutPageView(generic.TemplateView):
	template_name = 'movierating/about.html'

class HomePageView(generic.TemplateView):
	template_name = 'movierating/home.html'


class MovieListView(generic.ListView):
	model = Movie
	context_object_name = 'movies'
	template_name = 'movierating/movies.html'
	paginate_by = 300

	def get_queryset(self):
		return Movie.objects.all().order_by('movie_title')

class MovieDetailView(generic.DetailView):
	model = Movie
	context_object_name = 'movie'
	template_name = 'movierating/movie_detail.html'