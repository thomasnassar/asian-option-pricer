
# Projet Pricing ING4 - Option Asiatique Monte Carlo avec Réduction de Variance


import numpy as np
import pandas as pd
import yfinance as yf
import time
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns

np.random.seed(42)


# FRÉQUENCE DE CONSTATATION


def get_m_steps(obs_freq):
    """
    Convertit la fréquence de constatation en nombre de pas Monte Carlo.
        - "daily"   = 252 observations
        - "weekly"  = 52 observations
        - "monthly" = 12 observations
    """
    obs_freq = obs_freq.lower()

    if obs_freq == "daily":
        return 252
    elif obs_freq == "weekly": 
        return 52
    elif obs_freq == "monthly":
        return 12
    else:
        raise ValueError("obs_freq doit être 'daily', 'weekly' ou 'monthly'.")


# IMPORT DES PARAMÈTRES RÉELS DE L’ACTIF via yfinance


def load_asset_parameters(ticker="AAPL", period="1y"):
    """
    Télécharge l'actif réel.
    Retourne :
        - Spot
        - volatilité implicite calculée sur 1 an
        - taux sans risque
        - dividende
        - série historique
    """

    data = yf.download(ticker, period=period, auto_adjust=False)

    if data is None or len(data) == 0:
        raise ValueError(f"Impossible de télécharger {ticker}")

    # Correction multi-index
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(0)

    data.columns = [c.lower().strip() for c in data.columns]

    # Correction si bug yfinance sur certaines versions Windows
    if len(set(data.columns)) == 1 and list(set(data.columns))[0] == ticker.lower():
        data = yf.Ticker(ticker).history(period=period)
        data.columns = [c.lower() for c in data.columns]

    # Choix du prix de clôture
    if "close" in data.columns:
        close = data["close"]
    elif "adj close" in data.columns:
        close = data["adj close"]
    else:
        raise KeyError("Impossible de trouver 'close' ou 'adj close'.")

    S0 = float(close.iloc[-1])

    # Vol annualisée sur log-retours
    log_returns = np.log(close / close.shift(1)).dropna()
    sigma = float(np.sqrt(252) * log_returns.std())

    # Taux constants selon nos hypothèses  
    r = 0.03
    q = 0.005

    return S0, sigma, r, q, close


# GÉNÉRATION DE NORMales via Box–Muller 


def box_muller(n_sim, m_steps):
    """
    Génère n_sim × m_steps normales indépendantes via Box-Muller.
    """
    U1 = np.random.rand(n_sim, m_steps)
    U2 = np.random.rand(n_sim, m_steps)
    return np.sqrt(-2 * np.log(U1)) * np.cos(2 * np.pi * U2)


# SIMULATION DE TRAJECTOIRES BS VECTORISÉE


def simulate_paths(S0, r, q, sigma, T, n_sim, m_steps, Z):
    """
    Génère toutes les trajectoires sous Black-Scholes en 1 ligne vectorisée.
    """
    dt = T / m_steps
    drift = (r - q - 0.5*sigma**2) * dt
    vol = sigma * np.sqrt(dt)

    increments = drift + vol * Z
    log_S = np.cumsum(increments, axis=1)

    S = S0 * np.exp(np.hstack([np.zeros((n_sim,1)), log_S]))
    return S


# PAYOFFS CALL/PUT 


def asian_payoff(S, K, option_type="call"):
    """
    Payoff asiatique discret : moyenne arithmétique des prix simulés.
    """
    A = S.mean(axis=1)
    if option_type == "call":
        return np.maximum(A - K, 0)
    return np.maximum(K - A, 0)


def european_payoff(S, K, option_type="call"):
    """
    Payoff européen standard
    """
    ST = S[:, -1]
    if option_type == "call":
        return np.maximum(ST - K, 0)
    return np.maximum(K - ST, 0)


# CONTROL VARIATE 


