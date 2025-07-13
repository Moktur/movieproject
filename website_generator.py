import movie_storage_sql as storage

TITLE = "My Movie App"

def write_html():
    """Writes the final HTML file"""
    try:
        with open("./static/index_template.html", "r", encoding="utf-8") as obj:
            template = obj.read()

        html_content = template.replace("__TEMPLATE_TITLE__", TITLE)
        html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_data_to_html())

        with open("./static/my_movie_app.html", "w", encoding="utf-8") as obj:
            obj.write(html_content)
        print(f"Website successfully created")
    except Exception as e:
        print(f"{e} \n Couldn't create html file")

def movie_data_to_html():
    movies = storage.list_movies()
    movie_info = ""
    for title, moviedetails in movies.items():
        movie_info += serialize_movies(title, moviedetails)
    return movie_info


def serialize_movies(title, moviedetails):
    """Creates HTML for each movie"""
    return (
      '<li>'
      f'<div class="movie">'
      f'<img class="movie-poster" src="{moviedetails["url"]}">'
      f'<div class="movie-title">{title}</div>'
      f'<div class="movie-year">{moviedetails["year"]}</div>'
      f'</div>'
      f'</li>'
    )