# Created by Jason Chuy
"""This modules handles the user interaction."""

import logging
import PySimpleGUI as sg
import plot_operations
from db_operations import DBOperations
from scrape_weather import scrape_data

try:
    logging.basicConfig(filename="weather_log.log", level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt='%m/%d/%Y %I:%M:%S %p')

    class WeatherProcessor:
        """Handles the processing for the entire app."""

        def build_gui():
            """This function builds the GUI."""

            try:
                sg.theme('BluePurple')
                layout = [[sg.Text("Persistent window", key="box"), sg.Push(),
                                    sg.Button("Delete/Rebuild"), sg.Button("Update")],
                            [sg.Text("", key="errorbox")],
                            [sg.Text("Month"), sg.Text("Year")],
                            [sg.Input(size=(10), key="key1"), sg.Input(size=(10), key="key2"),
                                    sg.Button("Line Plot")],
                            [sg.Text("Year"), sg.Text("Year")],
                            [sg.Input(size=(10), key="key3"), sg.Input(size=(10), key="key4"),
                                    sg.Button("Box Plot")],
                            [sg.Exit()]]

                window = sg.Window("Weather Processor", layout)

                while True:
                    event, values = window.read()

                    if event == "Line Plot":
                        month_year = (values["key1"], values["key2"])
                        mydata = DBOperations.fetch_data(event, month_year)
                        plot_operations.PlotOperations.my_line_plot(mydata, month_year)

                    elif event == "Box Plot":
                        years = (values["key3"], values["key4"])
                        mydata = DBOperations.fetch_data(event, years)
                        plot_operations.PlotOperations.my_box_plot(mydata, years)

                    elif event == "Update":
                        latest_date = DBOperations.update_data()
                        # print(f"latest_date is: {latest_date}. It's type is: {type(latest_date)}.")
                        new_data = scrape_data(latest_date)
                        DBOperations.save_data(new_data)

                    elif event == "Delete/Rebuild":
                        DBOperations.purge_data()
                        emptystr = ""
                        DBOperations.save_data(scrape_data(emptystr))

                    if event in (sg.WIN_CLOSED, "Exit"):
                        break

                window.close()
            except Exception as error:
                logging.error(f"***Error occured in build_gui method.*** {error}")

    WeatherProcessor.build_gui()

except Exception as error_outer:
    logging.error(error_outer)
