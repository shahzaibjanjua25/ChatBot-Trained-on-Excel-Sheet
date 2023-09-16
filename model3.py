from flask import Flask, request, render_template
import pandas as pd
from fuzzywuzzy import fuzz
import random

app = Flask(__name__)


df = pd.read_csv('movies.csv')

def extract_info_type_and_movie(query):
    info_types = ['rating', 'genre', 'year', 'released', 'score', 'votes',
                  'director', 'writer', 'star', 'country', 'budget',
                  'gross', 'company', 'runtime']

    for info_type in info_types:
        if f'{info_type} of' in query:
            movie_name = query.split(f'{info_type} of')[1].strip()
            return info_type, movie_name

    if 'list all movies in' in query:
        year = query.split('list all movies in')[1].strip()
        return 'list_year', year

    if 'all data for the movie' in query:
        movie_name = query.split('all data for the movie')[1].strip()
        return 'all', movie_name

    return None, None

def search_movie_info(query):
    query = query.lower()
    info_type, movie_name = extract_info_type_and_movie(query)

    if info_type is None or movie_name is None:
        return "I'm sorry, I couldn't understand your query."

    if info_type == 'list_year':
        year_movies = df[df['year'] == int(movie_name)]

        if not year_movies.empty:
            movie_names = year_movies['name'].tolist()
            response = f"Movies released in {movie_name}:  "
            response += " , ".join(movie_names)
        else:
            response = f"No movies found for the year {movie_name}."
    elif info_type == 'all':
        movie_data = df[df['name'].str.lower() == movie_name.lower()]
        if not movie_data.empty:
            movie_data = movie_data.iloc[0]
            response = f"All data for the movie '{movie_name}': , "
            for column, value in movie_data.items():
                response += f"{column}: {value} , "
        else:
            response = f"No information found for the movie '{movie_name}'."
    else:
        best_match = None
        best_score = -1

        for index, row in df.iterrows():
            title = str(row['name']).lower()
            score = fuzz.ratio(movie_name, title)

            if score > best_score:
                best_score = score
                best_match = row

        if best_score >= 80:
            info_value = best_match[info_type]
            response = f"The {info_type} of '{best_match['name']}' is {info_value}."
        else:
            response = f"Sorry, '{movie_name}' not found in the database."

    return response

@app.route('/')
def index():

    return render_template('templates/index.html')


@app.route('/query', methods=['POST'])
def query():
    user_query = request.form.get('user_query')
    response = ""

    if user_query.lower() == 'quit':
        response = "Goodbye!"
    else:
        response = respond_to_query(user_query)

    return render_template('templates/index.html', response=response)

def respond_to_query(query):
    query = query.lower()

    if 'top rated movie' in query:
        top_rated_movie = df[df['score'] == df['score'].max()]
        response = f"The top-rated movie is '{top_rated_movie.iloc[0]['name']}' with a score of {top_rated_movie.iloc[0]['score']}."

    elif 'random movie' in query:
        random_movie = random.choice(df['name'])
        response = f"Here's a random movie: '{random_movie}'."

    elif 'list genres' in query:
        genres = df['genre'].dropna().unique()
        response = "Here are the genres in the dataset: , "
        response += " , ".join(genres)

    elif 'movies directed by' in query:
        director_name = query.split('movies directed by')[1].strip()
        director_movies = df[df['director'].str.lower().str.contains(director_name, na=False)]
        if not director_movies.empty:
            movie_names = director_movies['name'].tolist()
            response = f"Movies directed by {director_name}: , "
            response += " , ".join(movie_names)
        else:
            response = f"No movies found directed by {director_name}."

    elif 'movies with genre of' in query:
        genre_name = query.split('movies with genre of')[1].strip()
        genre_movies = df[df['genre'].str.lower().str.contains(genre_name, na=False)]
        if not genre_movies.empty:
            movie_names = genre_movies['name'].tolist()
            response = f"Movies with the genre '{genre_name}': , "
            response += " , ".join(movie_names)
        else:
            response = f"No movies found with the genre '{genre_name}'."

    elif 'movies with rating of' in query:
        rating = query.split('movies with rating of')[1].strip()
        rating_movies = df[df['rating'].str.lower().str.contains(rating.lower(), na=False)]
        if not rating_movies.empty:
            movie_names = rating_movies['name'].tolist()
            response = f"Movies with a rating of '{rating}': , "
            response += " , ".join(movie_names)
        else:
            response = f"No movies found with a rating of '{rating}'."

    else:
        response = search_movie_info(query)

    return response

if __name__ == '__main__':
    app.run(debug=True)
