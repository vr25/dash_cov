import datetime
from dateutil.relativedelta import relativedelta
import pandas
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import copy

start = datetime.datetime.today() - relativedelta(days=90)
end = datetime.datetime.today()


#small-cap

df1_small = pd.read_csv("sp_600.csv", index_col=False) #.head(5)
inputStock1 = df1_small['Symbol']
inputSector1 = df1_small['Sector']

df1 = pd.DataFrame()

print("small")

for (i, j) in zip(inputStock1, inputSector1):
    try:
        print("Fetched: ", i)
        df1_ = (web.DataReader(i, 'yahoo', start=start, end=end)).reset_index()
        df1_['Symbol'] = i
        df1_['Sector'] = j
        df1 = pd.concat([df1, df1_])
    except:
        print(i)

df1['daily_returns'] = df1['Close'].pct_change()
df1 = df1.dropna()
df1['daily_cum_returns'] = (df1['daily_returns'] + 1).cumprod()

df1.to_csv("small_cap.csv")

df1 = df1.groupby(['Date', 'Sector']).mean().reset_index()
df1.to_csv("small_cap_group.csv")


#mid-cap

df1_mid = pd.read_csv("sp_400.csv", index_col=False) #.head(5)
inputStock2 = df1_mid['Symbol']
inputSector2 = df1_mid['Sector']

df2 = pd.DataFrame()

print("mid")

for (i, j) in zip(inputStock2, inputSector2):
    try:
        print("Fetched: ", i)
        df2_ = (web.DataReader(i, 'yahoo', start=start, end=end)).reset_index()
        df2_['Symbol'] = i
        df2_['Sector'] = j
        df2 = pd.concat([df2, df2_])
    except:
        print(i)

df2['daily_returns'] = df2['Adj Close'].pct_change()
df2 = df2.dropna()
df2['daily_cum_returns'] = (df2['daily_returns'] + 1).cumprod()

df2.to_csv("mid_cap.csv")

df2 = df2.groupby(['Date', 'Sector']).mean().reset_index()
df2.to_csv("mid_cap_group.csv")

#large-cap

df1_large = pd.read_csv("sp_500.csv", index_col=False) #.head(5)
inputStock3 = df1_large['Symbol']
inputSector3 = df1_large['Sector']

df3 = pd.DataFrame()

print("large")

for (i, j) in zip(inputStock3, inputSector3):
    try:
        print("Fetched: ", i)
        df3_ = (web.DataReader(i, 'yahoo', start=start, end=end)).reset_index()
        df3_['Symbol'] = i
        df3_['Sector'] = j
        df3 = pd.concat([df3, df3_])
    except:
        print(i)


df3['daily_returns'] = df3['Adj Close'].pct_change()
df3 = df3.dropna()
df3['daily_cum_returns'] = (df3['daily_returns'] + 1).cumprod()

df3.to_csv("large_cap.csv")

df3 = df3.groupby(['Date', 'Sector']).mean().reset_index()
df3.to_csv("large_cap_group.csv")