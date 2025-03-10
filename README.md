# volt

![volt-cover](https://github.com/user-attachments/assets/49a13372-d27b-45c3-bc52-89d812596ffe)

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
Safety Margin: 17.5%
Optimal LTV: 65.0%
For $10,000 Ethereum deposit, optimal Bitcoin borrow: $6495.76

=== Capital Efficiency Comparison ===
Ethereum/USDC optimal borrow: $5458.66
Ethereum/Bitcoin optimal borrow: $6495.76
Improvement: 19.0%

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
