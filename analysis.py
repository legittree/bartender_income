import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn' rids the warning while assigning checks take home tips

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
    data = pd.read_csv('income_sheet.csv')

    checks = pd.read_excel('paycheck_info.xlsx')

    return data, checks

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

def format_income_sheet(data):

    data['Date'] = pd.to_datetime(data['Date'])
    data['DoW'] = pd.DatetimeIndex(data['Date']).dayofweek
    data['DoY'] = pd.DatetimeIndex(data['Date']).dayofyear
    data['Month'] = pd.DatetimeIndex(data['Date']).month
    # isocalendar() is a python function being applied to a pandas series
    data['Week'] = data['Date'].dt.isocalendar().week
    data['Hourly'] = data['Total Income']/data['Hours']
    data['Take Home'] = data['Total Income'] - (data['Total Income'] * tax_percent)
    data['Tax'] = data['Total Income'] - data['Take Home']

def formate_paycheck_info(checks):

    checks['Period Start'] = pd.to_datetime(checks['Period Start'])
    checks['Period End'] = pd.to_datetime(checks['Period End'])
    checks['Start DoY'] = pd.DatetimeIndex(checks['Period Start']).dayofyear
    checks['End DoY'] = pd.DatetimeIndex(checks['Period End']).dayofyear

    return

def display_info(data):

    print('\n' + '-'*80)
    print('Hourly:', data['Hourly'].mean())
    print('Total Cash Tips:', data['Cash Tips'].sum())
    print('Total Hours Worked:', data['Hours'].sum())
    print('')
    print('Total Take Home Income:', data['Take Home'].sum())
    print('Total Income:', data['Total Income'].sum())

    # I could conditionally split this off if there is no month filter
    print('Average Monthly Take Home:', data.groupby(['Month']).sum(numeric_only = True)['Take Home'].mean())
    print('Average Monthly Cash Tips:', data.groupby(['Month']).sum(numeric_only = True)['Cash Tips'].mean())
    print('Average Tax Per Month:', data.groupby(['Month']).sum(numeric_only = True)['Tax'].mean())
    print('Average Pre Tax Income Per Month:', data.groupby(['Month']).sum(numeric_only = True)['Total Income'].mean())
    print('-'*80, '\n')
    print('Sums by month:\n', data.groupby(['Month']).sum(numeric_only = True)[['Cash Tips', 'Hours', 'Total Income', 'Take Home', 'Tax']])
    print('Average Weekly Hours:', data.groupby(['Week']).sum(numeric_only = True)['Hours'].mean())
    print('Average Take Home Weekly Income:', data.groupby(['Week']).sum(numeric_only = True)['Take Home'].mean())
    print('Average Total Weekly Income:', data.groupby(['Week']).sum(numeric_only = True)['Total Income'].mean())
    print('Day of Week Averages:\n', data.groupby(['DoW']).mean(numeric_only = True)[['Cash Tips', 'Hours', 'Total Income', 'Hourly', 'Take Home']])
    print(data.groupby(['Week']).mean(numeric_only = True)[['Cash Tips', 'Take Home']].sort_values(by = ['Cash Tips'], ascending = False))

def made_money(data, checks):

    """ Getting DFs within each pay period """

    combo = pd.DataFrame([])
    checks['Take Home Tips'] = pd.Series([], dtype = 'float64')

    for i in range(len(checks.values)):
        # Selects shifts within each pay period (by day of the year only, needs improvement)
        temp = data[(data['DoY'] > checks['Start DoY'][i]) & (data['DoY'] < checks['End DoY'][i])]
        # adds Cash Tips sum to the end of each paycheck
        checks['Take Home Tips'].iloc[[i]] = temp.sum(numeric_only = True)['Cash Tips']
        combo = pd.concat([temp, combo])
        i += 1
        print('TEMP\n', temp)

    useful_checks = checks[['Pay Date', 'Paycheck', 'Cash Tips', 'Total Pay', 'Taxation', 'Total Hours', 'Overtime Hours', 'Regular Hours', 'Take Home Tips']]
    print(useful_checks)
    print(combo)

    return

def main():
    data, checks = reader()
    #month, day = filter_getter()
    format_income_sheet(data)
    #data = apply_filter(data, 'all', 'all')
    #display_info(data)
    formate_paycheck_info(checks)
    made_money(data, checks)

if __name__ == '__main__':
    main()
