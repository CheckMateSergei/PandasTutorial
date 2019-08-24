"""Begginner pandas tutorial. Creates a DataFrame, sorts and manipulates the data
    and then creates a graph to plot the moving average prices against other
    regions that have avocados for sale."""
#! /usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plot

df = pd.read_csv('avocado.csv') #creates a dataframe object and reads csv file

#the dataframe 'df' can be thought of as an array with various indices,
   # the 'type' index is a column in the csv file that contains information
   # on whether or not the avocado was organic.
df = df.copy()[df['type'] == 'organic'] #Copy only the rows with organic types
df['Date'] = pd.to_datetime(df['Date']) #Converts the 'Date' column to datetime objects
df.sort_values(by='Date', ascending=True, inplace=True)
print(df.head())

albany_df = df.copy()[df['region'] == 'Albany'] #Copies the dataframe 'df' where the region is albany

#If inplace=True, then a copy need not be created as the original dataframe will be changed
albany_df.set_index('Date', inplace = True) #Changes the main index to the 'Date' column

#Puts the dates (indices) into proper order
albany_df.sort_index(inplace = True)

#Creates a new pandas dataframe object
graph_df = pd.DataFrame()

#Loops through the individual unique regions. ie: it only loops once for each region
for region in df['region'].unique():
    print(region)
    #Copies the rows of df where the region is the current one looping through
    region_df = df.copy()[df['region']==region]
    #Reset the sorting index to date
    region_df.set_index('Date', inplace = True)
    #Resorts by date with new added rows
    region_df.sort_index(inplace = True)
    #Changes the value in the moving average column to a new rolling mean
    region_df[f'{region}_price25ma'] = region_df['AveragePrice'].rolling(25).mean()

    #If the graph dataframe is empty we add the rows with the new moving average
       # where the region matches the current iteration
    if graph_df.empty:
        graph_df = region_df[[f'{region}_price25ma']]
    #Otherwise join the other rows to the current dataframe object
    else:
        graph_df = graph_df.join(region_df[f'{region}_price25ma'])
#Remove the entries where no data is available
graph_df = graph_df.dropna()
#Plot the 8x5  graph without a legend
plt = graph_df.plot(figsize=(8,5), legend=False, title='Avocado Prices in \'Merica')
#Change x axis limits to match stupid video
plt.set_xlim(pd.to_datetime('2015-07'), pd.to_datetime('2018-04'))
#Shows the plot in a pop up window
plot.show()

