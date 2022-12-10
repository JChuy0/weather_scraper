# Created by Jason Chuy
"""This module plots data onto a graph."""

import logging
import matplotlib.pyplot as plt

try:
    class PlotOperations:
        """Plots the weather data on a graph."""

        def my_box_plot(data, years):
            """Retrieves data from the database and draws a boxplot graph."""

            try:
                # Creates 12 empty lists
                january, february, march, april, may, june = ([] for i in range(6))
                july, august, september, october, november, december = ([] for i in range(6))

                # Filters the data for each month into their appropriate list
                for i in data:
                    # Take a date, remove everything but the month, then convert it to an int.
                    month = int(i[0][5:-3])

                    if month == 1:
                        january.append(i[1])
                    elif month == 2:
                        february.append(i[1])
                    elif month == 3:
                        march.append(i[1])
                    elif month == 4:
                        april.append(i[1])
                    elif month == 5:
                        may.append(i[1])
                    elif month == 6:
                        june.append(i[1])
                    elif month == 7:
                        july.append(i[1])
                    elif month == 8:
                        august.append(i[1])
                    elif month == 9:
                        september.append(i[1])
                    elif month == 10:
                        october.append(i[1])
                    elif month == 11:
                        november.append(i[1])
                    elif month == 12:
                        december.append(i[1])

                monthly_temps = [january, february, march, april, may, june,
                                july, august, september, october, november, december]

                plt.boxplot(monthly_temps)
                plt.xlabel("Month")
                plt.ylabel("Temperature (Celsius)")
                plt.title(f"Monthly Temperature Distribution for: {years[0]} to {years[1]} ")
                plt.grid()
                plt.show()
            except Exception as error:
                logging.error(f"***Error occured in my_box_plot method.*** {error}")


        def my_line_plot(data, month_year):
            """Retrieves data from the database and draws a line plot graph."""

            try:
                month_temp = []

                for i in data:
                    month_temp.append(i[1])

                plt.plot(month_temp)
                plt.xlabel("Day of Month")
                plt.ylabel("Average Daily Temp")
                plt.title(f"Temperature for: {month_year[0]}-{month_year[1]}")
                plt.grid()
                plt.show()
            except Exception as error:
                logging.error(f"***Error occured in my_line_plot method.*** {error}")

except Exception as error_outer:
    logging.error(f"***Error occured in plot_operations module.*** {error_outer}")
