from django.shortcuts import render, redirect
from .models import Movie
from django.contrib import messages

def home_page(request):
    user_query = str(request.GET.get('query', ''))
    # get all movie and filter by the user search
    search_result = Movie.objects.filter(name__icontains=user_query)
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'picture': request.POST.get('picture'),
            'rating': int(request.POST.get('rating')),
            'notes': request.POST.get('notes')
        }
        try:

            response = Movie.objects.create(
                name=data.get('name'),
                picture=data.get('picture'),
                rating=data.get('rating'),
                notes=data.get('notes'),

            )
            messages.success(request, 'New movie added: {}'.format(data.get('name')))
        except Exception as e:
            messages.warning(
                request, 'Got an error when trying to create new movie: {}'.format(e))
    return redirect('/')


def edit(request, movie_id):
    if request.method =='POST':
        # get the data posted edited in the form
        data = {
            'name':request.POST.get('name'),
            'picture': request.POST.get('picture'),
            'rating': int(request.POST.get('rating')),
            'notes': request.POST.get('notes'),
        }
        try:
            # and set the database old data with the new data gotten from the form
            movie_obj = Movie.objects.get(id=movie_id)
            movie_obj.name = data.get('name')
            movie_obj.picture = data.get('picture')
            movie_obj.rating = data.get('rating')
            movie_obj.notes = data.get('notes')
            movie_obj.save()
            messages.success(request, f"Movie Updated {data.get('name')}!")
        except Exception as e:
            messages.warning(request, f"Got an error when trying to update movie {e}.")
        return redirect('/')

def delete(request, movie_id):
    try:
        movie_obj = Movie.objects.get(id=movie_id)
        movie_name = movie_obj.name
        movie_obj.delete()
        messages.success(request, f"Movie deleted {movie_name}!")
    except Exception as e:
        messages.warning(request, f"Got an error when trying to delete movie {e}.")
    return redirect('/')
