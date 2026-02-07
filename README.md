# Monte Carlo Pricer for Asian Options 📈

A high-performance Python implementation of Monte Carlo simulation for pricing Asian options with advanced variance reduction techniques, achieving up to **73.8% variance reduction**.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🎯 Overview

This project implements a Monte Carlo pricer for path-dependent Asian options under the Black-Scholes framework. The key innovation lies in comparing three variance reduction methods to optimize pricing accuracy and computational efficiency.

### Key Features

- **Three variance reduction methods**:
  - Basic Monte Carlo (baseline)
  - Antithetic variates
  - Control variates using European options
  
- **Real market data integration** via Yahoo Finance API
- **Comprehensive performance analysis**:
  - Convergence behavior across simulation sizes (1,000 to 50,000 paths)
  - Payoff correlation analysis between Asian and European options
  - Detailed variance reduction effectiveness metrics

## 📊 Results

### Variance Reduction Performance

| Method | Variance | Reduction vs Basic | Confidence Interval Width |
|--------|----------|-------------------|---------------------------|
| Basic Monte Carlo | 2,534 | - | 0.63 |
| Antithetic Variates | 2,535 | -0.1% | 0.62 |
| **Control Variates** | **665** | **73.8%** | **0.30** |

### Key Findings

- **73.8% variance reduction** achieved with control variates
- **Asian-European correlation**: ρ = 0.86 (explains effectiveness of control variate method)
- **Efficiency gain**: 3.8x fewer simulations needed for same accuracy
- **Confidence interval**: 2x narrower with control variates

### Sample Output

```
=== COMPARISON OF 3 METHODS ===

--- BASIC PURE (no variance reduction) ---
Price     = 98.5881
Variance  = 2534.0740
IC        = (98.15, 99.03)

--- ANTITHETIC ONLY ---
Price     = 98.6679
Variance  = 2535.3626   (↓ vs basic: -0.1%)
IC        = (98.36, 98.98)

--- ANTITHETIC + CONTROL VARIATE ---
Price     = 97.1666
Variance  = 665.1806    (↓ vs anti: 73.8%)
IC        = (97.01, 97.33)
```

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/asian-option-pricer.git
cd asian-option-pricer

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from src.monte_carlo_pricer import asian_option_pricer

# Price an Asian call option on Apple stock
result = asian_option_pricer(
    S0=278.12,          # Current spot price
    K=180,              # Strike price
    r=0.03,             # Risk-free rate
    q=0.005,            # Dividend yield
    sigma=0.316,        # Volatility (estimated from historical data)
    T=1,                # Maturity in years
    n_sim=50000,        # Number of simulations
    obs_freq="daily",   # Observation frequency
    option_type="call"  # Call or put
)

# Display results
print(f"Option Price (CV): ${result['Price CV']:.2f}")
print(f"Variance Reduction: {(1 - result['Var CV']/result['Var Basic'])*100:.1f}%")
print(f"95% Confidence Interval: [{result['IC CV'][0]:.2f}, {result['IC CV'][1]:.2f}]")
```

### Using Real Market Data

```python
from src.monte_carlo_pricer import load_asset_parameters, asian_option_pricer

# Automatically fetch real market parameters
S0, sigma, r, q, _ = load_asset_parameters("AAPL", period="1y")

# Price the option
result = asian_option_pricer(S0, K=180, r=r, q=q, sigma=sigma, T=1)
print(f"Price: ${result['Price CV']:.2f}")
```

## 📈 Methodology

### Asian Options

Asian options are path-dependent derivatives where the payoff depends on the **average price** over the option's life:

```
Payoff = max(A - K, 0)  for call
where A = (1/n) Σ S(ti)
```

Unlike European options, no closed-form solution exists for Asian options under Black-Scholes, making Monte Carlo the practical pricing method.

### Variance Reduction Techniques

#### 1. Antithetic Variates

For each random normal Z, simulate both Z and -Z to create symmetric paths:

```python
Z = box_muller(n_sim, m_steps)
Z_full = np.vstack([Z, -Z])  # Antithetic pairs
```

**Result**: Minimal improvement (-0.1%) for Asian options due to path-averaging effect.

#### 2. Control Variates

Use European option (known closed-form price) as control variable:

```python
# Adjustment formula
X_cv = X_asian - β * (Y_european - Y_exact)

