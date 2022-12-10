# Created by Jason Chuy
"""This module will scrape weather data from the internet."""

from datetime import datetime
import urllib.request
from html.parser import HTMLParser
import logging

try:
    weather = {}
    current_title = ""

    class WeatherScraper(HTMLParser):
        """Scrapes weather data."""

        def __init__(self) -> None:
            """Initializes the weather scraper object."""
            
            super().__init__()
            self.tbody_bool = False
            self.tr_bool = False
            self.td_bool = False
            self.a_bool = False
            self.strong_bool = False
            self.abbr_bool = False
            self.h1_bool = False

            self.counter = 0
            self.date = ""
            self.daily_temps = {}


        def handle_starttag(self, tag, attrs):
            """Sets a boolean to true when entering a certain tag."""

            try:
                if tag == "tbody":
                    self.tbody_bool = True

                if tag == "tr":
                    self.tr_bool = True

                if tag == "td":
                    self.td_bool = True

                if tag == "a":
                    self.a_bool = True

                if tag == "strong":
                    self.strong_bool = True

                if tag == "abbr":
                    tempstr = str(attrs)

                    # Grabs the date for each dictonary entry
                    if "Average" not in tempstr and "Extreme" not in tempstr:
                        tempnum = tempstr.find(",")
                        self.date = tempstr[tempnum + 3 : -3].strip()
                        self.abbr_bool = True

                if tag == "h1":
                    self.h1_bool = True
            except Exception as error:
                logging.error(f"***Error occured in handle_starttag method.*** {error}")


        def handle_endtag(self, tag):
            """Sets a boolean to false when exiting certain tags."""

            try:
                global weather

                if tag == "tbody":
                    self.tbody_bool = False

                if tag == "tr":
                    self.tr_bool = False
                    self.counter = 0

                    # Adds new entry to weather dictonary
                    if self.tbody_bool and self.date != "":
                        if self.daily_temps["Max"] == "" or self.daily_temps["Min"] == "" or self.daily_temps["Mean"] == "":
                            pass
                        else:
                            # Formats the date from 'September 30, 2022' to '2022-09-30'
                            format = "%B %d, %Y"
                            date = datetime.strptime(self.date, format).date()

                            weather[date] = self.daily_temps

                    self.date = ""
                    self.daily_temps = {}

                if tag == "td":
                    self.td_bool = False

                if tag == "a":
                    self.a_bool = False

                if tag == "strong":
                    self.strong_bool = False

                if tag == "abbr":
                    self.abbr_bool = False

                if tag == "h1":
                    self.h1_bool = False
            except Exception as error:
                logging.error(f"***Error occured in handle_endtag method.*** {error}")


        def handle_data(self, data):
            """Scrapes the Min, Max, and Mean temperatures."""

            try:
                global current_title

                # Adds the temperature for the day to daily_temps
                if self.tbody_bool and self.tr_bool and self.td_bool:
                    if self.a_bool is False and self.strong_bool is False:

                        if self.counter == 0:
                            self.daily_temps["Max"] = data.strip()
                        elif self.counter == 1:
                            self.daily_temps["Min"] = data.strip()
                        elif self.counter == 2:
                            self.daily_temps["Mean"] = data.strip()

                        self.counter = self.counter + 1

                if self.h1_bool:
                    current_title = data
            except Exception as error:
                logging.error(f"***Error occured in handle_data method.*** {error}")


    def scrape_data(latest_date):
        """Scrapes data."""

        try:
            myparser = WeatherScraper()

            today = datetime.now()
            month = today.month
            year = today.year

            while True:
                prev_title = current_title

                with urllib.request.urlopen(f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Month={month}&Year={year}") as response:
                    html = str(response.read())

                myparser.feed(html)

                # This is used when updating weather data. Stops scraping data if the latest date from the DB is found in the weather dictionary.
                if len(latest_date) > 2:
                    for k in weather:
                        temp_date = k.strftime("%Y-%m-%d")
                        temp_date = temp_date[:-3]

                        if latest_date == temp_date:
                            return weather

                month = month - 1
                if month == 0:
                    month = 12
                    year = year - 1

                # Ends the loop when there is no more data to retrieve
                if current_title == prev_title:
                    break

            return weather
        except Exception as error:
            logging.error(f"***Error occured in scrape_data method.*** {error}")

except Exception as error_outer:
    logging.error(f"***Error occured in scrape_weather module.*** {error_outer}")
