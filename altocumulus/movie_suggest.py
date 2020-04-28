from flask import Blueprint
import requests

movie_suggest = Blueprint('movie_suggest', __name__)


@movie_suggest.route('/api/movie')
def suggest_movie(movie):
    baseurl = "https://tastedive.com/api/similar"
    params_diction = {"q": movie, "type": 'movies', "limit": 5}
    resp = requests.get(baseurl, params=params_diction)
    word_ds = resp.json()
    return word_ds


def extract_movie_titles(titles):
    makelist = []
    for k, v in titles.items():
        for x in v['Results']:
            makelist.append(x['Name'])
        return makelist


print(extract_movie_titles(suggest_movie("A movie")))