where β = Cov(X_asian, Y_european) / Var(Y_european)
```

**Result**: 73.8% variance reduction due to high correlation (ρ = 0.86) between Asian and European payoffs.

### Box-Muller Algorithm

Generates standard normal random variables from uniform distributions:

```python
def box_muller(n_sim, m_steps):
    U1 = np.random.rand(n_sim, m_steps)
    U2 = np.random.rand(n_sim, m_steps)
    return np.sqrt(-2 * np.log(U1)) * np.cos(2 * np.pi * U2)
```

## 📁 Project Structure

```
asian-option-pricer/
│
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── LICENSE                        # MIT License
│
├── src/
│   └── monte_carlo_pricer.py     # Main implementation
│
├── visualizations/
│   ├── create_visualizations.py  # Generate all plots
│   ├── monte_carlo_process.png   # Process overview
│   ├── convergence.png           # Convergence analysis
│   └── variance_comparison.png   # Method comparison
│
├── examples/
│   ├── basic_usage.py            # Simple examples
│   └── advanced_analysis.ipynb   # Jupyter notebook with detailed analysis
│
└── results/
    └── benchmark_results.txt     # Performance metrics
```

## 🛠️ Technologies

- **Python 3.8+**
- **NumPy** - Vectorized numerical computations
- **Pandas** - Data manipulation and analysis
- **SciPy** - Statistical functions (normal distribution)
- **Matplotlib/Seaborn** - Publication-quality visualizations
- **yfinance** - Real-time market data from Yahoo Finance

## 📊 Visualizations

### Convergence Analysis

Shows how the price estimate stabilizes as simulation count increases:

![Convergence](visualizations/convergence_placeholder.png)

### Variance Reduction Comparison

Compares the three methods across different metrics:

![Variance Comparison](visualizations/variance_comparison_placeholder.png)

## 🧪 Testing & Validation

### Validation Against Black-Scholes

European option prices are validated against Black-Scholes closed-form solution:

```
European Price (Monte Carlo): $104.27
European Price (Black-Scholes): $104.27
Difference: < 0.01%
```

### Grid Analysis

Tested across multiple strikes and maturities:

```
Strike | Maturity | Asian Price | European Price | Difference
-------|----------|-------------|----------------|------------
80     | 0.5y     | $195.40     | $198.62        | $3.21
100    | 1.0y     | $173.59     | $179.69        | $6.11
120    | 2.0y     | $151.04     | $163.01        | $11.97
```

**Observation**: Asian options consistently priced lower than Europeans (expected behavior due to averaging effect).

## 🎓 Academic Context

This project was developed as part of quantitative finance coursework at **ECE Paris** (2024-2025), focusing on:

- Stochastic calculus applications in derivatives pricing
- Monte Carlo methods for path-dependent options
- Variance reduction techniques in computational finance
- Real-world data integration and validation

## 📚 References

- Hull, J. (2018). *Options, Futures, and Other Derivatives*
- Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*
- Kemna, A., & Vorst, A. (1990). "A pricing method for options based on average asset values"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Thomas Nassar**
- 🎓 ECE Paris - M1 Finance & Quantitative Engineering
- 💼 [LinkedIn](https://www.linkedin.com/in/thomas-nassar-a9935a290)
- 📧 thomas.nassar@edu.ece.fr
- 🔗 Seeking 6-month Front Office / Quantitative internship (April 2026)

## 🌟 Acknowledgments

- ECE Paris Finance & Quantitative Engineering program
- Yahoo Finance for market data API

---

⭐ **If you find this project useful, please consider giving it a star!**

## 📝 Future Enhancements

- [ ] Add GPU acceleration with CuPy for large-scale simulations
- [ ] Implement additional variance reduction (importance sampling, stratified sampling)
- [ ] Extend to geometric Asian options
- [ ] Add Greeks calculation (Delta, Gamma, Vega)
- [ ] Develop web interface for interactive pricing
- [ ] Compare with other numerical methods (PDE, binomial trees)
