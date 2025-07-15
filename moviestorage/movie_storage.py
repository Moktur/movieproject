import json


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database
    """
    with open('data.json', 'r') as m:
        dict_of_movies = json.load(m)
    return dict_of_movies


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    json_str = json.dumps(movies)
    with open("data.json", "w") as fileobj:
        fileobj.write(json_str)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    with open("data.json", "r") as fileobj:
        database = json.load(fileobj)
        movie = {title: {
                    "name": title,
                    "rating": rating,
                    "release": year
                }
            }
        database.update(movie)
    with open("data.json", "w") as fileobj:
        json.dump(database, fileobj, indent=4)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    database = is_in_database(title)
    if database is not False:
        del database[title]
        with open("data.json", "w") as fileobj:
            json.dump(database, fileobj, indent=4)
            print(f"The movie {title} was deleted")


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    database = is_in_database(title)
    if database is not False:
        database[title]["rating"] = rating
        with open("data.json", "w") as fileobj:
            json.dump(database, fileobj, indent=4)
            print(
                f"The movie {title} was updated with "
                f"a new rating ({rating})")
    else:
        print(f"Movie {title} not found")


def is_in_database(title):
    was_in_database = False
    database = ""
    with open("data.json", "r") as fileobj:
        database = json.load(fileobj)
        for movie in database:
            if title in movie:
                was_in_database = True
                return database
    if not was_in_database:
        print("Movie not found in database")
        return was_in_database
