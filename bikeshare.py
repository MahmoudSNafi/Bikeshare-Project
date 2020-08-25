import time
import pandas as pd
import numpy as np

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
    print("Hello! Let's explore some US bikeshare data!\n")
    while True:
        city=input("Which city you want to know about? chicago, new york city or washington? ").lower()

        month=input("which month between januaray and june you want to filter by? insert 'all' for no filter: ").lower()

        day=input("which weekday you want to filter by? insert 'all' for no filter: ").lower()

        _valid_cities=['chicago', 'new york city','washington']
        _valid_months=['january','february','march''april','may','June','june','all']
        _valid_days=['saturday','sunday','monday','tuesday','wednesday','thursday','friday','all']

        if city in _valid_cities and month in _valid_months and day in _valid_days:
            break
        else:
            print('\nInvalid inputs, Please insert them again correctly.\n')
            continue

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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day']=df['Start Time'].dt.weekday_name
    df['hour']=df['Start Time'].dt.hour

    if month !='all':
        months=['january', 'february', 'march', 'april', 'may', 'june']
        month=months.index(month)+1
        df=df[df['month']==month]

    if day !='all':
        df=df[df['day']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months=['january', 'february', 'march', 'april', 'may', 'june']

    time_stats_df=pd.DataFrame({'Time Stats':[months[df['month'].mode()[0]-1],df['day'].mode()[0],df['hour'].mode()[0]]},
                               index=['Most Common Month','Most Common Weekday','Most Common Hour'])
    print(time_stats_df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['start-end-stations']=df['Start Station']+' --> '+df['End Station']

    popular_stations_df=pd.DataFrame({'Popular Stations and Trips':
                                     [df['Start Station'].mode()[0],df['End Station'].mode()[0],df['start-end-stations'].mode()[0]]},
                                     index=['Most Common Start Station','Most Common End Station','Most Common Trip Path'])
    print(popular_stations_df)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration=df['Trip Duration'].sum()
    avg_duration=df['Trip Duration'].mean()

    duration_df=pd.DataFrame({'Duration in seconds':[total_duration,avg_duration],
                              'Duration in minutes':[total_duration/60,avg_duration/60],
                              'Duration in hours':[total_duration/3600,avg_duration/3600]},
                             index=['Total','Average'])
    print(duration_df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("The distribution of user types as follows:")
    print(pd.DataFrame(df['User Type'].value_counts()))

    if city !='washington':
        print("\nThe distribution of user gender as follows:")
        print(pd.DataFrame(df['Gender'].value_counts()))

    if city !='washington':
        print("\nUser Birth year states as follows:")
        birth_year_stats=pd.DataFrame({'Birth year stats':
                                       [int(df['Birth Year'].min()),int(df['Birth Year'].max()),int(df['Birth Year'].mode()[0])]},
                                      index=['Earliest year of birth','Most recent Year of birth','Most common year of birth'])
        print(birth_year_stats)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    ques=input("\nDo you want to see how your raw data looks like, yes or no? ").lower()
    counter=0
    if ques=='yes':
        print(df.iloc[counter:counter+5])
        while True:
            another_ques=input("\nDo you want to see another 5 rows, yes or no? ").lower()
            if another_ques=='yes':
                counter+=5
                print(df.iloc[counter:counter+5])
            elif another_ques=='no':
                break
            else:
                print("\nInvalid input, please insert yes or no")
                continue
    elif ques=='no':
        pass
    else:
        print("\nInvalid input, please insert yes or no")
        raw_data(df)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
