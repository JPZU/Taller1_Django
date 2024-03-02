from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
# create your views here

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Paola Vallejo'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})


def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()
    
    movie_counts_by_genre = {}
    movie_counts_by_year = {}
    
    for movie in all_movies:
        genres = movie.genre.split(',') 
        genre = genres[0].strip() if genres else "None"
        
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1
    
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
            
    # Gráfico 1: Movies per genre
    bar_width = 0.5
    bar_positions_1 = range(len(movie_counts_by_genre))
    
    plt.bar(bar_positions_1, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_1, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3) 
    buffer_1 = io.BytesIO()
    plt.savefig(buffer_1, format='png')
    buffer_1.seek(0)
    plt.close()
    
    image_png_1 = buffer_1.getvalue()
    buffer_1.close()
    graphic_1 = base64.b64encode(image_png_1)
    graphic_1 = graphic_1.decode('utf-8')
    
    # Gráfico 2: Movies per year
    bar_positions_2 = range(len(movie_counts_by_year))
    
    plt.bar(bar_positions_2, movie_counts_by_year.values(), width=bar_width, align='center', color='orange')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_2, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3) 
    buffer_2 = io.BytesIO()
    plt.savefig(buffer_2, format='png')
    buffer_2.seek(0)
    plt.close()
    
    image_png_2 = buffer_2.getvalue()
    buffer_2.close()
    graphic_2 = base64.b64encode(image_png_2)
    graphic_2 = graphic_2.decode('utf-8')
    
    return render(request, 'statistics.html', {'graphic_1': graphic_1, 'graphic_2': graphic_2})
        