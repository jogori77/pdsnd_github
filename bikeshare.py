#import relevant modules
import time
import pandas as pd
import numpy as np

#prepare city data dictionary to be able to load the right file after user input, also other useful dictionaries to convert data to more user friendly format later on
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_conv = {1:'January',
               2:'February',
               3:'March',
               4:'April',
               5:'May',
               6:'June'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. Make sure any combination of capitals and not capitals is handled correctly.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #prepare valid inputs lists and empty variables for user input validation
    city_list = ['chicago','new york','washington']
    filters_list = ['month','day','both','all']
    month_list = ['january','february','march','april','may','june']
    day_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    city = ''
    filters = ''
    month = ''
    day = ''
    #start user input
    print('\nHello! Let\'s explore some US bikeshare data!')
    #ask user for the city they would like to get the data for
    while city not in city_list: city = input('\nWould you like to see data for Chicago, New York, or Washington? ').lower()
    #ask user about what type of filtering would like to use
    while filters not in filters_list: filters = input('\nWould you like to filter the data by month, day, both or not at all? (for no filtering type: all) ').lower()
    #define month and day depending on the answer above
    if filters == 'all':  #if no filter is selected (i.e. all), then month and day variables need to be assigned to 'all'
        month = 'all'
        day = 'all'
    else:  #if a filter is selected (i.e. either month or day or both), then further info is requested for the filter selected and the other filter is set to 'all'
        if filters == 'month':
            while month not in month_list: month = input('\nWhich month? January, February, March, April, May or June? ').lower()
            day = 'all'
        if filters == 'day':
            while day not in day_list: day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ').lower()
            month = 'all'
        if filters == 'both':
            while month not in month_list: month = input('\nWhich month? January, February, March, April, May or June? ').lower()
            while day not in day_list: day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ').lower()
    #finish the function
    print('\n','-'*60)
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
    #load the file of the city the user inputs
    df = pd.read_csv(CITY_DATA[city])

    #convert the time to the datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #get the month and the weekday as new temp columns to allow the filtering
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month if this is what is requested by the user
    if month != 'all':
        #conversion to month numbers first as this is how it is in the file
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]  #actual filtering into the new filtered dataframe

    #filter by day if this is what is requested by the user
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]  #actual filtering into the new filtered dataframe

    return df  #finish the function


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n*** STATS ON MOST FREQUENT TIMES OF TRAVEL ***\n')
    start_time = time.time()

    # TO DO: display the most common month (also used the months_conv dictionary defined at the start to convert back to text month)
    print('  -> Most common month:',months_conv[common_month = df['month'].mode()[0]],'\n')

    # TO DO: display the most common day of week
    common_dow = df['day_of_week'].mode()[0]
    print('  -> Most common day of the week:',common_dow,'\n')

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print('  -> Most common start hour: '+str(df['start_hour'].mode()[0])+'h\n')
    #finish the function
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n*** MOST POPULAR STATIONS AND TRIPS ***\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('  -> Most commonly used start station:',common_start_station,'\n')

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('  -> Most commonly used end station:',common_end_station,'\n')

    # TO DO: display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station']+' - '+df['End Station']
    common_trip = df['trip'].mode()[0]
    print('  -> Most frequent combination of start station and end station trip:',common_trip,'\n')

    #finish the function
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n*** TRIP DURATION STATS***\n')
    start_time = time.time()

    # TO DO: display total travel time -> including a conversion to a more readable format
    total_travel_time = time.gmtime(df['Trip Duration'].sum())
    simple_ttt = time.strftime("%H:%M:%S",total_travel_time)
    print('  -> Total travel time from all users (HH:MM:SS):',simple_ttt,'\n')

    # TO DO: display mean travel time -> including a conversion to a more readable format
    mean_travel_time = time.gmtime(df['Trip Duration'].mean())
    simple_mtt = time.strftime("%H:%M:%S",mean_travel_time)
    print('  -> Mean travel time from all users (HH:MM:SS):',simple_mtt,'\n')

    #finish the function
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n*** BIKESHARE USERS STATS ***\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('  -> Count of user types:\n',user_types,'\n', sep='')

    # TO DO: Display counts of gender -> including a way to account for the fact that Washington doesn't have Gender data
    try:
        genders = df['Gender'].value_counts()
        print('  -> Count of gender types:\n',genders,'\n', sep='')
    except KeyError: print('  -> Count of user types: Sorry, no gender info for Washington\n')

    # TO DO: Display earliest, most recent, and most common year of birth -> including a way to account for the fact that Washington doesn't have birth year data
    try:
        earliest_by = int(df['Birth Year'].min())
        most_recent_by = int(df['Birth Year'].max())
        most_common_by = int(df['Birth Year'].mode()[0])
        print('  -> User\'s birth years: the earliest is {}, the most recent is {}, and most common is {}\n'.format(earliest_by,most_recent_by,most_common_by))
    except KeyError: print('  -> User\'s birth years: Sorry, no birth year info for Washington\n')

    #finish the function
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def show_raw(df):
    """Displays raw statistics
       Asks the user whether raw statistics have to be shown. In case they are, shows 5 rows at a time and keeps asking whether he/she wants to see the next 5.
    """
    df = df.drop(['start_hour','month','day_of_week','trip'], axis=1) #clean up the temp rows created to show some stats
    #make some float data nicer to read (also need to prepare for the case where 'Birth Data' column is not present in Washington)
    if 'Birth Year' in df.columns:
        columns = ['Trip Duration','Birth Year']
    else: columns = ['Trip Duration']
    df[columns]=df[columns].fillna(0.0).astype(int)
    #ask whether the user wants to see the raw data and then keep asking whether 5 more rows are needed
    if input('\nWould you like to see the raw data? (enter yes or no) => ').lower() == 'yes':
        print(df.iloc[0:5,1:])
        start = 5
        end = 10
        while input('\nWould you like to see 5 more rows? (enter y or n) => ').lower() == 'y':  #y or n (as opposed to yes or no) this time to be easier for the user to see more rows
            print(df.iloc[start:end,1:])
            start += 5
            end +=5


def main():
    while True:
        #load the relevant data to be used
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #run the different functions presenting interesting stats and also the raw data if requested by the user
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw(df)
        #see if the user wants to run another query or quit
        restart = input('\nWould you like to restart and input your preferences again? (enter yes or no) => ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
