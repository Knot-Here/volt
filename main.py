# main.py
import pandas as pd
import numpy as np
import os
from src.core import calculate_volt_simple


def main():
    # Asset configuration
    asset1_name = "ethereum"  # Collateral asset
    asset2_name = "bitcoin"  # Borrowed asset
    deposit_amount = 10000

    # Load price data for both assets
    prices_dir = "./output/prices"
    asset1_df = pd.read_csv(os.path.join(prices_dir, f"{asset1_name}.csv"))
    asset2_df = pd.read_csv(os.path.join(prices_dir, f"{asset2_name}.csv"))

    # Convert to series with datetime index
    asset1_df["timestamp"] = pd.to_datetime(asset1_df["timestamp"])
    asset2_df["timestamp"] = pd.to_datetime(asset2_df["timestamp"])

    asset1_prices = asset1_df.set_index("timestamp")["price"]
    asset2_prices = asset2_df.set_index("timestamp")["price"]

    # Run VOLT calculation
    result = calculate_volt_simple(
        collateral_prices=asset1_prices,
        borrowed_prices=asset2_prices,
        deposit=deposit_amount,
    )

    asset1_name = asset1_name.capitalize()
    asset2_name = asset2_name.capitalize()

    # Print results
    print(f"\n=== VOLT Formula Results for {asset1_name}/{asset2_name} ===")
    print(f"{asset1_name} Volatility: {result['volatility_a'] * 100:.1f}%")
    print(f"{asset2_name} Volatility: {result['volatility_b'] * 100:.1f}%")
    print(f"{asset1_name}-{asset2_name} Correlation: {result['correlation']:.2f}")
    print(f"Relative Volatility: {result['relative_volatility'] * 100:.1f}%")
    print(f"Safety Margin: {result['safety_margin'] * 100:.1f}%")
    print(f"Optimal LTV: {result['optimal_ltv'] * 100:.1f}%")
    print(
        f"For ${deposit_amount:,} {asset1_name} deposit, optimal {asset2_name} borrow: ${result['optimal_borrow']:.2f}"
    )

    # Compare with stablecoin borrow
    # For stablecoins, volatility_b = 0 and correlation = 0
    v_rel_stablecoin = result[
        "volatility_a"
    ]  # Just use the already calculated volatility
    safety_margin_stablecoin = 2.0 * (v_rel_stablecoin / np.sqrt(365)) * np.sqrt(14)
    optimal_ltv_stablecoin = 0.825 - safety_margin_stablecoin
    optimal_borrow_stablecoin = deposit_amount * optimal_ltv_stablecoin

    print("\n=== Capital Efficiency Comparison ===")
    print(f"{asset1_name}/USDC optimal borrow: ${optimal_borrow_stablecoin:.2f}")
    print(
        f"{asset1_name}/{asset2_name} optimal borrow: ${result['optimal_borrow']:.2f}"
    )
    print(
        f"Improvement: {((result['optimal_borrow'] / optimal_borrow_stablecoin) - 1) * 100:.1f}%"
    )


if __name__ == "__main__":
    main()

