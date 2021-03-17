import pandas as pd  # to read data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Display all of the columns in the data set
pd.set_option('display.max_columns', None)

# store the csv as a dataframe
df = pd.read_csv('euro-daily-hist_1999_2020.csv', delimiter=',')

'''CLEAN THE COLUMN HEADERS'''
# Remove the square brackets around
df.columns = df.columns.str.replace(r'([\[\]])', '')

# Remove the '\' and ':' from 'Period\Unit:' column
df.columns = df.columns.str.replace(r'[^\w.+\s]', ' ')
df.columns = df.columns.str.strip()

# fill the null (NaN) values with 0 to help with type conversion
df = df.fillna(0)

# Reduce the width of the data frame
df = df[[
    'Period Unit',
    # 'Australian dollar',
    # 'Chinese yuan renminbi',
    # 'Korean won',
    'Brazilian real',
    'UK pound sterling',
    'US dollar'
]]
# Change the names of the columns for simpler comparisons
headers = {
    'Period Unit': 'Period',
    # 'Australian dollar': 'AUD',
    # 'Chinese yuan renminbi': 'CNY',
    # 'Korean won': 'KRW',
    # 'Brazilian real': 'BRL',
    'UK pound sterling': 'GBP',
    'US dollar': 'USD'
}

df.rename(columns=headers, inplace=True)
# print(df)


# df = df[~df['AUD'].isin(['-'])]
# df = df[~df['CNY'].isin(['-'])]
# df = df[~df['KRW'].isin(['-'])]
# df = df[~df['BRL'].isin(['-'])]
df = df[~df['GBP'].isin(['-'])]
df = df[~df['USD'].isin(['-'])]

# Change the data type of the working columns
type_conversion_dict = {
    'Period': 'datetime64[ns]',
    # 'AUD': float,
    # 'CNY': float,
    # 'BRL': float,
    'GBP': float,
    'USD': float
}

df['Period'] = pd.to_datetime(df['Period'])

df = df[df['Period'] > '2020-01-01 00:00:00']
df = df[df['Period'] < '2021-02-12 00:00:00']

usd_max = df['USD'].max()
usd_min = df['USD'].min()

gbp_max = df['GBP'].max()
gbp_min = df['GBP'].min()

df = df.astype(type_conversion_dict)
df.set_index('Period', inplace=True)

# Line chart of the data with scatter points on the peaks and valleys and size adjustment
ax = df.plot(lw=6, zorder=1)
plt.scatter('2020-03-19', df['GBP'].max(), c='black', s=100, zorder=2)
plt.scatter('2020-02-18', df['GBP'].min(), c='black', s=100, zorder=2)
plt.scatter('2021-01-06', df['USD'].max(), c='black', s=100, zorder=2)
plt.scatter('2020-03-20', df['USD'].min(), c='black', s=100, zorder=2)

# Change the label and their size
plt.xlabel('Period', fontsize=20)
plt.ylabel('Euro', fontsize=20)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(16)

axes = plt.gca()

# Display the legend
ax.legend()

# Create a red-line at 1.00 which denotes the Euro
plt.axhline(y=1, color='r', linestyle='--', lw=4)

# Show the created graph
plt.show()
