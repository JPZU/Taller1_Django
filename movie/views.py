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
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'signup.html')

def statistics_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()
    
    movie_counts_by_genre = {}
    
    
    for movie in all_movies:
        
        genres = movie.genre.split(',') 
        genre = genres[0].strip() if genres else "None"
        
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1
            
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_genre))
    
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3) 
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return render(request, 'statistics.html', {'graphic': graphic})
        