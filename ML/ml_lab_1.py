# -*- coding: utf-8 -*-
"""ml lab 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FsEhJSPT-3DNbbdIMuMb0zQK4kAZyUSR

Predict the price of the Uber ride from a given pickup point to the agreed drop-off location.
Perform following tasks:
1. Pre-process the dataset.
2. Identify outliers.
3. Check the correlation.
4. Implement linear regression and random forest regression models.
5. Evaluate the models and compare their respective scores like R2, RMSE, etc.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path="/content/drive/MyDrive/ml lab assignments/Copy of uber.csv"

df=pd.read_csv(path)

"""**Data Preprocessing**"""

df.head()

df1=df.drop(columns=['Unnamed: 0','key'],axis=1)
df1

df1.isnull().sum()

df1.pickup_datetime=pd.to_datetime(df.pickup_datetime)
df1.head()

df1['pickup_datetime'].dtype

df2 = df1.assign(
    year=df1.pickup_datetime.dt.year,
    month=df1.pickup_datetime.dt.month,
    day=df1.pickup_datetime.dt.day,
    hour=df1.pickup_datetime.dt.hour,
    dayofweek=df1.pickup_datetime.dt.dayofweek
)

df2.head()

df3=df2.drop(['pickup_datetime'],axis=1)
df3.head()

df3.dtypes

"""**Identify Outliers**"""

plt.boxplot(df3['fare_amount'],vert=False)

q1=df3['fare_amount'].quantile(0.25)
q3=df3['fare_amount'].quantile(0.75)
IQR=q3-q1
lower_bound=q1-1.5*IQR
upper_bound=q3+1.5*IQR

df4=df3[(df3['fare_amount']<upper_bound) & (df3['fare_amount']>lower_bound)]
plt.boxplot(df4['fare_amount'],vert=False)

df4['fare_amount'].median()

print(q3,q1)

df4.dtypes

incorrect_coordinates=df4.loc[(df4.pickup_latitude>90) | (df4.pickup_latitude<-90) |
                              (df4.pickup_longitude>180) | (df4.pickup_longitude<-180) |
                              (df4.dropoff_latitude>90) | (df4.dropoff_latitude<-90) |
                              (df4.dropoff_longitude>180) | (df4.dropoff_longitude<-180)]

df.drop(incorrect_coordinates,inplace=True,errors='ignore')

"""**Check correlation**"""

df4.corr()

"""**Implement ML models**

Linear Regression
"""

df4.columns

x=df4[['pickup_longitude', 'pickup_latitude','dropoff_longitude', 'dropoff_latitude', 'passenger_count', 'year','month', 'day', 'hour', 'dayofweek']]
y=df4[['fare_amount']]

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=12000)

x_train.shape,y_train.shape,x_test.shape,y_test.shape

x_train

x_test

x_train.isnull().sum()

x_train['passenger_count'].fillna(value=x_train['passenger_count'].mean(),inplace=True)
x_train['dropoff_longitude'].fillna(value=x_train['dropoff_longitude'].mean(),inplace=True)
x_train['dropoff_latitude'].fillna(value=x_train['dropoff_latitude'].mean(),inplace=True)

x_train.isnull().sum()

y_train.isnull().sum()

"""y_train.head()"""

from sklearn.linear_model import LinearRegression
reg=LinearRegression()
reg.fit(x_train,y_train)

y_pred_lin=reg.predict(x_test)

y_pred_lin

y_test.shape,y_pred_lin.shape

y_test = np.array(y_test).flatten()
y_pred_lin = np.array(y_pred_lin).flatten()

pd.DataFrame({"expected value":y_test,"actual value":y_pred_lin})

"""Random Forest Regression"""

from sklearn.ensemble import RandomForestRegressor
rf=RandomForestRegressor(n_estimators=100)
rf.fit(x_train,y_train)

y_pred_rf=rf.predict(x_test)

y_pred_rf

y_pred_rf = np.array(y_pred_rf).flatten()

pd.DataFrame({"expected value":y_test,"actual value":y_pred_rf})

"""**Evaluate the models and compare their respective scores like R2, RMSE, etc.**"""

from sklearn import metrics
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

"""Linear Regression metrics"""

r1_random=r2_score(y_test,y_pred_lin)
r1_random

msc1_random=mean_squared_error(y_test,y_pred_lin)
msc1_random

rmsc1_random=np.sqrt(msc1_random)
rmsc1_random

"""Random Forest Regression Metrics"""

r2_random=r2_score(y_test,y_pred_rf)
r2_random

msc2_random=mean_squared_error(y_test,y_pred_rf)
msc2_random

rmsc2_random=np.sqrt(msc2_random)
rmsc2_random

