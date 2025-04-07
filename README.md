# volt


![volt-cover](https://github.com/user-attachments/assets/7b63029e-02fb-4fe8-9c97-529951310257)

## Overview

VOLT (Volatility-Optimized Loan-to-Value Threshold) is a quantitative approach to determining optimal position sizes in crypto lending markets. This calculator helps you maximize capital efficiency while maintaining a sufficient safety buffer against liquidation.

The core innovation of VOLT is that it dynamically adjusts your borrowing capacity based on:
- Asset volatility
- Correlation between collateral and borrowed assets
- Your chosen risk tolerance
- Your time horizon

## Key Features

- Calculate optimal LTV ratios between any two crypto assets
- Compare capital efficiency of different collateral/borrow pairs
- Visualize the relationship between various crypto assets
- Process historical price data to inform lending decisions

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/volt.git
cd volt
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # WindowsS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Repository Structure
```bash
volt/
├── output/
│   ├── prices/            # CSV files with historical price data
│   ├── correlation-heatmap.png
│   └── relative-volatility-heatmap.png
├── src/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── heatmaps.py    # Heatmap generation utilities
│   │   ├── prices.py      # Price data handling
│   │   └── surface.py     # 3D surface visualization
│   ├── __init__.py
│   └── core.py            # Core VOLT formula implementation
├── LICENSE
├── README.md
├── main.py                # Main script to run the calculator
└── requirements.txt
```

## Usage
To use the VOLT calculator with default settings (ETH as collateral, BTC as borrowed asset):

```bash
python main.py
```

To analyze different asset pairs, modify the asset names at the top of main.py:
```bash
# Asset configuration
asset1_name = "ethereum"  # Collateral asset
asset2_name = "bitcoin"   # Borrowed asset
deposit_amount = 10000
```

Results of VOLT will be displayed like so:
```bash
=== VOLT Formula Results for Ethereum/Bitcoin ===
Ethereum Volatility: 71.3%
Bitcoin Volatility: 50.0%
Ethereum-Bitcoin Correlation: 0.78
Relative Volatility: 44.8%
Safety Margin: 8.8%
Optimal LTV: 73.7%
For $10,000 Ethereum deposit, optimal Bitcoin borrow: $7372.88

=== Capital Efficiency Comparison ===
Ethereum/USDC optimal borrow: $5458.66
Ethereum/Bitcoin optimal borrow: $7372.88
Improvement: 35.1%

```
## Collecting Price Data
This script fetches historical price data for specified cryptocurrencies from the CoinGecko API and optionally caches it for further analysis.

### What It Does
- Retrieves historical market prices for a given list of coins over a specified number of days.
- Converts raw JSON API responses into a structured Pandas DataFrame.
- Saves each coin's data as a CSV file in the output/prices/ directory if cache=True.
- Includes a helper function to compute log returns from price data.

### Key Functions
- get_historical_prices(coin_id, vs_currency, days, cache): Downloads price data for a coin. If cache=True, saves the result to a CSV file.
- calculate_log_returns(price_series)" Calculates log returns from a price series for downstream analysis.

#### Usage
```bash
python src/utils/prices.py
```

By default, the script downloads the last 180 days of price data for:

- bitcoin
- ethereum

## Generating Plots
### Heatmaps
his script processes historical price data to compute log returns, volatility, correlation, and relative volatility between crypto assets. It visualizes the results using heatmaps, giving insights into how assets behave in relation to one another.

#### What It Does
1. Loads CSV price data from the output/prices directory.
2. Computes daily log returns for each asset.
3. Calculates:
  - Annualized volatility (σ)
  - Pairwise correlation between asset returns (ρ)
  - Relative volatility using V_rel = √(σ_A² + σ_B² - 2ρσ_Aσ_B)
4. Visualizes:
- Relative Volatility Heatmap
- Correlation Matrix Heatmap

#### Output
The following visualizations are saved in the output/ directory:
- relative-volatility-heatmap.png
- correlation-heatmap.png

These plots help assess diversification potential and volatility overlap between different crypto assets.

#### Usage
```bash
python src/utils/heatmaps.py
```

![rel-vol](https://github.com/user-attachments/assets/e15bee92-96b1-4c6f-96ec-9ff1e4ae80fd)
![correlation](https://github.com/user-attachments/assets/345f5272-93d4-4e87-903f-1b1c1ea156f9)



### Relative Volatility 3D surface 


This module visualizes the relative volatility between two assets in a 3D surface plot, helping users understand how correlation and individual asset volatility affect overall volatility exposure.

#### What It Does
- Fixes the volatility of Asset B (σ_B) and varies:
  - The volatility of Asset A (σ_A)
  - The correlation (ρ) between the two assets
- Computes relative volatility V_rel = √(σ_A² + σ_B² - 2ρσ_Aσ_B)
- Renders a 3D surface plot with color gradients to highlight regions of high and low relative volatility

#### Output
- Saves a high-resolution plot to output/relative-volatility-surface.png
- Highlights the maximum and minimum V_rel values on the surface
- Includes contour projections for better visual interpretation

#### Usage
```bash
python src/utils/surface.py
```

![surface](https://github.com/user-attachments/assets/4db76550-7c2f-485a-b4f7-6c17d6d82fe5)