def control_variate_adjustment(X, Y, Y_exact):
    """
    Ajustement Control Variate :
    X_cv = X - beta * (Y - Y_exact)
    """
    cov_xy = np.cov(X, Y)[0][1]
    beta = cov_xy / np.var(Y)
    X_cv = X - beta * (Y - Y_exact)
    return X_cv, beta


# FORMULE DE BLACK–SCHOLES 


def bs_european_call_put(S0, K, r, q, sigma, T, option_type="call"):
    """
    Prix exact Black-Scholes utilisé pour le control variate.
    """
    d1 = (np.log(S0/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if option_type == "call":
        return S0*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        return K*np.exp(-r*T)*norm.cdf(-d2) - S0*np.exp(-q*T)*norm.cdf(-d1)


# 7. PRICER ASIATIQUE


def asian_option_pricer(S0, K, r, q, sigma, T,
                        n_sim=50000,
                        obs_freq="daily",     # modifier ici si besoin ("daily", "weekly", "monthly")
                        option_type="call",    # "call" ou "put"
                        variance_reduction=True):

    """
    Fonction principale :
    - calcule prix asiatique
    - calcule prix amélioré CV
    - retourne variance, intervalle de confiance, beta
    """

    # Convertit la fréquence en nombre de steps
    m_steps = get_m_steps(obs_freq)

    # Normales Box-Muller (+ antithetic variates)
    Z = box_muller(n_sim, m_steps)
    Z_full = np.vstack([Z, -Z])

    # Simulation des trajectoires BS
    S_paths = simulate_paths(S0, r, q, sigma, T, 2*n_sim, m_steps, Z_full)

    # Payoffs
    asian = asian_payoff(S_paths, K, option_type)
    euro = european_payoff(S_paths, K, option_type)

    # Prix exact européen
    euro_exact = bs_european_call_put(S0, K, r, q, sigma, T, option_type)

    # Control variate
    asian_cv, beta = control_variate_adjustment(asian, euro, euro_exact)

    # Actualisation
    disc = np.exp(-r*T)
    p_basic = disc * np.mean(asian)
    p_cv = disc * np.mean(asian_cv)

    # Variances et intervalles de confiance
    var_basic = np.var(asian)*disc**2
    var_cv = np.var(asian_cv)*disc**2

    ic_basic = (p_basic - 1.96*np.sqrt(var_basic/(2*n_sim)),
                p_basic + 1.96*np.sqrt(var_basic/(2*n_sim)))

    ic_cv = (p_cv - 1.96*np.sqrt(var_cv/(2*n_sim)),
             p_cv + 1.96*np.sqrt(var_cv/(2*n_sim)))

    return {
        "Price Basic": p_basic,
        "Price CV": p_cv,
        "Var Basic": var_basic,
        "Var CV": var_cv,
        "IC Basic": ic_basic,
        "IC CV": ic_cv,
        "Beta": beta,
        "Euro Exact": euro_exact
    }



# CALCUL DES 3 VERSIONS POUR ANALYSE


def price_no_antithetic(S0, K, r, q, sigma, T, n_sim, obs_freq="daily", option_type="call"):
    """
    Version BASIC PURE :
    - pas d'antithetic variates
    - pas de control variate
    """
    m_steps = get_m_steps(obs_freq)

    Z = box_muller(n_sim, m_steps)                     # pas de -Z
    S = simulate_paths(S0, r, q, sigma, T, n_sim, m_steps, Z)

    asian = asian_payoff(S, K, option_type)
    disc = np.exp(-r*T)

    price = disc * np.mean(asian)
    var = np.var(asian) * disc**2
    ic = (price - 1.96*np.sqrt(var/n_sim), price + 1.96*np.sqrt(var/n_sim))

    return price, var, ic


def price_antithetic_only(S0, K, r, q, sigma, T, n_sim, obs_freq="daily", option_type="call"):
    """
    Version :
    - antithetic variates
    - pas de control variate
    """
    m_steps = get_m_steps(obs_freq)

    Z = box_muller(n_sim, m_steps)
    Z_full = np.vstack([Z, -Z])
    S = simulate_paths(S0, r, q, sigma, T, 2*n_sim, m_steps, Z_full)

    asian = asian_payoff(S, K, option_type)
    disc = np.exp(-r*T)

    price = disc * np.mean(asian)
    var = np.var(asian) * disc**2
    ic = (price - 1.96*np.sqrt(var/(2*n_sim)), price + 1.96*np.sqrt(var/(2*n_sim)))

    return price, var, ic


def price_antithetic_control_variate(S0, K, r, q, sigma, T, n_sim, obs_freq="daily", option_type="call"):
    """
    Version COMPLÈTE :
    - antithetic variates
    - control variate
    """
    res = asian_option_pricer(S0, K, r, q, sigma, T, n_sim=n_sim, obs_freq=obs_freq, option_type=option_type)
    return res["Price CV"], res["Var CV"], res["IC CV"]


def compare_three_methods(S0, K, r, q, sigma, T, n_sim=50000, obs_freq="daily", option_type="call"):

    print("\n==============================")
    print(" COMPARAISON DES 3 MÉTHODES ")
    print("==============================")

    # BASIC PUR
    p_basic_pure, var_basic_pure, ic_basic_pure = price_no_antithetic(
        S0, K, r, q, sigma, T, n_sim, obs_freq, option_type
    )

    # ANTITHETIC SEUL
    p_anti, var_anti, ic_anti = price_antithetic_only(
        S0, K, r, q, sigma, T, n_sim, obs_freq, option_type
    )

    # ANTITHETIC + CONTROL VARIATE
    p_cv, var_cv, ic_cv = price_antithetic_control_variate(
        S0, K, r, q, sigma, T, n_sim, obs_freq, option_type
    )

    print("\n--- BASIC PUR (aucune réduction de variance) ---")
    print(f"Prix     = {p_basic_pure:.4f}")
    print(f"Variance = {var_basic_pure:.4f}")
    print(f"IC       = {ic_basic_pure}")

    print("\n--- ANTITHETIC SEULEMENT ---")
    print(f"Prix     = {p_anti:.4f}")
    print(f"Variance = {var_anti:.4f}   (↓ vs basic : {(1 - var_anti/var_basic_pure)*100:.1f}%)")
    print(f"IC       = {ic_anti}")

    print("\n--- ANTITHETIC + CONTROL VARIATE ---")
    print(f"Prix     = {p_cv:.4f}")
    print(f"Variance = {var_cv:.4f}      (↓ vs anti : {(1 - var_cv/var_anti)*100:.1f}%)")
    print(f"IC       = {ic_cv}")


# COURBE DE CONVERGENCE

def plot_convergence(S0, K, r, q, sigma, T):
    """
    Visualiser la convergence en fonction du nombre
    de simulations.
    """
    ns = [1000, 3000, 7000, 15000, 30000, 50000]
    prices = []

    for n in ns:
        res = asian_option_pricer(S0, K, r, q, sigma, T, n_sim=n)
        prices.append(res["Price CV"])

    plt.figure(figsize=(10,6))
    plt.plot(ns, prices, marker="o")
    plt.title("Convergence du prix (Control Variate)")
    plt.xlabel("Nombre de simulations")
    plt.ylabel("Prix asiatique")
    plt.grid(True)
    plt.show()


#HEATMAP (comparaison K,T )


def heatmap_prices(S0, r, q, sigma, strikes=[80,100,120], maturities=[0.5,1,2]):
    """
    Compare plusieurs strikes et maturités.
    """
    mat = np.zeros((len(strikes), len(maturities)))

    for i,K in enumerate(strikes):
        for j,T in enumerate(maturities):
            res = asian_option_pricer(S0, K, r, q, sigma, T, n_sim=20000)
            mat[i,j] = res["Price CV"]

    df = pd.DataFrame(mat, index=strikes, columns=maturities)

    plt.figure(figsize=(8,6))
    sns.heatmap(df, annot=True, cmap="viridis")
    plt.title("Heatmap du prix asiatique CV (K,T)")
    plt.xlabel("Maturité T")
    plt.ylabel("Strike K")
    plt.show()


# COMPARAISON ASIAN vs EURO SUR UNE GRILLE (K,T)


def compare_asian_euro_grid(S0, r, q, sigma,
                            strikes=[80, 100, 120],
                            maturities=[0.5, 1, 2],
                            n_sim=20000,
                            option_type="call"):
    """
    Compare Asian CV vs European BS pour plusieurs (K,T)
    """
    rows = []
    for K in strikes:
        for T in maturities:
            res_asian = asian_option_pricer(S0, K, r, q, sigma, T,
                                            n_sim=n_sim,
                                            obs_freq="daily",
                                            option_type=option_type)
            asian_price = res_asian["Price CV"]
            euro_price = bs_european_call_put(S0, K, r, q, sigma, T, option_type)
            rows.append({
                "K": K,
                "T": T,
                "Asian CV": asian_price,
                "Euro BS": euro_price,
                "Diff (Euro - Asian)": euro_price - asian_price
            })

    df = pd.DataFrame(rows)
    print("\n=== COMPARAISON ASIAN vs EURO SUR LA GRILLE (K,T) ===")
    print(df.to_string(index=False))
    return df


# CORRÉLATION 


def plot_correlation(S0, K, r, q, sigma, T):
    """
    Affiche la corrélation entre payoff asiatique et payoff européen.
    Plus elle est élevée, plus la méthode CV est efficace.
    """

    Z = box_muller(20000, 252)
    Z_full = np.vstack([Z, -Z])
    S_paths = simulate_paths(S0, r, q, sigma, T, 40000, 252, Z_full)

    asian = asian_payoff(S_paths, K)
    euro = european_payoff(S_paths, K)

    corr = np.corrcoef(asian, euro)[0,1]
    print("Corrélation payoff Asian/Euro :", corr)

    plt.figure(figsize=(8,6))
    sns.scatterplot(x=euro, y=asian, alpha=0.2)
    plt.title(f"Corrélation = {corr:.4f}")
    plt.xlabel("Payoff européen")
    plt.ylabel("Payoff asiatique")
    plt.show()


# BENCHMARK TEMPS 


def benchmark(S0, K, r, q, sigma, T):
    """
    Compare le temps d'exécution avec/sans variance reduction.
    """
    t0 = time.time()
    asian_option_pricer(S0, K, r, q, sigma, T, variance_reduction=False)
    t_basic = time.time()-t0

    t1 = time.time()
    asian_option_pricer(S0, K, r, q, sigma, T, variance_reduction=True)
    t_cv = time.time()-t1

    print("Temps Basic :", t_basic)
    print("Temps CV :", t_cv)
    print("Gain (%) :", 100*(1 - t_cv/t_basic))



# MAIN 


if __name__ == "__main__":

    S0, sigma, r, q, series = load_asset_parameters("AAPL")

    print("\n=== PARAMÈTRES ACTIF RÉEL (AAPL) ===")
    print("Spot =", S0)
    print("Sigma =", sigma)
    print("r =", r)
    print("q =", q)

    
    # Comparaison des 3 méthodes
    compare_three_methods(
        S0, K=180, r=r, q=q, sigma=sigma, T=1,
        n_sim=50000,
        obs_freq="daily",
        option_type="call"
    )

    print("\n=== PRICER PRINCIPAL ===")
    result = asian_option_pricer(S0, K=180, r=r, q=q, sigma=sigma, T=1,
                                 obs_freq="daily",
                                 option_type="call")
    print(result)

    print("\n=== CONVERGENCE ===")
    plot_convergence(S0, 180, r, q, sigma, 1)

    print("\n=== HEATMAP ===")
    heatmap_prices(S0, r, q, sigma)

    print("\n=== COMPARAISON ASIAN vs EURO (K,T) ===")
    compare_asian_euro_grid(S0, r, q, sigma)

    print("\n=== CORRÉLATION ===")
    plot_correlation(S0, 180, r, q, sigma, 1)

    print("\n=== BENCHMARK ===")
    benchmark(S0, 180, r, q, sigma, 1)
