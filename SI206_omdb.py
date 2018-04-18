from secrets import *
from bs4 import BeautifulSoup
import requests
import json
import sqlite3
from requests_oauthlib import OAuth1
import plotly.plotly as py
import plotly.graph_objs as go
from collections import Counter
from collections import defaultdict


#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
#Code for OAuth ends

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

## First Version of Cache only one parameters
def get_unique_key(url):
  return url

def make_request_using_cache(url):
    global header
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        #print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

## Second Version of Cache two parameters
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache_second_version(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        #print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

## Third Version of Cache two parameters with OAuth1
def make_request_using_cache_third_version(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        #print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params, auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


# Scrape a new page from top 200 movies
topmovie_url = 'http://www.imdb.com/list/ls051781075/?sort=list_order,asc&st_dt=&mode=simple&page=1&ref_=ttls_vw_smp'
topmovie_html = make_request_using_cache(topmovie_url)
topmovie_soup = BeautifulSoup(topmovie_html,'html.parser')
topmovie_name = topmovie_soup.find_all(class_='lister-item-header')
topmovie_rate = topmovie_soup.find_all(class_='col-imdb-rating')

url2 = 'http://www.imdb.com/list/ls051781075/?st_dt=&mode=simple&page=2&ref_=ttls_vw_smp&sort=list_order,asc'
html2 = make_request_using_cache(url2)
soup2 = BeautifulSoup(html2,'html.parser')
name2 = soup2.find_all(class_='lister-item-header')
rate2 = soup2.find_all(class_='col-imdb-rating')

mylist_rank = []
mylist_title = []
mylist_year = []
mylist_rating = []

for item in topmovie_rate:
    myrating = item.find('strong').text.strip()
    mylist_rating.append(myrating)

for item in topmovie_name:
    topmovie_rank = item.find(class_='lister-item-index unbold text-primary').text
    topmovie_title = item.find('a').text
    topmovie_year = item.find(class_='lister-item-year text-muted unbold').text
    mylist_title.append(topmovie_title)
    mylist_year.append(topmovie_year)
    mylist_rank.append(topmovie_rank)

for item in rate2:
    myrating = item.find('strong').text.strip()
    mylist_rating.append(myrating)

for item in name2:
    topmovie_rank = item.find(class_='lister-item-index unbold text-primary').text
    topmovie_title = item.find('a').text
    topmovie_year = item.find(class_='lister-item-year text-muted unbold').text
    mylist_title.append(topmovie_title)
    mylist_year.append(topmovie_year)
    mylist_rank.append(topmovie_rank)


# API to get data from Open Movie Database
def get_movies(name):
    baseurl = 'http://www.omdbapi.com/'
    params = {'apikey': OMDb_key, 'type':'movie','r':'json', 't':name}
    #response = requests.get(baseurl, params).json()
    response = make_request_using_cache_second_version(baseurl, params)
    return response

data_list = []
for i in range(len(mylist_title)):
    movie_list_json = get_movies(mylist_title[i])
    data_list.append(movie_list_json)
with open('movie.json', 'w') as outfile:
    json.dump(data_list, outfile, sort_keys=True,indent=4)


# Twitter Api to get the related tweets about the movie
def get_tweets_for_movie(movie_title):
    baseurl_twitter = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {'q':movie_title, 'count':1}
    d = make_request_using_cache_third_version(baseurl_twitter, params)
    return d['statuses'][0]['text']

title_no_space = []
for item in mylist_title:
    item = item.replace(" ","")
    title_no_space.append(item)




# Read data into a new database called movie.db
DBNAME = 'movie.db'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

# Drop table if already exit
statement = '''
    DROP TABLE IF EXISTS 'Top200';
'''
cur.execute(statement)
conn.commit()

statement = '''
    DROP TABLE IF EXISTS 'MovieInfo';
'''
cur.execute(statement)
conn.commit()

# Create the table Top100, MovieInfo in the database
statement = '''
    CREATE TABLE 'Top200' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Title' TEXT NOT NULL,
        'Rank' INTEGER NOT NULL,
        'Year' TEXT NOT NULL
    );
'''
cur.execute(statement)
conn.commit()

statement = '''
    CREATE TABLE 'MovieInfo' (
        'MovieId' INTEGER,
        'Name' TEXT,
        'Country' TEXT,
        'Director' TEXT,
        'Genre' TEXT,
        'Language' TEXT,
        'Metascore' REAL,
        'Rated' TEXT,
        'imdbRating' REAL,
        'imdbID' TEXT,
        'imdbVotes' REAL,
        'Runtime' REAL

    );
'''
cur.execute(statement)
conn.commit()

# Insert the data into the database
for i in range(len(mylist_title)):
    insertion = (None,mylist_title[i],int(mylist_rank[i].split('.')[0]),
    mylist_year[i].replace('(', '').replace(')', ''))
    statement = '''
        INSERT INTO 'TOP200' VALUES (?,?,?,?)
    '''
    cur.execute(statement,insertion)
    conn.commit()


movieInf = json.load(open('movie.json'))

for i in range(len(movieInf)):
    insertion = (None, movieInf[i]['Title'], movieInf[i]['Country'],
    movieInf[i]['Director'], movieInf[i]['Genre'], movieInf[i]['Language'],
    int(movieInf[i]['Metascore']) if movieInf[i]['Metascore'] != 'N/A' else 0,
    movieInf[i]['Rated'],
    float(movieInf[i]['imdbRating']), movieInf[i]['imdbID'],
    int(movieInf[i]['imdbVotes'].replace(',','')),
    int(movieInf[i]['Runtime'].split(" ")[0]))
    statement = '''
        INSERT INTO 'MovieInfo' VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    cur.execute(statement,insertion)
    conn.commit()


#Update the foreign key into the table MovieInfo
statement = '''
    UPDATE MovieInfo SET MovieId =
    (SELECT Id FROM Top200 WHERE Top200.Title=MovieInfo.Name)
'''
cur.execute(statement)
conn.commit()
conn.close()

# bar charts of movie types
def bar_chart_movie_genre():
    type_list = []
    distinct_type_list = []
    frequency_list = []

    DBNAME = 'movie.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Genre FROM MovieInfo
    '''
    cur.execute(statement)

    for item in cur:
        for i in range(len(item)):
            itemlist = item[i].split(',')
            for j in itemlist:
                type_list.append(j)

    res = Counter(type_list)
    mydict = dict(res)
    distinct_type_list = list(mydict.keys())
    frequency_list = list(mydict.values())


    trace0 = go.Bar(
        x= distinct_type_list,
        y= frequency_list,
    )

    data = [trace0]
    layout = go.Layout(
        title='Bar chart of Movie Genre',
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='color-bar')
    conn.close()

# Side by side boxplot of rating of every movie type
def boxplot_ratings():
    type_list = []
    composite_list = []
    ratings_composite = []
    genre = []
    ratings = []

    DBNAME = 'movie.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        SELECT AVG(imdbRating), Genre from MovieInfo
        GROUP BY Genre
    '''
    cur.execute(statement)
    for item in cur:
        type_list = item[1].split(',')
        for i in range(len(type_list)):
            composite_list = [item[0],type_list[i]]
            ratings_composite.append(composite_list)

    for i in range(len(ratings_composite)):
        ratings.append(ratings_composite[i][0])
        genre.append(ratings_composite[i][1])

    temp = defaultdict(set)

    # Aggregate movie ratings by movie types
    for gen, rat in zip(genre, ratings):
        temp[gen].add(rat)

    temp = dict(temp)
    x_list = list(temp.keys())
    y_data = list(temp.values())
    y_list = []
    for i in range(len(y_data)):
        y_list.append(list(y_data[i]))


    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)',
    'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)',
    'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)',
    'rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)',
    'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)',
    'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)',
    'rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)',
    'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)',
    'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)',
    'rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)',
    'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)',
    'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)',
    'rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)',
    'rgba(44, 160, 101, 0.5)']

    traces = []

    for xd, yd, cls in zip(x_list, y_list, colors):
            traces.append(go.Box(
                y=yd,
                name=xd,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker=dict(
                    size=2,
                ),
                line=dict(width=1),
            ))

    layout = go.Layout(
        title='Side By Side Boxplot of Different Types of Average Movie Ratings',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )

    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig)
    conn.close()

def table_rating(criteria):
    name_list = []
    year_list = []
    rating_list = []
    criteria = float(criteria)
    DBNAME = 'movie.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        SELECT MovieInfo.Name, Top200.Year, MovieInfo.imdbRating FROM MovieInfo
        JOIN Top200 ON MovieInfo.MovieId=Top200.Id WHERE imdbRating > {}
    '''.format(criteria)

    cur.execute(statement)
    for item in cur:
        name_list.append(item[0])
        year_list.append(item[1])
        rating_list.append(item[2])


    trace = go.Table(
        header=dict(values=['Movie Name', 'Year', 'Rating'],
                    line = dict(color='#7D7F80'),
                    fill = dict(color='#a1c3d1'),
                    align = ['left'] * 5),
        cells=dict(values=[name_list, year_list, rating_list],
                    line = dict(color='#7D7F80'),
                    fill = dict(color='#EDFAFF'),
                    align = ['left'] * 5)
    )

    data = [trace]
    namestring = 'Movie Information table with rating great than ' + str(criteria)
    py.plot(data, filename = namestring)
    conn.close()

def table_year(criteria):
    name_list = []
    year_list = []
    rating_list = []

    DBNAME = 'movie.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        SELECT MovieInfo.Name, Top200.Year, MovieInfo.imdbRating FROM MovieInfo
        JOIN Top200 ON MovieInfo.MovieId=Top200.Id WHERE Year = '{}'
    '''.format(criteria)
    cur.execute(statement)
    for item in cur:
        name_list.append(item[0])
        year_list.append(item[1])
        rating_list.append(item[2])

    trace = go.Table(
        header=dict(values=['Movie Name', 'Year', 'Rating'],
                    line = dict(color='#7D7F80'),
                    fill = dict(color='#a1c3d1'),
                    align = ['left'] * 5),
        cells=dict(values=[name_list, year_list, rating_list],
                    line = dict(color='#7D7F80'),
                    fill = dict(color='#EDFAFF'),
                    align = ['left'] * 5)
    )

    data = [trace]
    namestring = 'Movie Information table with year in ' + criteria
    py.plot(data, filename = namestring)
    conn.close()

def pie_chart():
    type_list = []
    DBNAME = 'movie.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        SELECT MovieInfo.Genre FROM MovieInfo
    '''
    cur.execute(statement)

    for item in cur:
        for i in range(len(item)):
            itemlist = item[i].split(',')
            for j in itemlist:
                type_list.append(j)

    res = Counter(type_list)
    mydict = dict(res)
    distinct_type_list = list(mydict.keys())
    frequency_list = list(mydict.values())

    labels = distinct_type_list
    values = frequency_list

    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], filename='basic_pie_chart')
    conn.close()

