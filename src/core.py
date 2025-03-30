import pandas as pd
import numpy as np
import os


def calculate_volt(
    collateral_prices: pd.Series,
    borrowed_prices: pd.Series,
    risk_tolerance: float = 2.0,
    time_horizon: int = 14,
    ltv_max: float = 0.825,
    deposit: float = 10000,
):
    """
    Simple VOLT formula calculator using price series data.

    Parameters:
    - collateral_prices: Price series for collateral asset (e.g., ETH prices)
    - borrowed_prices: Price series for borrowed asset (e.g., BTC prices)
    - risk_tolerance: Risk parameter k (1=risky, 2=balanced, 3=conservative)
    - time_horizon: Position horizon in days
    - ltv_max: Maximum LTV allowed by the platform
    - deposit: Amount of collateral to deposit

    Returns:
    - Dictionary with optimal LTV and borrow amount
    """
    # Calculate returns
    collateral_returns = collateral_prices.pct_change().dropna()
    borrowed_returns = borrowed_prices.pct_change().dropna()

    # Calculate volatilities (annualized)
    volatility_a = collateral_returns.std() * np.sqrt(365)
    volatility_b = borrowed_returns.std() * np.sqrt(365)

    # Calculate correlation
    # Align the series first to ensure we're comparing the same dates
    aligned_returns = pd.concat([collateral_returns, borrowed_returns], axis=1).dropna()
    correlation = aligned_returns.iloc[:, 0].corr(aligned_returns.iloc[:, 1])

    # Calculate relative volatility
    v_rel = np.sqrt(
        volatility_a**2
        + volatility_b**2
        - 2 * correlation * volatility_a * volatility_b
    )

    # Convert to daily volatility
    v_rel_daily = v_rel / np.sqrt(365)

    # Calculate safety margin
    safety_margin = risk_tolerance * v_rel_daily * np.sqrt(time_horizon)

    # Calculate optimal LTV
    optimal_ltv = ltv_max - safety_margin

    # Calculate optimal borrow
    optimal_borrow = deposit * optimal_ltv

    # Create results
    results = {
        "volatility_a": volatility_a,
        "volatility_b": volatility_b,
        "correlation": correlation,
        "relative_volatility": v_rel,
        "safety_margin": safety_margin,
        "optimal_ltv": optimal_ltv,
        "optimal_borrow": optimal_borrow,
    }

    return results


# Example usage
if __name__ == "__main__":
    # Load price data for ETH and BTC
    prices_dir = "./output/prices"
    eth_df = pd.read_csv(os.path.join(prices_dir, "ethereum.csv"))
    btc_df = pd.read_csv(os.path.join(prices_dir, "bitcoin.csv"))

    # Convert to series with datetime index
    eth_df["timestamp"] = pd.to_datetime(eth_df["timestamp"])
    btc_df["timestamp"] = pd.to_datetime(btc_df["timestamp"])

    eth_prices = eth_df.set_index("timestamp")["price"]
    btc_prices = btc_df.set_index("timestamp")["price"]

    # Run VOLT calculation
    result = calculate_volt(
        collateral_prices=eth_prices, borrowed_prices=btc_prices, deposit=10000
    )

    # Print results
    print("\n=== VOLT Formula Results ===")
    print(f"ETH Volatility: {result['volatility_a'] * 100:.1f}%")
    print(f"BTC Volatility: {result['volatility_b'] * 100:.1f}%")
    print(f"ETH-BTC Correlation: {result['correlation']:.2f}")
    print(f"Relative Volatility: {result['relative_volatility'] * 100:.1f}%")
    print(f"Safety Margin: {result['safety_margin'] * 100:.1f}%")
    print(f"Optimal LTV: {result['optimal_ltv'] * 100:.1f}%")
    print(
        f"For $10,000 ETH deposit, optimal BTC borrow: ${result['optimal_borrow']:.2f}"
    )

    # Compare with stablecoin borrow
    # For stablecoins, volatility_b = 0 and correlation = 0
    v_rel_stablecoin = volatility_a = eth_prices.pct_change().dropna().std() * np.sqrt(
        365
    )
    safety_margin_stablecoin = 2.0 * (v_rel_stablecoin / np.sqrt(365)) * np.sqrt(14)
    optimal_ltv_stablecoin = ltv_max = 0.825 - safety_margin_stablecoin
    optimal_borrow_stablecoin = 10000 * optimal_ltv_stablecoin

    print("\n=== Capital Efficiency Comparison ===")
    print(f"ETH/USDC optimal borrow: ${optimal_borrow_stablecoin:.2f}")
    print(f"ETH/BTC optimal borrow: ${result['optimal_borrow']:.2f}")
    print(
        f"Improvement: {((result['optimal_borrow'] / optimal_borrow_stablecoin) - 1) * 100:.1f}%"
    )
