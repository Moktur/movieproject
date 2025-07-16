from moviestorage import movie_storage_sql as storage
import os
import webbrowser


TITLE = "My Movie App"
MOVIES_PER_ROW = 5
output_path = os.path.join("static", "index.html")
template_path = os.path.join("static", "index_template.html")


def write_html():
    """Writes the final HTML file"""
    try:
        with open(template_path, "r", encoding="utf-8") as obj:
            template = obj.read()

        html_content = template.replace("__TEMPLATE_TITLE__", TITLE)
        html_content = html_content.replace(
            "__TEMPLATE_MOVIE_GRID__",
            movie_data_to_html()
        )

        with open(output_path, "w", encoding="utf-8") as obj:
            obj.write(html_content)
        print("Website successfully created")

        try:
            webbrowser.open(f"file://{os.path.abspath(output_path)}")
            print("Opening in browser...")
        except Exception as e:
            print(f"{e}, couldn't open Website")
    except Exception as e:
        print(f"{e}\nCouldn't create html file")


def movie_data_to_html():
    movies = storage.list_movies()
    movie_info = ""
    current_row = []

    for i, (title, moviedetails) in enumerate(movies.items(), 1):
        current_row.append(serialize_movies(title, moviedetails))

        # start new row, if MOVIES_PER_ROW is reached
        if i % MOVIES_PER_ROW == 0 or i == len(movies):
            movie_info += (
                '<div class="movie-row">' + ''.join(current_row) + '</div>'
            )
            current_row = []

    return movie_info


def serialize_movies(title, moviedetails):
    """Creates HTML for each movie with fixed height containers"""
    return (
      '<div class="movie-container">'
      f'<img class="movie-poster" src='
      f'{moviedetails["url"]}" alt="{title}" loading="lazy">'
      '<div class="movie-info">'
      f'<div class="movie-title" title="{title}">{title}</div>'
      f'<div class="movie-year">{moviedetails["year"]}</div>'
      '</div>'
      '</div>'
    )
