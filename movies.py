import statistics
import random
from data import data_fetcher
from data import data_formatter
from website_generator import write_html
from moviestorage import movie_storage_sql as storage


def print_menu(menu_choices):
    """Printing the menu
    no return value
    """
    for i in range(len(menu_choices)):
        print(f"{i}. {menu_choices[i]}")
    print("Enter choice (0-9): ")


def list_all_movies():
    """
    Printing the list of all movies
    """
    all_movies = storage.list_movies()
    if all_movies:
        for title, data in all_movies.items():
            print(f"Title: {title}")
            print(f"Rating: {data['rating']}")
            print(f"Releaseyear: {data['year']}")
            print("- - - - - - - - - - - - - - -")
    else:
        print("Moviedatenbank empty")


def add_movie():
    """Adding a Movie to the Database"""
    list_of_movies = list(storage.list_movies())
    in_database = False
    validation = False
    moviename = ""
    while not validation:
        moviename = input("Add a movie name and press Enter ")
        if moviename == "" or moviename.isspace():
            print("Please enter a valid name for the movie")
        else:
            validation = True
    for movie in list_of_movies:
        if moviename in movie:
            print("Movie already in Database")
            in_database = True
    if not in_database:
        validation = False
        while not validation:
            # If Movie can't be found and data_fetchers receives None
            try:
                movie_information = data_formatter.format_data(
                                        data_fetcher.fetch_data(moviename))
            except Exception:
                print("Please write a different Moviename")
                break
            if movie_information["rating"] == "N/A":
                movie_information["rating"] = 5.0
                print(f"Movie {moviename} has no rating from omdb. \n"
                      "Default rating is 5.0.\n"
                      "If you want to change the rating, choose "
                      "<update> from the menu")
            storage.add_movie(
                movie_information["title"],
                movie_information["year"],
                movie_information["rating"],
                movie_information["url"]
            )
            print(
                f'Movie {moviename} with a '
                f'{movie_information["rating"]} rating released '
                f'{movie_information["year"]} was added to the database')
            validation = True 
            

def delete_movie():
    """Deletes a movie from the database"""
    try:
        name_of_movie_to_delete = input(
            "Enter the name of the movie you wish to delete: ")
        storage.delete_movie(name_of_movie_to_delete)
    except Exception:
        print(
            f"Couldn't find {name_of_movie_to_delete}. "
            f"Did you wrote the correct name?")


def update_movie():
    """Update a movie in the database"""
    movie_to_update = input("Enter a movie name: ")
    validation = False
    while not (validation):
        try:
            new_rating = input("Enter a new rating: ")
            if len(new_rating) == 1 and \
                new_rating.isdigit():
                storage.update_movie(movie_to_update, float(new_rating))
                validation = True
                break
            if len(new_rating) == 3 and new_rating[1] == ".":
                storage.update_movie(movie_to_update, float(new_rating))
                validation = True
                break
            raise ValueError("Rating must be X or X.X (e.g., 7 or 4.9)")
        except ValueError:
            print("The rating must be written in the format" \
            " X.X or X (e.g., 4 or 3.2)")
            print("Please try again")


def stats():
    """Printing the average, median, best and worst movies"""
    list_of_movies = create_list_of_movies(storage.list_movies())
    print("The average is: ", average(list_of_movies))
    median(list_of_movies)
    best_and_worst_movie(list_of_movies)


def average(list_of_movies):
    """average of all movies"""
    avg = 0.0
    for movie in list_of_movies:
        avg += float(movie["rating"])
    return round(avg / len(list_of_movies), 1)


def median(list_of_movies):
    """Median of all movies"""
    list_for_median = list()
    for movie in list_of_movies:
        list_for_median.append(float(movie["rating"]))
    list_for_median.sort()
    print(f"The median is: {statistics.median(list_for_median)}")


