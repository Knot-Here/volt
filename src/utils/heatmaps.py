import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

############################
# 1. Load price data from CSV files
############################

# Folder containing CSV files
folder_path = "output/prices"


# Function to calculate log returns
def calculate_log_returns(price_series):
    return np.log(price_series / price_series.shift(1)).dropna()


# Dictionary to hold log returns for each coin
returns_data = {}

# Iterate through CSV files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)

        # Extract coin name from file name (e.g., "bitcoin.csv" -> "bitcoin")
        coin_name = os.path.splitext(file)[0]

        # Load the CSV file
        df = pd.read_csv(file_path)

        # Ensure the data is sorted by date
        df = df.sort_values(by="timestamp")

        # Compute log returns and store in dictionary
        returns_data[coin_name] = calculate_log_returns(df["price"])

# Convert dictionary to DataFrame, aligning by date
returns_df = pd.DataFrame(returns_data)

############################
# 2. Compute statistics
############################

# Daily volatility (standard deviation of returns)
sigmas_daily = returns_df.std()

# Convert to annualized volatility (by multiplying sqrt(365))
sigmas_annual = sigmas_daily * np.sqrt(365)

# Compute correlation matrix
corr_matrix = returns_df.corr()

############################
# 3. Compute Relative Volatility (Annualized)
############################


def relative_volatility(sigmaA, sigmaB, rhoAB):
    """
    Computes relative volatility:
    V_rel = sqrt( sigmaA^2 + sigmaB^2 - 2 * rhoAB * sigmaA * sigmaB )
    """
    return np.sqrt(sigmaA**2 + sigmaB**2 - 2 * rhoAB * sigmaA * sigmaB)


# Get list of coin names
coins = list(returns_data.keys())

# Create a matrix for relative volatility
n = len(coins)
rel_vol_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i == j:
            rel_vol_matrix[i, j] = 0
        else:
            sA = sigmas_annual[coins[i]]
            sB = sigmas_annual[coins[j]]
            rhoAB = corr_matrix.loc[coins[i], coins[j]]
            rel_vol_matrix[i, j] = relative_volatility(sA, sB, rhoAB)

# Convert to DataFrame
rel_vol_df = pd.DataFrame(rel_vol_matrix, index=coins, columns=coins)

############################
# 4. Plot Heatmaps
############################

# Relative Volatility Heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(rel_vol_df, annot=True, cmap="Reds")
plt.title("Relative Volatility Heatmap (Annualized)")
plt.show()

# Correlation Heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(corr_matrix, annot=True, cmap="Blues", vmin=-1, vmax=1)
plt.title("Correlation Heatmap of Crypto Assets (Daily Log Returns)")
plt.show()