def scatterplot():
    DBNAME = 'movie.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    rating_list = []
    runtime_list = []

    statement = '''
        SELECT imdbRating, Runtime, Year FROM MovieInfo
        JOIN TOP200 ON MovieInfo.MovieId=Top200.Id
    '''
    cur.execute(statement)
    for item in cur:
        rating_list.append(item[0])
        runtime_list.append(item[1])

    trace = go.Scatter(
        x = rating_list,
        y = runtime_list,
        mode = 'markers'
    )

    data = [trace]
    py.plot(data, filename='scatter plot between rating and runtime')

def interactive_prompt():
    response = ''
    while response != 'exit':
        response = input('Enter a command from (barchart, boxplot, tableRating(), tableYear(), piechart, scatterplot): ')

        if response == 'barchart':
            bar_chart_movie_genre()
        elif response == 'boxplot':
            boxplot_ratings()
        elif response[:11] == 'tableRating':
            rating = response.split('(', 1)[1].split(')')[0]
            table_rating(rating)
        elif response[:9] == 'tableYear':
            year = response.split('(', 1)[1].split(')')[0]
            table_year(year)
        elif response == 'piechart':
            pie_chart()
        elif response == 'scatterplot':
            scatterplot()
        else:
            print('Please enter a valid input.')
            continue
    print('Bye')

if __name__=="__main__":
    interactive_prompt()
