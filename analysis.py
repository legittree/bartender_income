import numpy as np
import pandas as pd

months = {'january' : 1,
          'february' : 2,
          'march' : 3,
          'april' : 4,
          'may' : 5,
          'june' : 6,
          'july' : 7,
          'august' : 8,
          'september' : 9,
          'october' : 10,
          'november' : 11,
          'december' : 12,
          'all' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
          }

days = {'monday' : 0,
        'tuesday' : 1,
        'wednesday' : 2,
        'thursday' : 3,
        'friday' : 4,
        'saturday' : 5,
        'sunday' : 6,
        'all' : [0, 1, 2, 3, 4, 5, 6]
       }

def filter_getter():
    time_filter = input('Filter by time?\n').lower().strip()
    while time_filter not in ['yes', 'no']:
        time_filter = input('Let\'s try that again\n')
    if time_filter == 'yes':
        month = input('Which month? January - November or all\n')
        while month not in months:
            month = input('Let\'s try that again\n')
        day = input('which day of the week? or all?\n')
        while day not in days:
            day = input('Let\'s try that again\n')
    else:
        month = 'all'
        day = 'all'
    return month, day


def reader():
    reader = pd.read_csv('income_sheet.csv')
    data = pd.DataFrame(reader)
    return data

def format(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['DoW'] = pd.DatetimeIndex(data['Date']).dayofweek
    data['Month'] = pd.DatetimeIndex(data['Date']).month

def main():
    data = reader()
    month, day = filter_getter()
    print(month, day)
    format(data)
    print(data['Cash Tips'].sum())
    print(data['Hours'].sum())
    print(data['Total Income'].sum())
    print(data)


if __name__ == '__main__':
    main()
