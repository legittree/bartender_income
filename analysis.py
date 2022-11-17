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

tax_percent = 0.273625908

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

def apply_filter(data, month, day):

    # Empty DF to add in filtered datapoints
    filteredDF = pd.DataFrame([])

    # Create new DataFrame filtered by month
    if month == 'all':
        filteredDF = data[data.Month.isin(months[month])]
    else:
        filteredDF = data[data['Month'] == months[month]]

    # Create new DataFrame filtered by month and day
    if day == 'all':
        filteredDF = filteredDF[filteredDF.DoW.isin(days[day])]
    else:
        filteredDF = filteredDF[filteredDF['DoW'] == days[day]]

    return filteredDF

def format(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['DoW'] = pd.DatetimeIndex(data['Date']).dayofweek
    data['Month'] = pd.DatetimeIndex(data['Date']).month
    data['Week'] = pd.DatetimeIndex(data['Date']).week
    data['Hourly'] = data['Total Income']/data['Hours']
    data['Take Home'] = data['Total Income'] - (data['Total Income'] * tax_percent)
    data['Tax'] = data['Total Income'] - data['Take Home']

def display_info(data):

    print('\n' + '-'*80)
    print('Hourly:', data['Hourly'].mean())
    print('Total Cash Tips:', data['Cash Tips'].sum())
    print('Total Hours Worked:', data['Hours'].sum())
    print('')
    print('Total Take Home Income:', data['Take Home'].sum())
    print('Total Income:', data['Total Income'].sum())

    # I could conditionally split this off if there is no month filter
    print('Average Monthly Take Home:', data.groupby(['Month']).sum()['Take Home'].mean())
    print('Average Tax Per Month:', data.groupby(['Month']).sum()['Tax'].mean())
    print('Average Pre Tax Income Per Month:', data.groupby(['Month']).sum()['Total Income'].mean())
    print('-'*80, '\n')
    print('Sums by month:\n', data.groupby(['Month']).sum()[['Cash Tips', 'Hours', 'Total Income', 'Take Home', 'Tax']])
    print(data.groupby(['Week']).mean()[['Cash Tips', 'Take Home']].sort_values(by = ['Cash Tips'], ascending = False))

def main():
    data = reader()
    #month, day = filter_getter()
    format(data)
    data = apply_filter(data, 'all', 'all')
    display_info(data)

if __name__ == '__main__':
    main()