def best_and_worst_movie(list_of_movies):
    """List the best and the worst movies"""
    highest_rate = 0.0
    lowest_rate = 10.0

    # Check for empty list:
    if not list_of_movies:
        print("No movies to compare!")
        return
        # check the highest rate and the lowest of the movie
    try:
        highest_rate = max(m["rating"] for m in list_of_movies)
        lowest_rate = min(m["rating"] for m in list_of_movies)
    except Exception:
        print("At least one Movie has no rating, \
              please add Rating for precise calculation")
        
    # print all movies with the same rating
    print("The best movies are: ")
    for movies in list_of_movies:
        if movies["rating"] == highest_rate:
            print(f'{movies["name"]}:{movies["rating"]}')

    print("The worst movies are: ")
    for movie in list_of_movies:
        if movie["rating"] == lowest_rate:
            print(f'{movie["name"]}:{movie["rating"]}')


def create_list_of_movies(dict_of_dicts):
    """
    Helper Method to create a compatible
    data structure from previous code
    returns a List with Dictionaries
    """
    list_of_movies = list()
    for title, data in dict_of_dicts.items():
        moviedict = {
                    "name": title,
                    "rating": float(data["rating"])
                    }
        list_of_movies.append(moviedict)
    return list_of_movies


def random_movie():
    """Picks a random movie from the database"""
    database = storage.list_movies()
    if bool(database):
        random_movie, random_movie_data = random.choice(list(database.items()))
        print(
            f'Here is your movie: {random_movie} \n'
            f'With a rating of: {random_movie_data["rating"]} \n'
            f'Which was released: {random_movie_data["year"]}')


def search_movie():
    """
    Searchs the database if the movie is already there,
    prints the result
    """
    found = False
    database = storage.list_movies()
    search = input("Enter Part of the Movie name: ")
    print("Following movies match with your letters: ")
    for movie, moviedetails in database.items():
        if search.lower() in movie.lower():
            found = True
            print(
                f'{movie}, '
                f'{moviedetails["rating"]}, '
                f'{moviedetails["year"]}')
    if not found:
        print("No match with your letters.")


def sort_by_rating():
    """
    Printing the movies descending in relation to their rating
    """
    list_of_movies = create_list_of_movies(storage.list_movies())
    new_sorted_list = list_of_movies[:]
    highest_value = 0
    moviename = ""
    while bool(new_sorted_list):
        for movie in new_sorted_list:
            if movie["rating"] > highest_value:
                highest_value = movie["rating"]
                moviename = movie["name"]
        print(f"{moviename}:{highest_value}")
        for movie in new_sorted_list:
            if moviename == movie["name"] and highest_value == movie["rating"]:
                new_sorted_list.remove(movie)
                continue
        highest_value = 0


def check_ifNOT_contains(item, movie_database):
    """Helpermethod to check if movie is in database"""
    if item not in movie_database:
        print(f"Error: {item} doesn't exist")
        return True


def exit_cli():
    print("Bye!")


def show_menu():
    print("____ My Movies Database____")
    menu_choices = ["Exit", "List movies", "Add movie", "Delete movie",
                    "Update movie", "Stats", "Random movie",
                    "Search movie", "Movies sorted by rating",
                    "Generate Website"]
    boolisch = True
    while boolisch:
        try:
            print_menu(menu_choices)
            point = int(input())
            print(f"You choosed {menu_choices[point]}")
            if point == 0:
                exit_cli()
                boolisch = False
            if point == 1:
                list_all_movies()
            if point == 2:
                add_movie()
            if point == 3:
                delete_movie()
            if point == 4:
                update_movie()
            if point == 5:
                stats()
            if point == 6:
                random_movie()
            if point == 7:
                search_movie()
            if point == 8:
                sort_by_rating()
            if point == 9:
                write_html()
        except Exception as e:
            print(f"{e} Please enter a valid number (0-9)")
            continue


if __name__ == "__main__":
    show_menu()
