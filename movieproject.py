import statistics
import random
import matplotlib.pyplot as plt
import os
import movie_storage


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
    returns: 
    """
    all_movies = movie_storage.get_movies()
    print(f"There are {len(all_movies)} movies in total")
    for movie, moviedetails in all_movies.items():
        print(f"Title: {moviedetails['name']}")
        print(f"Rating: {moviedetails['rating']}")
        print(f"Releaseyear: {moviedetails['release']}")
        print("- - - - - - - - - - - - - - -")


def add_movie():
    """Adding a Movie to the Database"""
    list_of_movies = list(movie_storage.get_movies())
    movierating = 0.0
    releaseyear = 0000
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
            try:
                movierating = input(
                    "Add the rating of the movie. Format: X.X ")
                if len(movierating) > 3 or len(movierating) < 3 or (
                        movierating[1] != "."):
                    raise ValueError
                else:
                    movierating = float(movierating)
                    validation = True
            except ValueError:
                print("Please enter the right format for the rating. I.e. 5.4")
        validation = False
        while not validation:
            try:
                releaseyear = input(
                    "Add the releaseyear of the movie. "
                    "For example: 2002 ")
                if len(releaseyear) > 4 or len(releaseyear) < 4:
                    raise TypeError
                else:
                    validation = True
                    movie_storage.add_movie(
                        moviename,
                        rating=movierating,
                        year=releaseyear)
                    print(
                        f"Movie {moviename} with a "
                        f"{movierating} rating released "
                        f"{releaseyear} was added to the database")
                    validation = True
            except TypeError:
                print(
                    "Wrong date format. "
                    "Please enter the year i.e. 2000")


def delete_movie():
    """Deletes a movie from the database"""
    try:
        name_of_movie_to_delete = input(
            "Enter the name of the movie you wish to delete: ")
        movie_storage.delete_movie(name_of_movie_to_delete)
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
            if len(new_rating) < 3 or (
                len(new_rating) > 3) or (
                    new_rating[1] != "."):
                raise ValueError
            else:
                validation = True
                movie_storage.update_movie(movie_to_update, float(new_rating))
        except ValueError:
            print("The rating must be written in the format X.X")
            print("Please try again")


def stats():
    """Printing the average, median, best and worst movies"""
    list_of_movies = create_list_of_movies(movie_storage.get_movies())
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
    highest_rate = max(m["rating"] for m in list_of_movies)
    lowest_rate = min(m["rating"] for m in list_of_movies)

    # print all movies with the same rating
    print("The best movies are: ")
    for movie in list_of_movies:
        if movie["rating"] == highest_rate:
            print(f'{movie["name"]}:{movie["rating"]}')

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
    for movie, moviedetails in dict_of_dicts.items():
        moviedict = {
                    "name": moviedetails["name"],
                    "rating": float(moviedetails["rating"])
                    }
        list_of_movies.append(moviedict)
    return list_of_movies


def random_movie():
    database = movie_storage.get_movies()
    if bool(database):
        random_movie = random.choice(list(database.items()))
        print(
            f'Here is your movie: {random_movie[1]["name"]} \n'
            f'With a rating of: {random_movie[1]["rating"]} \n'
            f'Which was released: {random_movie[1]["release"]}')


def search_movie():
    found = False
    database = movie_storage.get_movies()
    search = input("Enter Part of the Movie name: ")
    print("Following movies match with your letters: ")
    for movie, moviedetails in database.items():
        if search.lower() in movie.lower():
            found = True
            print(
                f'{moviedetails["name"]}, '
                f'{moviedetails["rating"]}, '
                f'{moviedetails["release"]}')
    if not found:
        print("No match with your letters.")


def sort_by_rating():
    """
    Printing the movies descending in relation to their rating
    """
    list_of_movies = create_list_of_movies(movie_storage.get_movies())
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


def create_rating_histogram():
    # Bewertungen in Liste packen
    movie_database = movie_storage.get_movies()
    print(movie_database)
    ratings = list()
    for movie, moviedetails in movie_database.items():
        ratings.append(moviedetails["rating"])
    print(ratings)
    # Histogramm erstellen
    # `bins` definiert die Anzahl der Balken
    plt.hist(ratings, bins=5, edgecolor="black", color='peachpuff')
    plt.xlabel("Rating (0-10)")
    plt.ylabel("Numbers of Movies")
    plt.title("Ratings of Movies")

    print(
        "Where do you want to save this picture? "
        "(for example: /Users/Name/Desktop/filme.png)")
    save_path = input("Enter path: ").strip()
    if save_path:
        try:
            plt.savefig(save_path)
            print(f"Picture was saved: {os.path.abspath(save_path)}")
        except Exception as e:
            print(f"Error during saving: {e}")
    else:
        print("No path entered.")
    plt.show()


def check_ifNOT_contains(item, movie_database):
    """Helpermethod to check if movie is in database"""
    if item not in movie_database:
        print(f"Error: {item} doesn't exist")
        return True


def exit_cli():
    print("Bye!")


def main():
    print("____ My Movies Database____")
    menu_choices = ["Exit", "List movies", "Add movie", "Delete movie",
                    "Update movie", "Stats", "Random movie",
                    "Search movie", "Movies sorted by rating",
                    "Create Rating Histogram"]
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
                create_rating_histogram()
        except Exception:
            print("Please enter a valid number (0-9)")
            continue


if __name__ == "__main__":
    main()
