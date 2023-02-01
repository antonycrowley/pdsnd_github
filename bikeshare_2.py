import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = dict(zip(range(0, 12+1), calendar.month_name))
MONTHS[0] = 'all'
DAYS = dict(zip(range(0, 6+1), calendar.day_name))
DAYS[7] = 'all'

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "0" to apply no month filter
        (int) day - name of the day of week to filter by, or "0" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter city name on which you want to review data: ').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Please enter a valid selction. chicago, new york city or washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = int(input('Please enter month with integer (1 to 12) or 0 for all: '))
            if int(month) in range(1,12+1):
                break
            elif month == 0:
                print('Selected all months')
                break
            else:
                print('Please enter a valid selction. Enter a month number from 1 to 12,')
                print('or 0 to select all months.')
        except ValueError:
            print('Please enter a valid option. Selection must be an integer from 0 to 12.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = int(input('Please enter a day with integer (0 Monday... 6 Sunday) or 7 for all: '))
            if day in range(0,6+1):
                break
            elif day == 7:
                print('Selected all days.')
                break
            else:
                print('Enter a day of the week number from 0 to 6 or 7 to select all.')
        except ValueError:
            print('Selection must be an integer from 0 to 7.')

    print(f'Selected: {city}, {MONTHS[month]} and {DAYS[day]}')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "0" to apply no month filter
        (int) day - name of the day of week to filter by, or "7" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Dataframe date columns datatype conversion.
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Station column datatype conversion to string
    df['Start Station'] = df['Start Station'].astype(str)
    df['End Station'] = df['End Station'].astype(str)

    # Birth year column conversion to int
    try:
        df['Birth Year'] = df['Birth Year'].astype('Int64', errors='ignore')
    except KeyError:
        pass # Do nothing, added this to resolve expected indented block

    # Creation of useful columns
    df['Start hour'] = df['Start Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.dayofweek
    df['Station Combination'] = df['Start Station'] + " AND " + df['End Station']

    # Apply month filter
    if month != 0:
        df = df[df['Month'] == month]

    # Apply day filter
    if day != 7:
        df = df[df['Day'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_number = df['Month'].mode()[0]
    print(str('Most common month is: {}.').format( MONTHS[month_number] ))

    # display the most common day of week
    dow_number = df['Day'].mode()[0] # 0 is Monday in pandas, 6 is Sunday in pandas
    print(str('Most common day of the week is: {}.').format( DAYS[dow_number] ))

    # display the most common start hour
    print(str('Most common hour of the day is: {}.').format( df['Start hour'].mode()[0] ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(str('Most common used start station is: {}.').format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print(str('Most common used end station is: {}.').format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    st_comb_mode = df['Station Combination'].mode()[0]
    print(str("The most frequent start and end station combination is: {}.").format(st_comb_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    statement = helper_seconds_to_statement(int(df['Trip Duration'].sum()))
    print(f'Total trip duration is: {statement}')

    # display mean travel time
    statement = helper_seconds_to_statement(int(df['Trip Duration'].mean()))
    print(f'Mean travel time is: {statement}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type count:')
    print(df['User Type'].value_counts())
    print('')

    # Display counts of gender
    try:
        print(df['Gender'].value_counts())
        print('')
    except KeyError:
        print('Birth years not available.')

    # Display earliest, most recent, and most common year of birth
    try:
        print(str('Earliest year of bith: {}').format( int(df['Birth Year'].min())) )
        print(str('Most recent year of birth: {}').format( int(df['Birth Year'].max()) ))
        print(str('Most common year of birth: {}').format(int(df['Birth Year'].mode())))
    except KeyError:
        print('Gender data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def helper_seconds_to_statement(seconds):
    """
    Converts a number in seconds to an understandable statement up to days:
    Args:
        (int) seconds
    Returns:
        (str) Ex: 2 days, 2 hours, 2 minutes, 2 seconds.
    """
    remaining_seconds = seconds
    days = int(remaining_seconds / (60 * 60 * 24))
    remaining_seconds -= days * (60 * 60 * 24)
    hours = int(remaining_seconds / (60 * 60))
    remaining_seconds -= hours * (60* 60)
    minutes = int(remaining_seconds / 60)
    remaining_seconds -= minutes * 60
    seconds = remaining_seconds
    statement = ''
    if days != 0:
        statement += str(f'{days} days, ')
    if hours != 0:
        statement += str(f'{hours} hours, ')
    if minutes != 0:
        statement += str(f'{minutes} minutes, ')
    if seconds != 0:
        statement += str(f'{seconds} seconds.')

    return statement

def raw_data_visualization(df):
    """
    Asks user if wants to visualize raw data 5 lines at a time.

    Returns:
        (Dataframe) a datafame with 5 lines with the selected filters applied
    """
    # Drop useful added columns
    df = df.drop(['Start hour', 'Month', 'Day', 'Station Combination'], axis=1)

    # Renumber rows
    df.reset_index(inplace=True)

    # get user input for raw data visualization.
    i = 0
    while True:
        if i != 0:
            break
        answer = input('Do you want to visualize raw data? [yes/no]: ').lower()     #Quest loop 1
        if answer in ['yes', 'no']:                                                 #Ans Val 1
            if answer == 'yes':                                                     #Valid answ 1
                while True:
                    if i != 0:
                        answer = input('Do you want to see 5 more? [yes/no]: ').lower() #Q loop 2
                    if answer in ['yes', 'no'] or i == 0:                           #Ans val 2
                        if answer == 'yes':
                            temp_df = df.loc[ i*5 : (i+1)*5-1]
                            if not temp_df.empty:
                                print(temp_df)                                      #Valid ans 2
                                i += 1
                            else:
                                print('There is no more data to show.')
                                break
                            continue
                        elif answer == 'no':                                        #Exit loop 2
                            break
                    else:                                                           #inv ans 2
                        print('Please enter a valid selction. Options are yes or no.')
            else:                                                                   #Exit loop 1
                break
        else:                                                                       #Inv ans 1
            print('Please enter a valid selction. Options are yes or no.')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            raw_data_visualization(df)
        else:
            print('No results with filters applied. Try wider ones')
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart in ['yes', 'no']:
                if restart == 'yes':
                    break
                else:
                    exit()
            else:
                print('Please enter a valid selction. Enter yes or no.')


if __name__ == "__main__":
    main()
