import time
import pandas as pd
import numpy as np
from pandas._libs.tslibs.timedeltas import Timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_name = input("Choose which city you want to examine(chicago, new york city, washington): ")
        try:
            city = CITY_DATA[city_name.lower()]
        except:
            print("City name is invalid. Please enter a valid city name(chicago, new york city, washington).\n")
            continue
        break
    # get user input for month (all, january, february, ... , june)
    print("")
    months = ["all", "january", "february", "march", "april", "may", "june"]
    while True:
        month = input("Choose which month to filter by (all, january, february, ..., june): ")
        if month.lower() not in months:
            print("Month name is invalid. Please enter a valid month (all, january, february, ..., june).\n")
            continue
        else:
            break
    print("")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while True:
        day = input("Choose which day of the week to filter by (all, monday, tuesday, ... sunday): ")
        if day.lower() not in days:
            print("Day name is invalid. Please enter a valid day of the week (all, monday, tuesday, ... sunday).\n")
            continue
        else:
            break
    print("")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)

    df["Start Time"] = pd.to_datetime(df["Start Time"], format ="%Y-%m-%d %H:%M:%S")
    df["End Time"] = pd.to_datetime(df["End Time"], format ="%Y-%m-%d %H:%M:%S")

    df["Month"] = df["Start Time"].dt.month
    df["Day_Of_Week"] = df["Start Time"].dt.day_name()

    months = ["january", "february", "march", "april", "may", "june"]
    if not (month == "all"):
        month = months.index(month) + 1
        df = df[df["Month"] == month]
    
    if not (day == "all"):
        df = df[df["Day_Of_Week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ["january", "february", "march", "april", "may", "june"]
    month = int(df["Month"].mode())
    most_common_month = months[month - 1].title()
    print("Most common month for borrowing is {}".format(most_common_month))

    # display the most common day of week
    day = df["Day_Of_Week"].mode().values[0]
    print("Most common day to borrow is {}".format(day))

    # display the most common start hour
    df["Hour"] = df["Start Time"].dt.hour
    most_common_hour = int(df["Hour"].mode())
    print("Most common hour to borrow is {}\n".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df["Start Station"].mode().values[0]
    print("Most common start station is {}".format(most_common_start))
    # display most commonly used end station
    
    most_common_end = df["End Station"].mode().values[0]
    print("Most common end station is {}".format(most_common_end))

    # display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(["Start Station", "End Station"], dropna = True).size().sort_values(ascending = False).index.tolist()
    print("Most common combination is {} to {}".format(most_common_combination[0][0], most_common_combination[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    df["Travel Time"] = (df["End Time"] - df["Start Time"])
    
    # display total travel time
    print("Total travel time is {} hours".format(pd.DataFrame.sum(df["Travel Time"]) / pd.Timedelta(hours = 1)))

    # display mean travel time
    print("Mean travel time is {} minutes".format(pd.DataFrame.mean(df["Travel Time"], axis=0) /pd.Timedelta(minutes = 1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of each user type:\n")
    print(df["User Type"].value_counts().to_string())

    # Display counts of gender
    print("Number of each Gender:\n")
    print(df["Gender"].value_counts().to_string())
    print("\n")

    # Display earliest, most recent, and most common year of birth
    print("Oldest user was born in {}".format(int(pd.DataFrame.min(df["Birth Year"]))))
    print("Youngest user was born in {}".format(int(pd.DataFrame.max(df["Birth Year"]))))
    print("Most common birth year is {}".format(int(df["Birth Year"].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
