""" import statements """
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

SECRETS = dotenv_values(".env")
CONFIG = {
    "user": SECRETS["USER"],
    "password": SECRETS["PASSWORD"],
    "host": SECRETS["HOST"],
    "database": SECRETS["DATABASE"],
    "raise_on_warnings": True
}

def print_key_values(cursor, rows):
    column_names = cursor.column_names
    for row in rows:
        for col, val in zip(column_names, row):
            print(f"{col}: {val}")
        print()

def show_films(cursor, title):
    """
    Execute an inner join on all tables,
    iterate over the dataset and output the results.
    """
    cursor.execute("""
        SELECT 
            film_name AS Name, 
            film_director AS Director, 
            genre_name AS Genre, 
            studio_name AS 'Studio Name'
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id;
    """)
    films = cursor.fetchall()
    print("\n -- {} --".format(title))
    for film in films:
        print(
            "Film Name: {}\n"
            "Director: {}\n"
            "Genre Name: {}\n"
            "Studio Name: {}\n".format(film[0], film[1], film[2], film[3])
        )

def insert_film(cursor, film_data):
    """
    Insert a new film record into the film table.
    """
    insert_query = """
        INSERT INTO film (
            film_name, 
            film_releaseDate, 
            film_runtime, 
            film_director, 
            studio_id, 
            genre_id
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, film_data)

def update_film_genre(cursor, film_name, new_genre_id):
    """Update the genre of a film."""
    update_query = """
        UPDATE film
        SET genre_id = %s
        WHERE film_name = %s;
    """
    cursor.execute(update_query, (new_genre_id, film_name))

def delete_film(cursor, film_name):
    """Delete a film record from the film table."""
    delete_query = """
        DELETE FROM film
        WHERE film_name = %s;
    """
    cursor.execute(delete_query, (film_name,))

if __name__ == "__main__":
    db = None
    cursor = None
    try:
        db = mysql.connector.connect(**CONFIG)
        db.autocommit = True

        print("-- Connection Successful --\nUser: {}\nHost: {}\nDatabase: {}".format(
            CONFIG["user"], CONFIG["host"], CONFIG["database"]))

        cursor = db.cursor()
        cursor.execute("USE movies")

        # Initial display
        show_films(cursor, "DISPLAYING FILMS")
        insert_film_data = (
            "Inception",       # film_name
            "2010",            # film_releaseDate (year as VARCHAR(5))
            148,               # film_runtime (INT)
            "Christopher Nolan",  # film_director
            3,                 # studio_id
            2                  # genre_id
        )
        insert_film(cursor, insert_film_data)
        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        # Update Alien's genre to 1 (Horror)
        update_film_genre(cursor, "Alien", 1)
        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

        # Delete Gladiator
        delete_film(cursor, "Gladiator")
        show_films(cursor, "DISPLAYING FILMS AFTER DELETING Gladiator")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")
        else:
            print(err)

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None and db.is_connected():
            db.close()
