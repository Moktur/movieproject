import data_fetcher

def format_data(movie_information):
  data_for_use = {
    "title": movie_information["Title"],
    "year" : movie_information["Year"],
    "rating": movie_information["imdbRating"],
    "url": movie_information["Poster"]
  }
  return data_for_use

