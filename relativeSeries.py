# For Data Manipulation
import pandas as pd
import numpy as np
# import os

# To Plot
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

def read_data(file_name, column_name, y_label, title_name):
    relative_path = "./data_modules/"
    dataframe = pd.read_csv(relative_path + file_name + '.csv', index_col=0, parse_dates=True)
    file_name = dataframe[column_name].plot(figsize=(10, 7))
    plt.title(title_name, fontsize=16)
    plt.ylabel(y_label, fontsize=14)
    plt.xlabel('Date', fontsize=14)

    plt.legend()

    plt.grid()

    # plt.show()

    return dataframe


stock = read_data('BAC_Jan_2010_to_Jan_2019', 'Close', 'Price', 'Stock: Bank of America')

forex = read_data('USDGBP_Jan_2010_to_Jan_2019', 'USDGBP', 'Price', 'Forex:USDGBP')

benchmark = read_data('SP500_Jan_2010_to_Jan_2019', 'SP500', 'Price', 'Benchmark: SP500')

# Joining Datasets
data = pd.concat([stock, forex, benchmark], axis=1)

# To remove fields with null values
# data.dropna(inplace=True)

# To get the first two rows
# print(data.head(2))

# Calculating Adjustment Factor
data['adjustment_factor'] = forex['USDGBP'] * benchmark['SP500']

# Calculate Relative Open
data['relative_open'] = data['Open']/data['adjustment_factor']

# Calculate Relative High
data['relative_high'] = data['High']/data['adjustment_factor']

# Calculate Relative Low
data['relative_low'] = data['Low']/data['adjustment_factor']

# Calculate Relative Close
data['relative_close'] = data['Close']/data['adjustment_factor']



# Calculate Rebased Open
data['rebased_open'] = data['relative_open'] * data['adjustment_factor'].iloc[0]

# Calculate Rebased High 
data['rebased_high'] = data['relative_high'] * data['adjustment_factor'].iloc[0]

# Calculate Rebased Low
data['rebased_low'] = data['relative_low'] * data['adjustment_factor'].iloc[0]

# Calculate Rebased Close
data['rebased_close'] = data['relative_close'] * data['adjustment_factor'].iloc[0]

data = round(data, 2)

# print(data.head(2))


# Plot BAC's Close price against rebased close price
data[['Close', 'rebased_close']].plot(figsize=(10, 7))
plt.title('Close vs Rebased Close Series', fontsize=16)
plt.ylabel('Price', fontsize=14)
plt.xlabel('Year', fontsize=14)
# Add legend on the plot
plt.legend()
# Add the grid
plt.grid()
# Display the graph
plt.show()


# print(os.getcwd())

