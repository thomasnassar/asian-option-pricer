"""
Basic usage examples for the Asian Option Monte Carlo Pricer
"""

import sys
sys.path.append('..')

from src.monte_carlo_pricer import (
    load_asset_parameters,
    asian_option_pricer,
    compare_three_methods
)

print("="*60)
print("ASIAN OPTION MONTE CARLO PRICER - EXAMPLES")
print("="*60)

# Example 1: Price with real market data
print("\n📊 Example 1: Pricing with Real Market Data (Apple)")
print("-" * 60)

S0, sigma, r, q, _ = load_asset_parameters("AAPL", period="1y")

print(f"Current Spot Price: ${S0:.2f}")
print(f"Implied Volatility: {sigma:.2%}")
print(f"Risk-free Rate: {r:.2%}")
print(f"Dividend Yield: {q:.2%}")

result = asian_option_pricer(
    S0=S0,
    K=180,
    r=r,
    q=q,
    sigma=sigma,
    T=1,
    n_sim=50000,
    obs_freq="daily",
    option_type="call"
)

print(f"\n✅ RESULTS:")
print(f"  Option Price (Basic MC): ${result['Price Basic']:.2f}")
print(f"  Option Price (Control Variate): ${result['Price CV']:.2f}")
print(f"  Variance Reduction: {(1 - result['Var CV']/result['Var Basic'])*100:.1f}%")
print(f"  95% CI (CV): [${result['IC CV'][0]:.2f}, ${result['IC CV'][1]:.2f}]")
print(f"  Beta: {result['Beta']:.4f}")
print(f"  European Price (Benchmark): ${result['Euro Exact']:.2f}")


# Example 2: Compare all three methods
print("\n\n📈 Example 2: Comparing Three Variance Reduction Methods")
print("-" * 60)

compare_three_methods(
    S0=S0,
    K=180,
    r=r,
    q=q,
    sigma=sigma,
    T=1,
    n_sim=50000,
    obs_freq="daily",
    option_type="call"
)


# Example 3: Custom parameters
print("\n\n🔧 Example 3: Custom Parameters")
print("-" * 60)

custom_result = asian_option_pricer(
    S0=100,             # Custom spot
    K=100,              # ATM option
    r=0.05,             # 5% risk-free rate
    q=0.02,             # 2% dividend
    sigma=0.20,         # 20% volatility
    T=0.5,              # 6 months
    n_sim=20000,        # Fewer simulations for speed
    obs_freq="weekly",  # Weekly averaging
    option_type="put"   # Put option
)

print(f"Custom Put Option Price: ${custom_result['Price CV']:.2f}")
print(f"Variance Reduction: {(1 - custom_result['Var CV']/custom_result['Var Basic'])*100:.1f}%")


# Example 4: Different observation frequencies
print("\n\n📅 Example 4: Impact of Observation Frequency")
print("-" * 60)

frequencies = ["daily", "weekly", "monthly"]
for freq in frequencies:
    result = asian_option_pricer(
        S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1,
        n_sim=10000, obs_freq=freq, option_type="call"
    )
    print(f"{freq.capitalize():10s} averaging: ${result['Price CV']:.4f}")


print("\n" + "="*60)
print("✅ Examples completed successfully!")
print("="*60)
