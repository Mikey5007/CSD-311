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
        print()  # blank line between records

if __name__ == "__main__":
    try:
        db = mysql.connector.connect(**CONFIG)

        print("-- Connection Successful --\nUser: {}\nHost: {}\nDatabase: {}".format(
            CONFIG["user"], CONFIG["host"], CONFIG["database"]))

        cursor = db.cursor()

        cursor.execute("USE movies")

        # -----------------------------------------
        # Query 1: Select all fields from studio
        # -----------------------------------------
        print("\n-- QUERY 1: All studios --")
        cursor.execute("SELECT * FROM studio;")
        studios = cursor.fetchall()
        print_key_values(cursor, studios)

        # -----------------------------------------
        # Query 2: Select all fields from genre
        # -----------------------------------------
        print("\n-- QUERY 2: All genres --")
        cursor.execute("SELECT * FROM genre;")
        genres = cursor.fetchall()
        print_key_values(cursor, genres)


        # -----------------------------------------
        # Query 3: Movie names with runtime < 120
        # -----------------------------------------
        print("\n-- QUERY 3: Movies with runtime < 2 hours --")
        cursor.execute("""
            SELECT film_name 
            FROM film 
            WHERE film_runtime < 120;
        """)
        movies_short = cursor.fetchall()
        print_key_values(cursor, movies_short)


        # -----------------------------------------
        # Query 4: Film names and directors grouped by director
        # -----------------------------------------
        print("\n-- QUERY 4: Film names and directors grouped by director --")
        cursor.execute("""
            SELECT film_director, film_name
            FROM film
            ORDER BY film_director, film_name;
        """)
        grouped = cursor.fetchall()
        print_key_values(cursor, grouped)


    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        cursor.close()
        db.close()
