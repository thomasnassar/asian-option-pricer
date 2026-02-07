# Monte Carlo Pricer for Asian Options 


##  Overview

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

##  Results

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


##  Methodology

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



##  Technologies

- **Python 3.8+**
- **NumPy** - Vectorized numerical computations
- **Pandas** - Data manipulation and analysis
- **SciPy** - Statistical functions (normal distribution)
- **Matplotlib/Seaborn** - Publication-quality visualizations
- **yfinance** - Real-time market data from Yahoo Finance

##  Visualizations

### Convergence Analysis

Shows how the price estimate stabilizes as simulation count increases:

![Convergence](visualizations/convergence_placeholder.png)

### Variance Reduction Comparison

Compares the three methods across different metrics:

![Variance Comparison](visualizations/variance_comparison_placeholder.png)

##  Testing & Validation

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


##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Author

**Thomas Nassar**
-  ECE Paris - Finance & Quantitative Engineering
-  [LinkedIn](https://www.linkedin.com/in/thomas-nassar-a9935a290)
-  thomas.nassar@edu.ece.fr

