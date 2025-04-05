# For Data Manipulation
import pandas as pd
import numpy as np

# For Plotting Graph
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

relative_path = "../data_modules/"
file_name = "Jan_2010_to_Jan_2019_Rebased_Series"
file_extension = ".csv"

data = pd.read_csv(relative_path + file_name + file_extension)

data.index = pd.to_datetime(data.index)

short_term = 50
long_term = 200

data['sma_50'] = data['rebased_close'].rolling(short_term, short_term).mean()
data['sma_200'] = data['rebased_close'].rolling(long_term, long_term).mean()

data['regime_sma_50_200'] = np.where(data['sma_50'] >= data['sma_200'], 1, -1)

def plot_graph(data, ylabel, xlabel, title, legend):
    plt.figure(figsize=(10, 7))
    plt.plot(data)
    plt.title(title, fontsize=16)
    plt.ylabel(ylabel, fontsize=14)
    plt.xlabel(xlabel, fontsize=14)
    plt.legend(labels=legend)
    plt.grid()
    plt.show()

# ax1 = plot_graph(data[['sma_50', 'sma_200']], 'Price', 'Year', 'Simple Moving Average of 50 & 200 days', ['SMA 50', 'SMA 200'])

# ax2 = plot_graph(data['regime_sma_50_200'], 'Signal', 'Year', 'SMA 50-200', ['regime_50_200'])

# Plotting above two together
# ax = data[['sma_50', 'sma_200']].plot(figsize=(10, 7))
# ax1 = data['regime_sma_50_200'].plot(secondary_y=True, figsize=(10, 7), ax=ax)

# ax.set_title('SMA 50-200 Regime', fontsize=16)
# ax.set_ylabel('Price', fontsize=14)
# ax.set_xlabel('Year', fontsize=14)
# ax1.set_ylabel('Signal', fontsize=14)
# plt.legend()
# plt.grid()
# plt.show()


# Calculating exponential moving average
data['ema_50'] = data['rebased_close'].ewm(span=short_term, min_periods=short_term).mean()
data['ema_200'] = data['rebased_close'].ewm(span=long_term, min_periods=long_term).mean()

data['regime_ema_50_200'] = np.where(data['ema_50'] >= data['ema_200'], 1, -1)

# ax1 = plot_graph(data[['ema_50', 'ema_200']], 'Price', 'Year', 'Exponential Moving Average of 50 & 200 days', ['EMA 50', 'EMA 200'])

# ax2 = plot_graph(data['regime_ema_50_200'], 'Signal', 'Year', 'EMA 50-200', ['regime_50_200'])

# Plotting above two together
# ax = data[['ema_50', 'ema_200']].plot(figsize=(10, 7))
# ax1 = data['regime_ema_50_200'].plot(secondary_y=True, figsize=(10, 7), ax=ax)

# ax.set_title('EMA 50-200 Regime', fontsize=16)
# ax.set_ylabel('Price', fontsize=14)
# ax.set_xlabel('Year', fontsize=14)
# ax1.set_ylabel('Signal', fontsize=14)
# plt.legend()
# plt.grid()
# plt.show()



def regime_sma(df, price, short_term, long_term):
    sma_st = df[price.roling(window=short_term, min_periods=short_term)].mean()
    sma_lt = df[price].rolling(window=long_term, min_periods=long_term).mean()
    df['regime_sma'+'_'+str(short_term)+'_'+str(long_term)] = np.where(sma_st >= sma_lt, 1, np.where(sma_st < sma_lt, -1, np.nan))

    return(df)

def regime_ema(df, price, short_term, long_term):
    ema_st = df[price].ewm(span=short_term, min_periods=short_term).mean()
    ema_lt = df[price].ewm(span=long_term, min_periods=long_term).mean()
    df['regime_ema_'+str(short_term)+'_'+str(long_term)] = np.where(ema_st >= ema_lt, 1, np.where(ema_st < ema_lt, -1, np.nan))

    return(df)


