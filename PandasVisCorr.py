import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

df = pd.read_csv('datasets/Minimum Wage Data.csv')
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

act_min_wage = act_min_wage.replace(0, np.NaN).dropna(axis=1)
min_wage_corr = act_min_wage.corr()

# parses the website and returns a list of dataframes
dfs = pd.read_html('https://www.infoplease.com/us/postal-information/state-abbreviations-and-state-postal-codes')
# create a dataframe for the state abbreveations from the web link above
state_abbv = dfs[0]  # stored in the first index of the dataframe list
# save this information to a csv
state_abbv.to_csv('datasets/abbreviations.csv', index=False)
# reload with states as indices
state_abbv = pd.read_csv('datasets/abbreviations.csv', index_col=0)

# create a dictionary with the abbreviations
abbv_dict = state_abbv[['Postal Code']].to_dict()
abbv_dict['Postal Code']['Federal (FLSA)'] = 'FLSA'
abbv_dict['Postal Code']['Guam'] = 'GU'
abbv_dict['Postal Code']['Puerto Rico'] = 'PR'

# set new labels list
labels = [abbv_dict['Postal Code'][c] for c in min_wage_corr.columns]

# changes the size of the plot
fig = plot.figure(figsize=(12, 12))
# creates one graph
ax = fig.add_subplot(111)
# displays the dataframe as a matrix, changes the colouring to RYG
ax.matshow(min_wage_corr, cmap=plot.cm.RdYlGn)
# tell matplotlib to show all of the labels
ax.set_yticks(np.arange(len(labels)))
ax.set_xticks(np.arange(len(labels)))
# changes the labels on the axes as defined in labels
ax.set_yticklabels(labels)
ax.set_xticklabels(labels)

# print(labels)
# print(min_wage_corr.head())
plot.show()
