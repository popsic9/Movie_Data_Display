from django.urls import path, re_path
from . import views

urlpatterns = [
   path('', views.HomePageView.as_view(), name='home'),
   path('about/', views.AboutPageView.as_view(), name='about'),
   path('movies/', views.MovieListView.as_view(), name='movies'),
   path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
   path('movies/new/', views.MovieCreateView.as_view(), name='movie_new'),
   path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),
   path('movies/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie_update'),
   path('filter', views.MovieFilterView.as_view(), name='filter'),
]