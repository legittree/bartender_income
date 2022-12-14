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

def new_job_getter():

    """ Get what day's I'd still work at cope, and find out hours per week, pay, and weeks per year working """

    print('-_'*80 + '\nEVERYTHING IS PRETAX!!')

    pay_type = input('Is the new job income hourly or annual:\n').strip().lower()
    while pay_type not in ['hourly', 'annual']:
        pay_type = input('That wasn\'t right. Try again.\n').strip().lower()
    if pay_type == 'hourly':
        new_pay = input('New job\'s hourly pay:\n').strip().lower()
        while new_pay.isnumeric() == False:
            new_pay = input('That wasn\'t right. Try again.\n').strip().lower()
    else:
        new_pay = input('New job\'s annual pay:\n').strip().lower()
        while new_pay.isnumeric() == False:
            new_pay = input('That wasn\'t right. Try again.\n').strip().lower()

    new_hours = input('New job\'s weekly hours:\n').strip().lower()
    while new_hours.isnumeric() == False:
        new_hours = input('That wasn\'t right. Try again\n').strip().lower()
    new_weeks_per_year = input('New job\'s weeks worked in a year:\n').strip().lower()
    while new_weeks_per_year.isnumeric() == False:
        new_weeks_per_year = input('That wasn\'t right. Try again\n').strip().lower()

    cope_shifts = input('Which days will you work at copehouse? Use full day name, or keep blank to use no cope days:\n').strip().lower().split(' ')
    check = False
    while check == False:
        for i in range(len(cope_shifts)):
            print(i, len(cope_shifts))
            if (cope_shifts[i] not in days) and (cope_shifts[i] != ''):
                print('error found')
                break
            elif i == (len(cope_shifts) - 1):
                print('end of list')
                check = True
        if check == False:
            cope_shifts = input('That wasn\'t right. Try again\n').strip().lower().split(' ')

    # Annual pay needs to be converted to hourly based on shits and hours worked
    if pay_type == 'annual':
        new_pay = int(new_pay)/(int(new_hours) * int(new_weeks_per_year))

    return new_pay, new_hours, new_weeks_per_year, cope_shifts


def income_filter_getter():
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
    data = pd.read_excel('income_sheet.xlsx')

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
    data['Hourly'] = (data['Total Income']/data['Hours']).round(decimals = 2)
    data['Take Home'] = (data['Total Income'] - (data['Total Income'] * tax_percent)).round(decimals = 2)
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

def useful_checks(data, checks):

    """ Getting DFs within each pay period """

    useful_checks = checks[['Pay Date', 'Paycheck', 'Total Pay', 'Taxation', 'Total Hours', 'Overtime Hours', 'Regular Hours', 'Cash Claim']]
    useful_checks[['Cash Tips', 'Shifts']] = None
    combo = None

    # Combine shift and paycheck data to make the useful_checks data
    for i in range(len(checks.values)):
        
        # Selects shifts within each pay period (by day of the year only, needs improvement)
        temp = data[(data['DoY'] > checks['Start DoY'][i]) & (data['DoY'] < checks['End DoY'][i])]
        
        # adds Cash Tips sum to the end of each paycheck
        useful_checks['Cash Tips'][i] = temp['Cash Tips'].sum()
        
        # Count Shifts and add it as column
        useful_checks['Shifts'][i] = temp['Date'].count()

        # Make a DF of all the shift data within the checks data
        combo = pd.concat([combo, temp])

        i += 1

    ##### THIS WRITES THE NEW USEFUL_CHECKS EXCEL SHEET 
    useful_checks.to_excel('useful_checks.xlsx')

    return useful_checks, combo

def DoW_breakdown(data, useful_checks, combo):

    # Find total income per DoW

    mean_hours = data['Hours'].groupby(data['DoW']).mean()
    mean_tips = combo['Cash Tips'].groupby(combo['DoW']).mean()
    mean_income = (mean_tips + (mean_hours * 15)).round(decimals = 2)

    means = pd.concat([mean_income, mean_hours], axis = 1)
    means.columns = ['Income', 'Hours']
    means.index = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    return means

def income_calculator(new_pay, new_hours, new_weeks_per_year, cope_shifts, means):

    """ This uses my mean income and new job info to figure how much I'd make """

    current_weekly_income = means['Income'].filter(items = ['tuesday', 'wednesday', 'friday', 'saturday', 'sunday']).sum()
    current_annual_income = current_weekly_income * 52
    current_weekly_hours = means['Hours'].filter(items = ['tuesday', 'wednesday', 'friday', 'saturday', 'sunday']).sum()
    current_annual_hours = current_weekly_hours * 52

    new_pay = int(new_pay)
    new_hours = int(new_hours)
    new_weeks_per_year = int(new_weeks_per_year)

    cope_weekly_income = means['Income'].filter(items = cope_shifts).sum()
    cope_annual_income = cope_weekly_income * 52
    cope_weekly_hours = means['Hours'].filter(items = cope_shifts).sum()
    cope_annual_hours = cope_weekly_hours * 52


    new_weekly_income = new_pay * new_hours
    new_annual_income = new_weekly_income * new_weeks_per_year
    new_weekly_hours = new_hours
    new_annual_hours = new_hours * new_weeks_per_year

    total_weekly = cope_weekly_income + new_weekly_income
    total_annual = cope_annual_income + new_annual_income
    total_weekly_hours = new_weekly_hours + cope_weekly_hours
    total_annual_hours = new_annual_hours + cope_annual_hours

    print('\n')
    print('#'*80)
    print('\n')

    print('*** WHAT I MAKE NOW ***\n')
    print('Current weekly: $', current_weekly_income)
    print('Current annual: $', current_annual_income.round(decimals = 2))
    print('Current weekly hours: ', current_weekly_hours.round(decimals = 2))
    print('Current annual hours: ', current_annual_hours.round(decimals = 2))

    print('CURRENT AVERAGE HOURLY: $', (current_annual_income/current_annual_hours).round(decimals = 2))

    print('\n')
    print('#'*80)
    print('\n')

    print('*** WHAT I WOULD MAKE ***\n')
    print('New weekly: $', total_weekly.round(decimals = 2))
    print('New annual: $', total_annual.round(decimals = 2))
    print('New weekly hours: ', total_weekly_hours.round(decimals = 2))
    print('New annual hours: ', total_annual_hours.round(decimals = 2))

    print('NEW AVERAGE HOURLY: $', (total_annual/total_annual_hours).round(decimals = 2))

    print('\n')
    print('#'*80)
    print('\n')

def main():
    data, checks = reader()
    new_pay, new_hours, new_weeks_per_year, cope_shifts = new_job_getter()
    format_income_sheet(data)
    formate_paycheck_info(checks)
    pay_period, check_shifts = useful_checks(data, checks)
    means = DoW_breakdown(data, pay_period, check_shifts)
    income_calculator(new_pay, new_hours, new_weeks_per_year, cope_shifts, means)

if __name__ == '__main__':
    main()

# '20', '40', '37', ['friday', 'saturday'] school job
# '40', '40', '52', ['friday', 'saturday'] great job
# '29', '40', '45', ['friday', 'saturday', 'sunday'] mandy's job












"""
Info I want:

average total income by DoW
    total pay period hours + (Delta Hours / # of shifts in pay period) + Cash Tips
    Won't be perfect but it'll be closer to my DoW income than without redistributing the extra hours

Maybe do the whole thing by month, find the averages of the pay period and extrapolate
to the month

Calculate take home and pretax income dependant on what shifts I'd take


"""
















