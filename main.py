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

df_small = df[[
    'Period Unit',
    # 'Australian dollar',
    # 'Chinese yuan renminbi',
    # 'Korean won',
    'Brazilian real',
    'UK pound sterling',
    'US dollar'
]]

headers = {
    'Period Unit': 'Period',
    # 'Australian dollar': 'AUD',
    # 'Chinese yuan renminbi': 'CNY',
    # 'Korean won': 'KRW',
    # 'Brazilian real': 'BRL',
    'UK pound sterling': 'GBP',
    'US dollar': 'USD'
}

df_small.rename(columns=headers, inplace=True)
# print(df_small)


# df_small = df_small[~df_small['AUD'].isin(['-'])]
# df_small = df_small[~df_small['CNY'].isin(['-'])]
# df_small = df_small[~df_small['KRW'].isin(['-'])]
# df_small = df_small[~df_small['BRL'].isin(['-'])]
df_small = df_small[~df_small['GBP'].isin(['-'])]
df_small = df_small[~df_small['USD'].isin(['-'])]

type_conversion_dict = {
    'Period': 'datetime64[ns]',
    # 'AUD': float,
    # 'CNY': float,
    # 'BRL': float,
    'GBP': float,
    'USD': float
}

df_small['Period'] = pd.to_datetime(df_small['Period'])

df_small = df_small[df_small['Period'] > '2020-01-01 00:00:00']
df_small = df_small[df_small['Period'] < '2021-02-12 00:00:00']

usd_max = df_small['USD'].max()
usd_min = df_small['USD'].min()

gbp_max = df_small['GBP'].max()
gbp_min = df_small['GBP'].min()

df_small = df_small.astype(type_conversion_dict)
df_small.set_index('Period', inplace=True)

# # Bar Chart of data
ax = df_small.plot(lw=6, zorder=1)
plt.scatter('2020-03-19', df_small['GBP'].max(), c='black', s=100, zorder=2)
plt.scatter('2020-02-18', df_small['GBP'].min(), c='black', s=100, zorder=2)
plt.scatter('2021-01-06', df_small['USD'].max(), c='black', s=100, zorder=2)
plt.scatter('2020-03-20', df_small['USD'].min(), c='black', s=100, zorder=2)

plt.xlabel('Period', fontsize=20)
plt.ylabel('Euro', fontsize=20)

for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(16)

axes = plt.gca()

ax.legend()

plt.axhline(y=1, color='r', linestyle='--', lw=4)
plt.show()
