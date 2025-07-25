from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
                            CREATE TABLE IF NOT EXISTS movies (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  title TEXT UNIQUE NOT NULL,
                                  year INTEGER NOT NULL,
                                  rating REAL NOT NULL,
                                  url VARCHAR(100)
                                )
                            """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text(
            "SELECT title, year, rating, url FROM movies"))
        movies = result.fetchall()
        return {row[0]: {
            "year": row[1],
            "rating": row[2],
            "url": row[3]
        } for row in movies}


def add_movie(title, year, rating, url):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text(
                "INSERT INTO movies (title, year, rating, url) "
                "VALUES (:title, :year, :rating, :url)"),
                {"title": title, "year": year, "rating": rating, "url": url})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            query = text("DELETE FROM movies WHERE title =: title")
            result = connection.execute(query, {"title": title})
            connection.commit()
            # check if any rows are affected
            if result.rowcount > 0:
                print(f"Movie {title} successfully deleted from Database")
                return True
            else:
                print(f"Movie {title} not found in database.")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            query = text(
                "UPDATE movies "
                "SET rating = :rating "
                "WHERE title = :title"
            )
            result = connection.execute(query, {
                "title": title, "rating": rating
                })
            connection.commit()

            if result.rowcount > 0:
                print(f"Movie {title} successfully updated")
                return True
            else:
                print(f"Movie {title} not found in database.")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
