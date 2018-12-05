from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy

from .models import User
from .models import Movie
from .models import MovieGenre

from .forms import MovieForm
from .filters import MovieFilter
from django_filters.views import FilterView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django import forms


def index(request):
   return HttpResponse("Hello, world. You're at the Movie Rating Display Sites Index.")

class AboutPageView(generic.TemplateView):
	template_name = 'movierating/about.html'

class HomePageView(generic.TemplateView):
	template_name = 'movierating/home.html'


@method_decorator(login_required, name='dispatch')
class MovieListView(generic.ListView):
	model = Movie
	context_object_name = 'movies'
	template_name = 'movierating/movies.html'
	paginate_by = 300

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Movie.objects.all().order_by('movie_title')

@method_decorator(login_required, name='dispatch')
class MovieDetailView(generic.DetailView):
	model = Movie
	context_object_name = 'movie'
	template_name = 'movierating/movie_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)




# how to update user information
@method_decorator(login_required, name='dispatch')
class MovieCreateView(generic.View):
	model = Movie
	form_class = MovieForm

	success_message = "Movie created successfully"
	template_name = 'movierating/movie_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = MovieForm(request.POST)
		if form.is_valid():
			newmovie = form.save(commit=False)
			l = len(Movie.objects.all())
			newmovie.movie_id = l + 1;
			newmovie.save()
			#many to many for genre
			for g in form.cleaned_data['genre']:
				MovieGenre.objects.create(movie=newmovie, genre=g)
			return redirect(newmovie)
		return render(request, 'movierating/movie_new.html', {'form': form})

	def get(self, request):
		form = MovieForm()
		return render(request, 'movierating/movie_new.html', {'form': form})











@method_decorator(login_required, name='dispatch')
class MovieDeleteView(generic.DeleteView):
	model = Movie
	success_message = "Movie deleted successfully"
	success_url = reverse_lazy('movies')
	context_object_name = 'movie'
	template_name = 'movierating/movie_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete Movie Genre entries
		MovieGenre.objects \
			.filter(movie_id=self.object.movie_id) \
			.delete()

		self.object.delete()
		return HttpResponseRedirect(self.get_success_url())











@method_decorator(login_required, name='dispatch')
class MovieUpdateView(generic.UpdateView):
	model = Movie
	form_class = MovieForm
	#fields = '__all__' #<-- superseded by form_class
	context_object_name = 'movie'
	# pk_url_kwarg = 'site_pk'
	success_message = "Movie updated successfully"
	template_name = 'movierating/movie_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)


	def form_valid(self, form):
		newmovie = form.save(commit=False)
		newmovie.save()

		# Current country_area_id values linked to site
		old_ids = MovieGenre.objects\
			.values_list('genre_id', flat=True)\
			.filter(movie_id=newmovie.movie_id)

		# New countries list
		new_genres = form.cleaned_data['genre']

		# New ids
		new_ids = []

		# Insert new unmatched country entries
		for g in new_genres:
			new_id = g.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieGenre.objects.create(movie=newmovie, genre=g)

		# Delete old unmatched movie genre entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieGenre.objects \
					.filter(movie_id=newmovie.movie_id, genre_id=old_id) \
					.delete()

		return HttpResponseRedirect(newmovie.get_absolute_url())










class MovieFilterView(FilterView):
	filterset_class = MovieFilter
	template_name = 'movierating/movie_filter.html'


