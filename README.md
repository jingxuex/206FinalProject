# 206FinalProject
### Project Title: SI206 Final Project <br />
### Environment setup:
In order to run this program, you need to set up a virtual environment with
python3 installed. The following is the step by step instruction:
(1) get the path on the local machine with
```
  which python3
```
(2) install virtual environment on your machine
```
  virtualenv -p <python3_path> my_project
```
(3) start the virtual environment
```
  source my_project/bin/activate
```


### Project Overview:
For this final project, I would like to write a program that let users choose specific movie and see the rating, rank, genre, and other information of that movie from OMDb and provide an interactive command line prompt for the user to choose visualization options by using the plotly, and try to make it interactive and engaging by providing different data visualization options such as bar charts, pie charts etc. <br />
### Data Sources:
(1) the Open Movie Database which uses the web API and requires API key -- http://www.omdbapi.com/ <br />
(2) scrape a single new page from -- https://www.imdb.com/list/ls051781075/?sort=list_order,asc&st_dt=&mode=simple&page=1&ref_=ttls_vw_smp%20to%20get%20the%20top200%20movies%20of%20all%20the%20time <br />
(3) scrape the recent tweets and comments about the recent movies.https://twitter.com/   <br />

### Presentation options and how to run the program:
(1) Bar charts of different movie types <br />
(2) Table of movie and rating with criteria - rating greater than the criteria <br />
(3) Table of movie and year with criteria - year equals to that criteria year <br />
(4) Pie Chart to show the percentage of different movie types <br />
(5) Scatterplot to show the relation between rating and runtime <br />
(6) Get the related tweets about the movie <br />

### Code Structure:
The main SI206_omdb.py program consists one class Movie and seven functions which are bar_chart_movie_genre(), tableRating(criteria), tableYear(criteria), pie_chart(),
scatterplot(), tweet(criteria) to implement my representation tools.

### User Guide:
At the beginning, it will give the user the prompt: <br />
Enter a command from (barchart, tableRating(), tableYear(), piechart, scatterplot, tweet(criteria)):  <br />
Option enter:
```
  barchart
```
Option enter(in the parentheses enter a number movie-rating between 1 and 10):
```
  tableRating() for example tableRating(7.8)
```
Option enter(in the parentheses enter a year):
```
  tableYear() for example tableYear(1993)
```
Option enter:
```
  piechart
```

Option enter:
```
  scatterplot
```

Option enter (in the parentheses enter a rank number between 1 and 200)
```
  tweet() for example tweet(4)
```
