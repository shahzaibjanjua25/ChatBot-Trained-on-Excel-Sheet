from flask import Flask, request, render_template
import pandas as pd
from fuzzywuzzy import fuzz
import random

app = Flask(__name__)

df = pd.read_csv('movies.csv')
conversation_history = []

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
            response = f"Movies released in {movie_name}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found for the year {movie_name}."
    elif info_type == 'all':
        movie_data = df[df['name'].str.lower() == movie_name.lower()]
        if not movie_data.empty:
            movie_data = movie_data.iloc[0]
            response = f"All data for the movie '{movie_name}':<br>"
            for column, value in movie_data.items():
                response += f"{column}: {value}<br>"
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
    return render_template('index.html', response="")

@app.route('/query', methods=['POST'])
def query():
    user_query = request.form.get('user_query')
    response = ""

    if user_query.lower() == 'quit':
        response = "Goodbye!"
    elif user_query=='hi':
        response="Hi, How can I help you regarding data of the movies?"    
    else:
        if ' and ' in user_query:
            response = combination_queries(user_query)
        else:
            response = respond_to_query(user_query)

    conversation_history.append({'type': 'user', 'text': user_query})
    conversation_history.append({'type': 'chatbot', 'text': response})

    return render_template('index.html', conversation_history=conversation_history)

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    global conversation_history
    conversation_history = []
    return "Chat history cleared."

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
        response = "Here are the genres in the dataset:<br>"
        response += "<br>".join(genres)

    elif 'movies directed by' in query:
        director_name = query.split('movies directed by')[1].strip()
        director_movies = df[df['director'].str.lower().str.contains(director_name, na=False)]
        if not director_movies.empty:
            movie_names = director_movies['name'].tolist()
            response = f"Movies directed by {director_name}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found directed by {director_name}."

    elif 'movies with genre of' in query:
        genre_name = query.split('movies with genre of')[1].strip()
        genre_movies = df[df['genre'].str.lower().str.contains(genre_name, na=False)]
        if not genre_movies.empty:
            movie_names = genre_movies['name'].tolist()
            response = f"Movies with the genre '{genre_name}':<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found with the genre '{genre_name}'."

    elif 'movies with rating of' in query:
        rating = query.split('movies with rating of')[1].strip()
        rating_movies = df[df['rating'].str.lower().str.contains(rating.lower(), na=False)]
        if not rating_movies.empty:
            movie_names = rating_movies['name'].tolist()
            response = f"Movies with a rating of '{rating}':<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found with a rating of '{rating}'."

    elif 'movies released in' in query:
        year = query.split('movies released in')[1].strip()
        released_movies = df[df['released'].str.contains(year, na=False)]
        if not released_movies.empty:
            movie_names = released_movies['name'].tolist()
            response = f"Movies released in {year}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found released in {year}."

    elif 'movies with votes greater than' in query:
        votes_threshold = int(query.split('movies with votes greater than')[1].strip())
        high_votes_movies = df[df['votes'] > votes_threshold]
        if not high_votes_movies.empty:
            movie_names = high_votes_movies['name'].tolist()
            response = f"Movies with votes greater than {votes_threshold}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found with votes greater than {votes_threshold}."

    elif 'movies starring' in query:
        actor_name = query.split('movies starring')[1].strip()
        actor_movies = df[df['star'].str.lower().str.contains(actor_name, na=False)]
        if not actor_movies.empty:
            movie_names = actor_movies['name'].tolist()
            response = f"Movies starring {actor_name}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found starring {actor_name}."

    elif 'movies from country' in query:
        country_name = query.split('movies from country')[1].strip()
        country_movies = df[df['country'].str.lower().str.contains(country_name, na=False)]
        if not country_movies.empty:
            movie_names = country_movies['name'].tolist()
            response = f"Movies from {country_name}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found from {country_name}."

    elif 'movies with budget greater than' in query:
        budget_threshold = int(query.split('movies with budget greater than')[1].strip())
        high_budget_movies = df[df['budget'] > budget_threshold]
        if not high_budget_movies.empty:
            movie_names = high_budget_movies['name'].tolist()
            response = f"Movies with a budget greater than {budget_threshold}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found with a budget greater than {budget_threshold}."

    elif 'movies with gross greater than' in query:
        gross_threshold = int(query.split('movies with gross greater than')[1].strip())
        high_gross_movies = df[df['gross'] > gross_threshold]
        if not high_gross_movies.empty:
            movie_names = high_gross_movies['name'].tolist()
            response = f"Movies with gross greater than {gross_threshold}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found with gross greater than {gross_threshold}."

    elif 'movies with score greater than' in query:
        score_threshold = float(query.split('movies with score greater than')[1].strip())
        high_score_movies = df[df['score'] > score_threshold]
        if not high_score_movies.empty:
            movie_names = high_score_movies['name'].tolist()
            response = f"Movies with score greater than {score_threshold}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found with score greater than {score_threshold}."  

    elif 'movies produced by' in query:
        company_name = query.split('movies produced by')[1].strip()
        company_movies = df[df['company'].str.lower().str.contains(company_name, na=False)]
        if not company_movies.empty:
            movie_names = company_movies['name'].tolist()
            response = f"Movies produced by {company_name}:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found produced by {company_name}."

    elif 'movies with runtime greater than' in query:
        runtime_threshold = int(query.split('movies with runtime greater than')[1].strip())
        long_runtime_movies = df[df['runtime'] > runtime_threshold]
        if not long_runtime_movies.empty:
            movie_names = long_runtime_movies['name'].tolist()
            response = f"Movies with a runtime greater than {runtime_threshold} minutes:<br>"
            response += "<br>".join(movie_names)
        else:
            response = f"No movies found with a runtime greater than {runtime_threshold} minutes."
    elif 'movies with score of' in query:
        try:
            score = float(query.split('movies with score of')[1].strip())
            score_movies = df[df['score'] == score]
            if not score_movies.empty:
                movie_names = score_movies['name'].tolist()
                response = f"Movies with a score of {score}:<br>"
                response += "<br>".join(movie_names)
            else:
                response = f"No movies found with a score of {score}."
        except ValueError:
            response = "Invalid input. Please provide a valid score."

    elif 'movies with votes of' in query:
        try:
            votes = int(query.split('movies with votes of')[1].strip())
            votes_movies = df[df['votes'] == votes]
            if not votes_movies.empty:
                movie_names = votes_movies['name'].tolist()
                response = f"Movies with {votes} votes:<br>"
                response += "<br>".join(movie_names)
            else:
                response = f"No movies found with {votes} votes."
        except ValueError:
            response = "Invalid input. Please provide a valid number of votes."

    elif 'movies with budget of' in query:
        try:
            budget = int(query.split('movies with budget of')[1].strip())
            budget_movies = df[df['budget'] == budget]
            if not budget_movies.empty:
                movie_names = budget_movies['name'].tolist()
                response = f"Movies with a budget of {budget}:<br>"
                response += "<br>".join(movie_names)
            else:
                response = f"No movies found with a budget of {budget}."
        except ValueError:
            response = "Invalid input. Please provide a valid budget."

    elif 'movies with gross of' in query:
        try:
            gross = int(query.split('movies with gross of')[1].strip())
            gross_movies = df[df['gross'] == gross]
            if not gross_movies.empty:
                movie_names = gross_movies['name'].tolist()
                response = f"Movies with a gross of {gross}:<br>"
                response += "<br>".join(movie_names)
            else:
                response = f"No movies found with a gross of {gross}."
        except ValueError:
            response = "Invalid input. Please provide a valid gross."

    elif 'movies with runtime of' in query:
        try:
            runtime = int(query.split('movies with runtime of')[1].strip())
            runtime_movies = df[df['runtime'] == runtime]
            if not runtime_movies.empty:
                movie_names = runtime_movies['name'].tolist()
                response = f"Movies with a runtime of {runtime} minutes:<br>"
                response += "<br>".join(movie_names)
            else:
                response = f"No movies found with a runtime of {runtime} minutes."
        except ValueError:
            response = "Invalid input. Please provide a valid runtime."        
    
    else:
        response = search_movie_info(query)

    return response

def combination_queries(query):
    queries = query.split(' and ')  

    filtered_df = df.copy()  

    for condition in queries:
        condition = condition.strip()  
        for column in df.columns:
            if f'movies with {column} of' in condition:
                value = condition.split(f'movies with {column} of')[1].strip()
                filtered_df = filtered_df[filtered_df[column].astype(str).str.lower() == value.lower()]

    if not filtered_df.empty:
        movie_names = filtered_df['name'].tolist()
        response = "Movies matching your criteria:<br>"
        response += "<br>".join(movie_names)
    else:
        response = "No movies found matching your criteria."

    return response

if __name__ == '__main__':
    conversation_history = []
    app.run(debug=True)
