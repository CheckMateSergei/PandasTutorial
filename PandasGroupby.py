import pandas as pd
import numpy as np

# read the csv with unclean data to dataframe
df = pd.read_csv('datasets/Minimum Wage Data.csv')
# print(df.head())

# convert the unclean data back to a csv with latin encoding
# df.to_csv('datasets/minwage.csv', encoding='latin-1')
# read the new properly encoded csv back into dataframe object
# df = pd.read_csv('datasets/minwage.csv')

# groups the dataframe by state (ie alabama is one group)
gb = df.groupby('State')
# print(gb.head())
# gets the group alabama from the grouped object and indexes it by year
# "setting the index" is basically choosing which column we use to
# index the rows of the dataframe. Here in the alabama group we choose to
# index by the year the data was taken
# print(gb.get_group('Alabama').set_index('Year').head())

# creates an empty dataframe
act_min_wage = pd.DataFrame()

# name is the index (state) of the group and group is the actual
# dataframe corresponding to the individual groups (states)
for name, group in df.groupby('State'):
    # if actual min wage is empty
    if act_min_wage.empty:
        # here we add content to our empty dataframe, we set the content
        # to be the states group and set the index to year, the '[]' brackets
        # indicaate a column of the df object and we rename this column to the
        # name of the state the group is reffering to
        act_min_wage = group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018': name})
    # else we join the new dataframe to our current actual min wage frame
    else:
        act_min_wage = act_min_wage.join(group.set_index('Year')[['Low.2018']].rename(columns={'Low.2018': name}))

# data that is giving us an issue, the issue is where we dont have data for
# some of the states in the dataframe
issue_df = df[df['Low.2018'] == 0]

# print(act_min_wage.describe())
# print(act_min_wage.head())
print(act_min_wage.corr().head())
# print(df.head())
# print(issue_df.head())
# print(issue_df['State'].unique())

# replace all the 0's in the act_min_wage dataframe with NaN's, then we
# can use dropna() to remove the violating entries, axis=1 says to drop the
# offending COLUMNS, so we will remove the offending state completely
# act_min_wage's columns are organized by state
# note: axis=0 would be the row
act_min_wage = act_min_wage.replace(0, np.NaN).dropna(axis=1)
print(act_min_wage.head())
print(act_min_wage.corr().head())
