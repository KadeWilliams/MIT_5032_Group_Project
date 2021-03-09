import pandas as pd # to read data
import numpy as np
import matplotlib.pyplot as plt

# Display all of the columns in the data set
pd.set_option('display.max_columns', None)

# store the csv as a dataframe
df = pd.read_csv('euro-daily-hist_1999_2020.csv', delimiter=',')

# fill the null (NaN) values with 0 to help with type conversion
df = df.fillna(0)

'''CLEAN THE COLUMN HEADERS'''
# Remove the square brackets around
df.columns = df.columns.str.replace(r'([\[\]])', '')
# Remove the '\' and ':' from 'Period\Unit:' column
df.columns = df.columns.str.replace(r'[^\w.+\s]', ' ')
df.columns = df.columns.str.strip()

# # Get the column names for readability and easy transfer
# text_file = open('columns.txt', 'w')
# for column in df:
#     column_names = text_file.write(f'{column}\n')

# print(df['Period\Unit:'])

df_small = df[[
        'Period Unit',
        'Australian dollar',
        'Chinese yuan renminbi',
        # 'Korean won',
        'Brazilian real',
        'UK pound sterling',
        'US dollar'
]]

headers = {
        'Period Unit': 'Period',
        'Australian dollar': 'AUD',
        'Chinese yuan renminbi': 'CNY',
        # 'Korean won': 'KRW',
        'Brazilian real': 'BRL',
        'UK pound sterling': 'GBP',
        'US dollar': 'USD'
}


df_small.rename(columns=headers, inplace=True)
print(df_small)


df_small = df_small[~df_small['AUD'].isin(['-'])]
df_small = df_small[~df_small['CNY'].isin(['-'])]
# df_small = df_small[~df_small['KRW'].isin(['-'])]
df_small = df_small[~df_small['BRL'].isin(['-'])]
df_small = df_small[~df_small['GBP'].isin(['-'])]
df_small = df_small[~df_small['USD'].isin(['-'])]

type_conversion_dict = {
        'Period': 'datetime64[ns]',
        'AUD': float,
        'CNY': float,
        'BRL': float,
        'GBP': float,
        'USD': float
}

df_small = df_small.astype(type_conversion_dict)
print(df_small.dtypes)


print(df_small.describe())

# # Bar Chart of unbound data (from the first entry to the latest entry)
# ax = df_small.plot.bar(rot=0)
# plt.show()

# # Write the Data Frame to txt for readability
df_small.to_csv('small_df.txt', header=True, index=None, sep=' ')


