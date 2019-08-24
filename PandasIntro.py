#! /usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plot

df = pd.read_csv("avocado.csv")

#print(df.head(3))
#print(df["AveragePrice"].head())
albany_df = df[ df['region'] == 'Albany' ]

#print(albany_df.head())

albany_df.set_index('Date', inplace=True, drop=True)
print(albany_df.head())

plot.imshow(albany_df['AveragePrice'])
plot.show()
