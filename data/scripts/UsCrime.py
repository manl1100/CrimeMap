# __author__ = 'manuelsanchez'


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math


def read():

    # Load geoid and name
    geoid_df = pd.read_csv("../crime/Gaz_counties_national.txt", sep="\t", usecols=['USPS', 'GEOID', 'NAME'])
    geoid_df['County'] = [input.replace(' County','') for input in geoid_df.NAME.values]
    geoid_df = geoid_df.drop(geoid_df.columns[[2]], axis=1)

    # Load state data
    states = pd.read_csv("../crime/state_table.csv", usecols=['name', 'abbreviation'])
    states['name'] = states['name'].apply(lambda x: x.upper())
    states.columns = ['State', 'USPS']
    state_df = pd.merge(geoid_df, states, on='USPS')

    # Load crime data by county
    crime_df = pd.read_excel('../crime/table-10.xls')
    crime_df['State'] = crime_df['State'].fillna(method='pad')
    crime_df['State'] = crime_df['State'].apply(lambda x: x[:x.index('-') - 1])
    crime_df = crime_df.drop(crime_df.columns[[3,4,5,6,7,8,9,10,11,12]], axis=1)
    crime_state = pd.merge(state_df, crime_df, on=['State', 'County'])

    # 2014 Population
    county_pop = pd.read_csv("../crime/CO-EST2014-alldata.csv", usecols=['STNAME', 'CTYNAME', 'POPESTIMATE2014'])
    county_pop.columns = ['State', 'County', 'Population']
    county_pop['County'] = [input.replace(' County','') for input in county_pop.County.values]
    county_pop['State'] = county_pop['State'].apply(lambda x: x.upper())

    # Combined sources
    complete_df = pd.merge(crime_state, county_pop, on=['County', 'State'])
    complete_df['CRIME_RATE'] = complete_df['Violent_crime']/complete_df['Population'] * 100000
    complete_df = complete_df.drop(complete_df.columns[[0, 2, 3, 4, 5]], axis=1)

    # Common stats
    # print complete_df['CRIME_RATE'].sort_values()
    # print "Mean: " + str(complete_df['CRIME_RATE'].mean())
    # print "Median " + str(complete_df['CRIME_RATE'].median())
    # print "Variance: " + str(complete_df['CRIME_RATE'].var())
    # print "Max: " + str(complete_df['CRIME_RATE'].max())
    # print "Max: " + str(complete_df['GEOID'].count())
    # print "Count: " + str(complete_df['CRIME_RATE'].value_counts())

    # Bar chart
    # gaussian_numbers = complete_df['CRIME_RATE'].values
    # plt.hist(gaussian_numbers)
    # plt.title("Gaussian Histogram")
    # plt.xlabel("Value")
    # plt.ylabel("Frequency")
    # plt.show()

    # Output file
    complete_df.to_csv("../crime/geoid_crimestat.csv", '\t')

    # Different data sources
    # Load crime data
    crime2_df = pd.read_excel('../crime/CRM03.xls')

    # Load population data
    pop2_df = pd.read_excel('../crime/POP03.xls')

    combined2 = pd.merge(crime2_df, pop2_df, on='STCOU')
    combined2['CRIME_STAT'] = (combined2['CRM250208D'] / combined2['POP665209D']) * 100000
    # print combined2[['Areaname', 'STCOU', 'CRM250208D', 'POP665209D', 'CRIME_STAT']]
    # print combined2['CRIME_STAT'] / combined2.iloc[0]['CRIME_STAT']
    print combined2['CRIME_STAT'].max()
    print combined2['CRIME_STAT'].mean()
    print combined2['CRIME_STAT'].median()
    print combined2.iloc[0]['CRIME_STAT']

    # Using US stat
    combined2['CRIME_STAT_AVG'] = combined2['CRIME_STAT'] / combined2.iloc[0]['CRIME_STAT']
    print combined2['CRIME_STAT_AVG']

    combined2[['STCOU', 'CRIME_STAT_AVG']].to_csv('../crime/test.csv', '\t')

read()
