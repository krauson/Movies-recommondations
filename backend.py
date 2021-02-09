import os
import requests


DEBUG_MODE = True

def get_modified_request(chosen_genre):
  API_KEY = os.getenv('API_KEY')
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
  sizes = ['w185', 'w300', 'w780', 'w1280', 'original']
  poster_size = sizes[2]
  for movie in movies_results:
    movie['poster'] = secure_base_url + poster_size + movie.get('poster_path')
  return movies_results


def get_genres_dict(API_KEY):
  request = 'https://api.themoviedb.org/3/genre/movie/list?api_key=5b8a2dbae1833b908c30e1f2e192a580&language=en-US'
  request = request.replace('{API_KEY}', API_KEY)
  resp = requests.get(request)
  genres = resp.json()['genres']
  genres_dict = {}
  for i in range(len(genres)):
      genres_dict[genres[i]['name'].lower()] = genres[i]['id']
  return genres_dict
