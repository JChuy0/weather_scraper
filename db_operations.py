# Created by Jason Chuy
"""This module handles all of the database functions."""

import logging
from dbcm import DBCM

try:
    class DBOperations():
        """Performs CRUD functionality for a database."""

        def fetch_data(plot_type, data) -> str:
            """Fetches and returns the requested data."""

            try:

                query = ""

                if plot_type == "Line Plot":
                    month = data[0]
                    year = data[1]

                    # If the user enters a single digit number, add a 0 in front.
                    if len(month) == 1:
                        month = f"0{month}"

                    query = f"""SELECT date, mean_temp
                                FROM myweather
                                WHERE date LIKE '{year}-{month}%'"""
                elif plot_type == "Box Plot":
                    year1 = data[0] + "-01-01"
                    year2 = data[1] + "-12-31"

                    query = f"""SELECT date, mean_temp
                                FROM myweather
                                WHERE date BETWEEN '{year1}' AND '{year2}'"""

                with DBCM() as cur:
                    mydata = ()

                    for row in cur.execute(query):
                        mydata = mydata + (row, )

                    return mydata
            except Exception as error:
                logging.error(f"***Error occured in fetch_data method.*** {error}")


        def update_data():
            """Updates the database."""

            try:
                with DBCM() as cur:
                    # This finds the latest date stored in the database.
                    for i in cur.execute("SELECT date FROM myweather ORDER BY date DESC LIMIT 1"):
                        latest_date = i[0][:-3]

                        return latest_date

            except Exception as error:
                logging.error(f"***Error occured in update_data method.*** {error}")


        def save_data(data) -> dict:
            """Saves new data to the database."""

            try:
                with DBCM() as cur:
                    cur.execute("""CREATE TABLE if not exists myweather
                        (id integer primary key autoincrement not null,
                        date text,
                        max_temp real,
                        min_temp real,
                        mean_temp real);""")

                    sql = ("""INSERT INTO myweather (date, max_temp, min_temp, mean_temp)
                            values(?, ?, ?, ?)""")

                    # Takes the date, max, min, mean temps and puts them in a tuple,
                    #   then adds them to the database.
                    # But it will ignore any duplicate dates.
                    for key1, value1 in data.items():
                        mytup = (key1,)

                        for key2, value2 in value1.items():
                            if value2 != "":
                                mytup = mytup + (float(value2),)

                        # Checks to see if a given date already exists in the database.
                        sqlcount = ("SELECT COUNT(*) FROM myweather WHERE date=?")
                        mydate = (f'{key1}', )

                        # Adds new entry to database, if the date is unique
                        for i in cur.execute(sqlcount, mydate):
                            if i[0] == 0:
                                print("Found new day of data.")
                                cur.execute(sql, mytup)
            except Exception as error:
                logging.error(f"***Error occured in save_data method.*** {error}")


        def initialize_db():
            """Creates a new database."""

            try:
                with DBCM() as cur:
                    cur.execute("""CREATE TABLE if not exists myweather
                                (id integer primary key autoincrement not null,
                                date text,
                                max_temp real,
                                min_temp real,
                                mean_temp real);""")
            except Exception as error:
                logging.error(f"***Error occured in initialize_db method.*** {error}")


        def purge_data():
            """Deletes all data from database."""

            try:
                with DBCM() as cur:
                    cur.execute("DROP TABLE myweather")
            except Exception as error:
                logging.error(f"***Error occured in purge_data method.*** {error}")

except Exception as error_outer:
    logging.error(f"***Error occured in db_operations module.*** {error_outer}")
