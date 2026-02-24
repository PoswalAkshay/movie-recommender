#c411344f7be153eec44c865e976568d1
from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

API_KEY = "c411344f7be153eec44c865e976568d1"

# load dataset
movies = pd.read_csv("tmdb_5000_movies.csv")

# ---------- TMDB helpers ----------
def get_movie_data(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": API_KEY, "query": title}
    data = requests.get(url, params=params).json()

    try:
        result = data['results'][0]
        poster = "https://image.tmdb.org/t/p/w500" + result['poster_path']
        rating = result['vote_average']
        year = result['release_date'][:4]
        return poster, rating, year
    except:
        return "https://via.placeholder.com/500x750?text=No+Image", "N/A", "N/A"

# ---------- Trending Movies ----------
def get_trending_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": API_KEY}
    data = requests.get(url, params=params).json()

    names, posters, ratings, years = [], [], [], []

    for movie in data['results'][:10]:
        names.append(movie['title'])
        posters.append("https://image.tmdb.org/t/p/w500" + movie['poster_path'])
        ratings.append(movie['vote_average'])
        years.append(movie['release_date'][:4])

    return names, posters, ratings, years

# ---------- Recommendation (Genre based) ----------
def recommend(movie):
    movie = movie.lower()
    movies['title_lower'] = movies['title'].str.lower()

    matches = movies[movies['title_lower'].str.contains(movie)]

    # अगर movie मिल गई
    if not matches.empty:
        genre = matches.iloc[0]['genres']
        similar_movies = movies[movies['genres'] == genre].head(6)

        names, posters, ratings, years = [], [], [], []

        for title in similar_movies['title'][1:6]:
            poster, rating, year = get_movie_data(title)
            names.append(title)
            posters.append(poster)
            ratings.append(rating)
            years.append(year)

        # अगर similar मिल गए → return
        if len(names) >= 5:
            return names, posters, ratings, years

    # ⭐ FALLBACK → Top popular movies (ALWAYS WORKS)
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": API_KEY}
    data = requests.get(url, params=params).json()

    names, posters, ratings, years = [], [], [], []

    for movie in data['results'][:5]:
        names.append(movie['title'])
        posters.append("https://image.tmdb.org/t/p/w500" + movie['poster_path'])
        ratings.append(movie['vote_average'])
        years.append(movie['release_date'][:4])

    return names, posters, ratings, years
# ---------- Suggestions ----------
@app.route('/suggest')
def suggest():
    query = request.args.get('q')
    if not query:
        return jsonify([])
    result = movies[movies['title'].str.contains(query, case=False)]
    return jsonify(result['title'].head(5).tolist())

# ---------- Home ----------
@app.route('/', methods=['GET','POST'])
def index():
    t_names, t_posters, t_ratings, t_years = get_trending_movies()

    if request.method == 'POST':
        movie = request.form['movie']
        names, posters, ratings, years = recommend(movie)

        if len(names) == 0:
            return render_template("index.html",
                                   error="Movie not found",
                                   t_names=t_names,
                                   t_posters=t_posters,
                                   t_ratings=t_ratings,
                                   t_years=t_years)

        return render_template("index.html",
                               names=names,
                               posters=posters,
                               ratings=ratings,
                               years=years,
                               t_names=t_names,
                               t_posters=t_posters,
                               t_ratings=t_ratings,
                               t_years=t_years)

    return render_template("index.html",
                           t_names=t_names,
                           t_posters=t_posters,
                           t_ratings=t_ratings,
                           t_years=t_years)

app.run(debug=True)