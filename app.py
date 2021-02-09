from flask import Flask, render_template, request
import requests
from backend import get_modified_request, add_posters

app = Flask(__name__)


@app.route('/')
def get_movies():
  chosen_genre = request.args.get('genre')
  if not chosen_genre:
    return render_template('index.html')
  else:
    api_request = get_modified_request(chosen_genre)
    response = requests.get(api_request)
    print(response)
    movies_results = response.json()['results']
    movies_results = add_posters(movies_results)
    return render_template('index.html',
                           chosen_genre=chosen_genre.title(),
                           movies_results=movies_results)
=======
from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)


@app.route('/')


def get_movies():

  chosen_genre = request.args.get('genre')

  if not chosen_genre:
    return render_template('index.html')

  api_request = get_modified_request(chosen_genre)

  response = requests.get(api_request)

  movies_results = response.json()['results']

  print(f'movie results: {type(movies_results)}')

  movies_results = add_posters(movies_results)

  print(request.args)

  return render_template('index.html',
    chosen_genre = chosen_genre.title(), movies_results=movies_results, )


def get_modified_request(chosen_genre):

  API_KEY = os.getenv('API_KEY')

  print(type(API_KEY))

  api_request = 'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&vote_count.gte=5000&vote_average.gte=7&with_genres=##&with_original_language=en'

  genre_id = get_genre_id(chosen_genre.lower(), API_KEY)

  api_request = api_request.replace('##', genre_id)

  api_request = api_request.replace('{API_KEY}', API_KEY)

  return api_request


def get_genre_id(chosen_genre, API_KEY):
  genres_dict = get_genres_dict(API_KEY)
  genre_id = genres_dict[chosen_genre]
  return str(genre_id)


def add_posters(movies_results):
  secure_base_url = 'https://image.tmdb.org/t/p/'
  poster_size = 'w185'

  for movie in movies_results:
    movie['poster'] = secure_base_url + poster_size + movie.get('poster_path')

  return movies_results


def get_genres_dict(API_KEY):

  request = 'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US'
  request = request.replace('{API_KEY}', API_KEY)
  resp = requests.get(request)
  genres = resp.json()['genres']
  genres_dict = {}

  for i in range(len(genres)):
      genres_dict[genres[i]['name'].lower()] = genres[i]['id']

  return genres_dict
>>>>>>> 16808abbf8d7c26c11142aa6af700f87e05eaa2d
