import pandas as pd
import numpy as np
import sklearn
from sklearn import svm, preprocessing

df = pd.read_csv('datasets/diamonds.csv', index_col=0)

# dictionaries giving numerical values to diamond attributes
cut_class_dict = {"Fair": 1, "Good": 2, "Very Good": 3, "Premium": 4, "Ideal": 5}
clarity_dict = {"I3": 1, "I2": 2, "I1": 3, "SI2": 4, "SI1": 5, "VS2": 6, "VS1": 7, "VVS2": 8, "VVS1": 9, "IF": 10, "FL": 11}
color_dict = {"J": 1,"I": 2,"H": 3,"G": 4,"F": 5,"E": 6,"D": 7}

# use map() function to map the row labels for the 'cut', 'clarity' and 'color'
# columns to those defined in the dictionary above
df['cut'] = df['cut'].map(cut_class_dict)
df['clarity'] = df['clarity'].map(clarity_dict)
df['color'] = df['color'].map(color_dict)

# shuffles the dataset to avoid any biases
df = sklearn.utils.shuffle(df)

# drop the price column from the dataframe, note we are predicting the price so
# having the price included in the table would be 'cheating'
X = df.drop('price', axis=1).values
# STANDARD NORMAL: computes the sample means and standard deviations of the
# data in the rows and then standardizes the data (ie: turns it into a standard
# normal distribution)
X = preprocessing.scale(X)
y = df['price'].values

test_size = 200

# use this data to train the model (last 200 rows of data)
X_train = X[:-test_size]
y_train = y[:-test_size]
# use this data to test against the trained model
X_test = X[-test_size:]
y_test = y[-test_size:]

# define the classifier
clf = svm.SVR(kernel='linear')
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))
# print out the models prediction and the actual price
for X, y in zip(X_test, y_test):
    print(f"Model: {clf.predict([X])[0]}, Actual: {y}")

# define the classifier
clf = svm.SVR(kernel='linear')
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))
# print out the models prediction and the actual price
for X, y in zip(X_test, y_test):
    print(f"Model: {clf.predict([X])[0]}, Actual: {y}")


# print(X)
# print(df.head())
