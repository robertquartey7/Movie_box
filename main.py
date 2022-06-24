from flask import Flask, render_template, url_for, request
import requests

app = Flask(__name__)





# all the movie api
query = ''
api_key = '0b79c5fbd226409b5cbbe233195ab7f9'
api_upcoming_movie = f'https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-US&page=1'
api_todays_hot_movie = f'https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}'
api_todays_hot_shows = f'https://api.themoviedb.org/3/trending/tv/day?api_key={api_key}'
api_search = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}'
api_week_hot_movie = f'https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}'
api_week_hot_shows = f'https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}'
api_top_rating_movies = 'https://api.themoviedb.org/3/movie/popular?api_key=0b79c5fbd226409b5cbbe233195ab7f9&language=en-US&page=1'
api_top_rating_tvshows = 'https://api.themoviedb.org/3/tv/popular?api_key=0b79c5fbd226409b5cbbe233195ab7f9&language=en-US&page=1'


# the home page route
@app.route('/home')
@app.route('/')
def home():
    upcoming_data = requests.get(api_upcoming_movie)
    todays_HM_data = requests.get(api_todays_hot_movie)
    todays_WT_data = requests.get(api_todays_hot_shows)
    week_HM_data = requests.get(api_week_hot_movie)
    week_HT_data = requests.get(api_week_hot_shows)
    search_data = requests.get(api_search)

    if(upcoming_data.status_code == 200):
        UC_results = upcoming_data.json()
        THM_results = todays_HM_data.json()
        THT_results = todays_WT_data.json()
        WHM_results = week_HM_data.json()
        WHT_results = week_HT_data.json()
       
    else:
        print('failed')

    context = {
        'UC_movies': UC_results['results'],
        'THM_movies': THM_results['results'],
        'THT_shows': THT_results['results'],  # new
        'WHT_shows': WHT_results['results'],
        'WHM_movies': WHM_results['results'],  # new


    }
    return render_template('movie/home.html', context=context)



@app.route('/movies')
def movies():
    
    
    top_rating_data = requests.get(api_top_rating_movies)
    results = top_rating_data.json()
    context = {
        'top_rating':results['results'],
    }
    return render_template('movie/movies.html', context=context)



@app.route('/tvshows')
def tvshows():
    top_rating_data = requests.get(api_top_rating_tvshows)
    results = top_rating_data.json()
    context = {
        'top_rating':results['results'],
    }
    return render_template('movie/tv_shows.html', context=context)



# def movielist():
#     return render_template('movie/movielist.html')
# rendering the details page with the information passed through the url



@app.route('/details/<int:id>/<string:type>')
def details(id, type):
    
    api_get_movie = f'https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&append_to_response=videos'
    api_get_tv = f'https://api.themoviedb.org/3/tv/{id}?api_key={api_key}&append_to_response=videos'
    
    
    #requesting data from the api
    details_movie = requests.get(api_get_movie)
    details_tv = requests.get(api_get_tv)
    
    
    # checking the type of show and if the request went through
    if (type == 'movie' and details_movie.status_code == 200):
        return render_template('movie/details.html' , context =details_movie.json() )
    elif(type== 'tv' and details_tv.status_code == 200):
         return render_template('movie/details.html' , context =details_tv.json() )
    else:
       pass



@app.route('/search', methods=['POST'])
def search():
    
    if request.method == "POST":
        movie_search_name = request.form['searchMovie']
        
        search_api = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_search_name}'
        search_result = requests.get(search_api)
        
        print(search_api)
        return render_template('movie/search.html', context=search_result.json())
    
    else:
        return '<h1>404 file not found</h1>'



# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)