import time
import numpy as np
import pandas as pd


CITIES = {'CHI': 'chicago.csv', 'WA': 'washington.csv', 'NY': 'new_york_city.csv'}
months = ['January', 'February', 'March', 'April', 'May', 'June']
days = ['Monday', 'Tuesday', 'Wednessday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

loading = '.'*4
section_breaker = '='*65

def loader():
    """ Prints a 'Please wait ...' to mimic a loader """
    i = 1
    print(' ')
    print('Please wait', end=' ')
    while i < len(loading):
        print(loading[i], end='', flush=True)
        time.sleep(1)
        i+=1
    print(' \n  ')

def delay(duration):
    """ Delays an execution
        Args:
            duration (int): Specifies how long the delay lasts in seconds
        Returns:
            the time delay (as in time.sleep(duration))
    """
    return time.sleep(duration)

def section_break():
    """ Displays a breaker
        Returns:
            (str) : ====
    """
    i = 1
    while i < len(section_breaker):
        print(section_breaker[i], end='', flush=True)
        time.sleep(0.03)
        i+=1

def get_filters():
    """ Gets filter details from users input
        Returns:
            (str): city, month, day (as specified by the users input)
    """

    city, month, day = '', '', ''

    print(' \n  ')
    print('Welcome to bikeshare\'s database!')
    section_break()
    print(' \n  ')

    try:
        # requests for the user's input on 'city' until it matches one of the available cities (NY, CHI, WA)
        while city.lower() not in [c.lower() for c in CITIES.keys()]:
            print('Please select a city.')
            delay(0.4)
            print('Be sure to type: ')
            for index, city in CITIES.items():
                print('              {} for {}'.format(index, city[:-4].title()))
            delay(1)
            city = str(input('What city do you choose? '))
            delay(1)
        print(' ')

        month = str(input(' \nEnter a month you\'re interested in. \nEnter January, February, March, April, May or June \nLeave blank for all: '))
        delay(0.4)
        day = str(input(' \nEnter a day of the week you\'re interested in.\nEnter Monday, Tuesday, Wednessday, Thursday, Friday. \nLeave blank for all: '))

        return city, month, day
    except KeyboardInterrupt:
        print('Your interrupted the process')
        return False
    except Exception as e:
        print('An error occurred', e)
        return False

def load_data(city):
    """ Reads the data from the CSV
        Args:
            city(str): One of the items in [CITIES] (based on the user's input)
        Returns:
            city(dataframe): The data read from the city's csv file, including the `day`, `month`, `hour` columns
                extracted from the `Start Time` columns
        """
    city_data = pd.read_csv(CITIES[city.upper()])
    city_data['Start Time'] = pd.to_datetime(city_data['Start Time'])
    city_data['day'] = city_data['Start Time'].dt.dayofweek
    city_data['month'] = city_data['Start Time'].dt.month
    city_data['hour'] = city_data['Start Time'].dt.hour


    return city_data

def calculate_execution_time():
    """ Calculates time of execution of functions """
    start_time = time.time()
    print("\nThis took %s seconds." % (time.time() - start_time))

city, month, day = get_filters()


def filtered_data(dataframe):
    """ Takes in a dataframe to filter by month and day where applicable
        Args:
            dataframe(dataframe): The dataframe to be filtered
        Returns: (dataframe)
            Filtered dataframe. Could be filtered by month and/or day or neither. Depending on the user's input.
    """
    if (month.lower() in [m.lower() for m in months]):
        month_index = months.index(month.title())
        dataframe = dataframe[(dataframe['month'] == (month_index + 1))]
    if (day.lower() in [d.lower() for d in days]):
        day_index = days.index(day.title())
        dataframe = dataframe[dataframe['day'] == day_index]
    return dataframe

def popular_travel_times(city_data):
    """ Queries/Filters dataframe for information about travel times
        Args:
            city_data(dataframe)
        Returns: (str)
            Most Common month = months_mode(str),
            Most common day = days_mode(str),
            Most Common Hour= hour_mode(int)
    """
    months_mode = city_data['month'].mode()[0]
    days_mode = city_data['day'].mode()[0]
    hour_mode = city_data['hour'].mode()[0]

    return 'Most Common month = {}, \nMost common day = {}, \nMost Common Hour = {}hrs'.format(months[months_mode - 1], days[days_mode], hour_mode)


def popular_stations_and_trip(city_data):
    """ Queries/Filters dataframe for information about stations and trip
        Args:
            city_data(dataframe)
        Returns: (str)
            Most Common Start Station = start_station_mode(str)
            Most Common End Station = end_station_mode(str)
            Most Common Trip (Start Station - End Station) = most_common_trip(str)
    """
    start_station_mode = city_data['Start Station'].mode()[0]
    end_station_mode = city_data['End Station'].mode()[0]
    city_data_copy = city_data.copy()
    city_data_copy['Stations'] = city_data['Start Station'] +' - ' + city_data['End Station']
    most_common_trip = city_data_copy['Stations'].mode()[0]

    return 'Most Common Start Station = {},\nMost Common End Station = {}, \nMost Common Trip (Start Station - End Station) = {}'.format(start_station_mode, end_station_mode, most_common_trip)


def trip_duration(city_data):
    """ Queries/Filters dataframe for information about user's trip
        Args:
            city_data(dataframe)
        Returns: (str)
            Total travel time = total_travel_time(str),
            Average travel time = average_travel_time(str)
    """
    total_travel_time = city_data['Trip Duration'].sum()
    average_travel_time = city_data['Trip Duration'].mean()

    return 'Total travel time = {}\nAverage travel time = {}'.format(total_travel_time, average_travel_time)


def user_info(city_data):
    """ Queries/Filters dataframe for user data
        Parameter:
            city_data(dataframe)
        Returns: (str)
            User Type Count = user_type_count(int),
            Gender Count = gender_count(int),
            Earliest Year of Birth = earliest_yob(float),
            Most Common YOB = most_common_yob(float/int),
            Most Recent YOB = most_recent_yob(float/int)
    """
    try:
        user_type_count = city_data['User Type'].value_counts()
        # assign the value `NA` to computations that may be unavailable for some cities
        gender_count, earliest_yob, most_common_yob, most_recent_yob = 'Not Provided', 'Not Provided', 'Not Provided', 'Not Provided'

        # check city user specified to ensure columns needed for these computations are present
        if city.upper() in ['NY', 'CHI']:
            gender_count = city_data['Gender'].value_counts()
            earliest_yob = city_data['Birth Year'].min()
            most_common_yob = city_data['Birth Year'].mode()[0]
            sorted_city_data = city_data.sort_values('Start Time', ascending=False)
            most_recent_yob = sorted_city_data['Birth Year'].iloc[0]

        return 'User Type Count: \n{}\n \nGender Count: \n{}\n \nEarliest Year of Birth = {},\nMost Common YOB = {},\nMost Recent YOB = {}'.format(user_type_count, gender_count, earliest_yob, most_common_yob, most_recent_yob)
    except Exception as e:
        return 'An error occurred: {}'.format(e)

def get_top_rows(city_data):
    """ Returns the number of columns as specified by the user from the raw dataframe
        Args:
            city_data(dataframe)
        Returns: (dataframe)
            A limited number of columns from the dataframe (specified by the user)
    """
    try:
        no_of_rows = int(input('How many rows would you like to view from {}\'s data? '.format(CITIES[city.upper()][:-4].upper())))

        return city_data.head(no_of_rows)
    except ValueError:
        print('Invalid input')
        users_choice = int(input('Enter 0 or 1 based on the choices listed above: '))
    except Exception as e:
        print(e)

def filter_by_user_type(city_data):
    """ Filters dataframe by user type
        Args:
            city_data(dataframe)
        Returns:
            Filtered dataframe
    """
    try:
        user_type = ''
        while user_type != 'Subscriber' or user_type != 'Customer':
            user_type = str(input('Enter "Subscriber" or "Customer" as filter option: '))

            return city_data[city_data['User Type'] == user_type.title()]
    except ValueError:
        print('Invalid input')
        user_type = ''
    except Exception as e:
        print(e)

def filter_by_birth_year(city_data):
    """ Filters dataframe by birth year
        Args:
            city_data(dataframe)
        Returns:
            Filtered dataframe
    """
    try:
        year = 0
        while year < 1800:
            year = float(input('Enter customer\'s birth year you\'re interested in: '))

        return city_data[city_data['Birth Year'] == year]
    except ValueError:
        print('Invalid input')
        year = 0
    except Exception as e:
        print(e)

def filter_by_gender(city_data):
    """ Filters dataframe by gender
        Args:
            city_data(dataframe)
        Returns:
            Filtered dataframe
    """
    try:
        # check if the specified city has the column `gender`
        if city.upper() not in ['NY', 'CHI']:
            return 'The \'Gender\' field is unavailable for {}'.format(city.upper())
        gender = False
        while gender == False:
            gender = str(input('Enter "Male" or "Female" as filter option: '))

        return city_data[city_data['Gender'] == gender]
    except ValueError:
        print('Invalid input')
        year = 0
    except Exception as e:
        print(e)

def queries_to_run(query):
    """ Combines all executable query functions
        Args:
            query(int)
        Returns: (function - uncalled)
            Chosen function name
    """
    queries = {
        0: popular_travel_times,
        1: popular_stations_and_trip,
        2: trip_duration,
        3: user_info
    }
    return queries.get(query, 'Invalid Item')

def filter_functions(filter_option):
    """ Combines all executable filter functions
        Args:
            filter_option(int)
        Returns: (function - uncalled)
            Chosen function name
    """
    filters = {
        0: get_top_rows,
        1: filter_by_user_type,
        2: filter_by_birth_year,
        3: filter_by_gender
    }
    return filters.get(filter_option, 'Invalid Item')

def main():
    dataframe = load_data(city)
    city_data = filtered_data(dataframe)

    while True:

        loader()

        available_queries = {0: 'Popular Travel Times', 1: 'Popular Stations & Trips', 2: 'Trip Duration', 3: 'User Info'}
        available_filters = {0: 'Get Top Rows', 1: 'Filter By User Type', 2: 'FIlter By Birth Year', 3: 'Filter By Gender'}

        try:
            users_choice = ''
            while users_choice == '':
                print('What will you like to do?')
                print('0 ==> Peak the database\n1 ==> Query the database \n2 ==> Quit')
                users_choice = int(input('Enter based on the choices listed above: '))

            if users_choice == 0:
                print(' ')
                print(' \nYou chose to: Peek {}\'s database.'.format(CITIES[city.upper()][:-4].upper()))
                section_break()
                print('\nWhat query would you like to run?\n  ')
                for i, item in available_filters.items():
                    print('{} ==> {}'.format(i, item))
                query_choice = int(input('Enter based on the choices listed above: '))
                loader()

                print('{}\n '.format(available_filters.get(query_choice, 'Invalid Input')))
                print(filter_functions(query_choice)(city_data))
                calculate_execution_time()
                delay(1)
                section_break()
                print(' \n ')
                users_choice = ''

            if users_choice == 1:
                loader()
                print('You chose to: Query {}\'s database.'.format(CITIES[city.upper()][:-4].upper()))
                section_break()
                print('\nWhat query would you like to run?\n  ')
                for i, item in available_queries.items():
                    print('{} ==> {}'.format(i, item))
                query_choice = int(input('Enter based on the choices listed above: '))
                loader()
                print('{}\n '.format(available_queries.get(query_choice, 'Invalid Input')))
                print(queries_to_run(query_choice)(city_data))
                calculate_execution_time()
                delay(1)
                section_break()
                print(' \n ')
                users_choice = ''

            if users_choice == 2:
                print(' \nThank you for exploring Bikeshare\'s database!\n ')
                return
            else:
                users_choice = ''
        except ValueError:
            print('Invalid Input')
            # restart
            users_choice = ''

        except Exception as e:
            print(e)
            return;

    return users_choice;

if __name__ == "__main__":
	main()
