# Getting Started Guide

## Quick Start (5 minutes)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/asian-option-pricer.git
cd asian-option-pricer

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Your First Pricing

```bash
# Run the example script
python examples/basic_usage.py
```

You should see output like:

```
=================================================
ASIAN OPTION MONTE CARLO PRICER - EXAMPLES
=================================================

📊 Example 1: Pricing with Real Market Data (Apple)
------------------------------------------------------------
Current Spot Price: $278.12
Implied Volatility: 31.56%
Risk-free Rate: 3.00%
Dividend Yield: 0.50%

✅ RESULTS:
  Option Price (Basic MC): $98.67
  Option Price (Control Variate): $97.17
  Variance Reduction: 73.3%
  95% CI (CV): [$96.99, $97.31]
```

### 3. Try Interactive Pricing

Open Python interpreter:

```python
from src.monte_carlo_pricer import asian_option_pricer

# Price a simple ATM call option
result = asian_option_pricer(
    S0=100,      # Current price
    K=100,       # Strike price
    r=0.05,      # 5% risk-free rate
    q=0.02,      # 2% dividend
    sigma=0.25,  # 25% volatility
    T=1          # 1 year maturity
)

print(f"Option Price: ${result['Price CV']:.2f}")
```

## Understanding the Output

### Key Metrics Explained

```python
result = {
    'Price Basic': 10.52,      # Price without variance reduction
    'Price CV': 10.48,         # Price with control variates (use this!)
    'Var Basic': 125.4,        # Variance of basic estimator
    'Var CV': 32.1,            # Variance of CV estimator (73.8% lower!)
    'IC Basic': (10.30, 10.74),# 95% confidence interval (basic)
    'IC CV': (10.41, 10.55),   # 95% confidence interval (CV) - much tighter!
    'Beta': 0.52,              # Control variate coefficient
    'Euro Exact': 12.34        # European option price (benchmark)
}
```

**What to look for:**
- Use `Price CV` as your final price estimate
- Check that `IC CV` is narrower than `IC Basic` (validates variance reduction)
- Higher variance reduction % = better performance

## Common Use Cases

### 1. Price with Real Market Data

```python
from src.monte_carlo_pricer import load_asset_parameters, asian_option_pricer

# Automatically fetch Apple's current parameters
S0, sigma, r, q, _ = load_asset_parameters("AAPL")

# Price an Asian call option
result = asian_option_pricer(S0=S0, K=200, r=r, q=q, sigma=sigma, T=1)
print(f"Asian Call Price: ${result['Price CV']:.2f}")
```

### 2. Compare Call vs Put

```python
# Call option
call = asian_option_pricer(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1, 
                           option_type="call")

# Put option
put = asian_option_pricer(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1, 
                          option_type="put")

print(f"Call Price: ${call['Price CV']:.2f}")
print(f"Put Price: ${put['Price CV']:.2f}")
```

### 3. Analyze Different Strikes

```python
import pandas as pd

strikes = [80, 90, 100, 110, 120]
results = []

for K in strikes:
    result = asian_option_pricer(S0=100, K=K, r=0.05, q=0.02, sigma=0.25, T=1)
    results.append({
        'Strike': K,
        'Price': result['Price CV'],
        'Moneyness': 'ITM' if K < 100 else ('ATM' if K == 100 else 'OTM')
    })

df = pd.DataFrame(results)
print(df)
```

### 4. Test Variance Reduction Effectiveness

```python
from src.monte_carlo_pricer import compare_three_methods

# This will show you the performance of all three methods
compare_three_methods(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1)
```

## Advanced Topics

### Adjusting Simulation Parameters

```python
# More simulations = higher accuracy but slower
result_10k = asian_option_pricer(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1,
                                 n_sim=10000)   # Fast (~1 second)

result_100k = asian_option_pricer(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1,
                                  n_sim=100000)  # Slower (~10 seconds)

# Compare confidence interval width
width_10k = result_10k['IC CV'][1] - result_10k['IC CV'][0]
width_100k = result_100k['IC CV'][1] - result_100k['IC CV'][0]

print(f"CI width with 10k sims: {width_10k:.4f}")
print(f"CI width with 100k sims: {width_100k:.4f}")
```

### Observation Frequency Impact

```python
# Daily averaging (252 observations per year)
daily = asian_option_pricer(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1,
                            obs_freq="daily")

# Weekly averaging (52 observations per year)
weekly = asian_option_pricer(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1,
                             obs_freq="weekly")

# Monthly averaging (12 observations per year)
monthly = asian_option_pricer(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1,
                              obs_freq="monthly")

print(f"Daily:   ${daily['Price CV']:.4f}")
print(f"Weekly:  ${weekly['Price CV']:.4f}")
print(f"Monthly: ${monthly['Price CV']:.4f}")
# Higher frequency → lower price (more averaging → less volatility)
```

## Troubleshooting

### Problem: "Module not found" error

**Solution:**
```bash
# Make sure you're in the project root directory
cd asian-option-pricer

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: yfinance download fails

**Solution:**
```python
# Use custom parameters instead
S0 = 100      # Set manually
sigma = 0.25  # Historical volatility
r = 0.05      # Current risk-free rate
q = 0.02      # Expected dividend

result = asian_option_pricer(S0=S0, K=100, r=r, q=q, sigma=sigma, T=1)
```

### Problem: Code runs very slowly

**Solution:**
```python
# Reduce number of simulations for testing
result = asian_option_pricer(S0=100, K=100, r=0.05, q=0.02, sigma=0.25, T=1,
                             n_sim=5000)  # Much faster, still reasonable accuracy
```

## Next Steps

1. **Explore visualizations**: Run `python visualizations/create_visualizations.py`
2. **Read the methodology**: Check the "Methodology" section in README.md
3. **Try different parameters**: Experiment with various S0, K, sigma, T combinations
4. **Compare with European options**: See how Asian prices differ from Europeans
5. **Analyze convergence**: Test with different simulation sizes

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [examples/basic_usage.py](examples/basic_usage.py) for more examples
- Open an issue on GitHub if you find bugs

---

Happy pricing! 📈
