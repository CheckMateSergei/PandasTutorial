import pandas as pd
import numpy as np

unem_county = pd.read_csv('datasets/output.csv')
df = pd.read_csv('datasets/Minimum Wage Data.csv')

act_min_wage = pd.DataFrame()

# loop through the grouped states and store dataframes in act_min_wage variable
for name, group in df.groupby('State'):
    if act_min_wage.empty:
        act_min_wage = group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018': name})
    else:
        act_min_wage = act_min_wage.join(group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018': name}))

# drop columns with no data
act_min_wage = act_min_wage.replace(0, np.NaN).dropna(axis=1)

# function for getting minimum wage from dataframe df, returns the minimum wage
# for specified year or an exception occurs and we return np.NaN
def get_min_wage(year, state):
    try:
        return act_min_wage.loc[year][state]
    except:
        return np.NaN

# adds a column for minimum wage by state, calls the get_min_wage function
# with the parameters year and state in the unem_county dataframe
unem_county['min_wage'] = list(map(get_min_wage, unem_county['Year'],
                              unem_county['State']))

# load the presedential election data into new dataframe
pres16 = pd.read_csv('datasets/pres16results.csv')

# filter the unem_county dataframe to just february 2015
county_2015 = unem_county.copy()[(unem_county['Year'] == 2015) & (unem_county['Month'] == 'February')]

# load abbreviation data and convert to dictionary
state_abbv = pd.read_csv('datasets/abbreviations.csv', index_col = 0)
state_abbv = state_abbv[['Postal Code']]
state_abbv_dict = state_abbv[['Postal Code']].to_dict()
state_abbv_dict['Postal Code']['Federal (FLSA)'] = 'FLSA'
state_abbv_dict['Postal Code']['Guam'] = 'GU'
state_abbv_dict['Postal Code']['Puerto Rico'] = 'PR'

# Change the state names in 'State' column to state abbrevations
county_2015['State'] = county_2015['State'].map(state_abbv_dict['Postal Code'])
# Change the column names in pres16 to match the county_2015 dataframe
pres16.rename(columns = {'county': 'County', 'st': 'State'}, inplace = True)

pres16['County'] = pres16['County'].astype(str)

# Change the indices for county_2015 and pres16 to a double index or
# county/state
for df in [county_2015, pres16]:
    df.set_index(['County', 'State'], inplace = True)

# drop year column from county_2015
del(county_2015['Year'])
del(county_2015['Month'])
# isolate the rows with donald trump in candidate column
pres16 = pres16[pres16['cand'] == 'Donald Trump']
# isolate the percentages of voters who voted for donald trump by state
pres16 = pres16[['pct']]
pres16.dropna(inplace = True)

# Merge the county_2015 data with the presedential election data into one
# single dataframe all_together
all_together = pd.merge(county_2015, pres16, left_index=True, right_index=True)
all_together.dropna(inplace = True)

print(all_together.head())
print("\nCorrelation: ")
print(all_together.corr())
print("\nCovariance: ")
print(all_together.cov())
# print(unem_county.head())
# test function get_min_wage
# print(get_min_wage(2012, 'Colorado'))
# print(act_min_wage.head())
