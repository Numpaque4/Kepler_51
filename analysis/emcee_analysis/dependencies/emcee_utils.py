"""
emcee_utils.py - Utilidades para adaptación del muestreo por rechazo a emcee

Este módulo encapsula el modelo estadístico del efecto PhotoRing para su uso con emcee.
Preserva completamente el modelo físico y astrofísico original de los notebooks
mcra-planet-*.ipynb de Zuluaga_PhotoRing.

Correspondencia con notebooks originales:
-----------------------------------------
Método original: Muestreo por rechazo (rejection sampling)
    - alpha = p_rho_obs * p_delta / (p_rho_obs_max * p_delta_max)
    - Acepta si u < alpha, donde u ~ Uniform(0,1)

Adaptación emcee:
    - log_prior: Priors uniformes en rangos definidos
    - log_likelihood: log(p_rho_obs * p_delta)
    - log_probability: log_prior + log_likelihood

Autores: Sebastian Numpaque-Rodriguez, Jorge I. Zuluaga, Jaime Alvarado-Montes, David Kipping
"""

import numpy as np
from scipy.stats import norm
from copy import deepcopy

# ============================================================================
# FUNCIONES DEL MODELO ESTADÍSTICO
# ============================================================================

def log_prior(theta, props, bounds_check=True):
    """
    Calcula el log-prior para los parámetros.
    
    El método original usa priors uniformes implícitos:
        np.random.uniform(vals['range'][0], vals['range'][1])
    
    Parámetros:
    -----------
    theta : array-like
        Vector de parámetros en el orden definido por props
    props : dict
        Diccionario de propiedades de parámetros con 'range' y 'scale'
    bounds_check : bool
        Si True, verifica límites y retorna -inf fuera de ellos
    
    Retorna:
    --------
    float : log(prior), 0.0 si dentro de límites, -inf si fuera
    """
    param_names = list(props.keys())
    
    for i, (name, vals) in enumerate(props.items()):
        value = theta[i]
        low, high = vals['range']
        
        if bounds_check and (value < low or value > high):
            return -np.inf
    
    # Prior uniforme: log(1/(b-a)) constante, podemos omitirlo
    # ya que no afecta la proporción de aceptación en MCMC
    return 0.0


def log_likelihood(theta, S_base, props, store, adjust_func, verbose=False):
    """
    Calcula el log-likelihood para los parámetros dados.
    
    Correspondencia con método original:
    ------------------------------------
    Original: p_rho_obs * p_delta
    Emcee: log(p_rho_obs) + log(p_delta)
    
    Donde:
        p_rho_obs = S.rho_obs_fun(rho_obs)  # Función interpolada de datos
        p_delta = norm.pdf(delta, delta_mean, delta_std)  # Gaussiana
    
    Parámetros:
    -----------
    theta : array-like
        Vector de parámetros [fe, Rplanet, ir, phir, ...] según props
    S_base : RingedSystem
        Sistema base con configuración inicial (noauto=True)
    props : dict
        Definición del espacio de parámetros
    store : dict
        Parámetros a almacenar y sus escalas
    adjust_func : callable
        Función de ajuste de parámetros derivados (adjust_params)
    verbose : bool
        Si True, imprime información de depuración
    
    Retorna:
    --------
    float : log-likelihood
    dict : Diccionario con parámetros almacenados (observables)
    """
    # Crear copia del sistema para modificación segura (thread-safe)
    S = deepcopy(S_base)
    S.noauto = True
    
    # Asignar parámetros al sistema
    param_names = list(props.keys())
    for i, (name, vals) in enumerate(props.items()):
        value = theta[i] * vals['scale']
        setattr(S, name, value)
    
    # Ajustar parámetros derivados (semi-eje mayor, inclinación orbital)
    adjust_func(S)
    
    # Actualizar sistema y calcular PhotoRing
    S.updateSystem()
    S.calculate_PR()
    
    # Extraer parámetros almacenados
    spars = {}
    for sprop, vals in store.items():
        spars[sprop] = getattr(S, vals['prop']) * vals['scale']
    
    # Calcular probabilidades (mismo cálculo que original)
    p_rho_obs = float(S.rho_obs_fun(spars['rho_obs']))
    p_delta = float(S.delta_fun(spars['delta']))
    
    if verbose:
        print(f"theta: {theta}")
        print(f"rho_obs: {spars['rho_obs']}, p_rho_obs: {p_rho_obs}")
        print(f"delta: {spars['delta']}, p_delta: {p_delta}")
    
    # Evitar log(0)
    if p_rho_obs <= 0 or p_delta <= 0:
        return -np.inf, spars
    
    # Log-likelihood
    logl = np.log(p_rho_obs) + np.log(p_delta)
    
    return logl, spars


def log_probability(theta, S_base, props, store, adjust_func):
    """
    Calcula el log-posterior (log-prior + log-likelihood).
    
    Esta es la función principal que emcee llama en cada paso.
    
    Parámetros:
    -----------
    theta : array-like
        Vector de parámetros
    S_base : RingedSystem
        Sistema base
    props : dict
        Definición del espacio de parámetros
    store : dict
        Parámetros a almacenar
    adjust_func : callable
        Función de ajuste
    
    Retorna:
    --------
    float : log-posterior
    """
    lp = log_prior(theta, props)
    if not np.isfinite(lp):
        return -np.inf
    
    ll, _ = log_likelihood(theta, S_base, props, store, adjust_func)
    
    if not np.isfinite(ll):
        return -np.inf
    
    return lp + ll


def log_probability_blobs(theta, S_base, props, store, adjust_func):
    """
    Versión de log_probability que también retorna los blobs (observables).
    
    Útil para almacenar parámetros derivados junto con las cadenas MCMC.
    
    Retorna:
    --------
    tuple : (log-posterior, dict de observables)
    """
    lp = log_prior(theta, props)
    if not np.isfinite(lp):
        return -np.inf, {}
    
    ll, spars = log_likelihood(theta, S_base, props, store, adjust_func)
    
    if not np.isfinite(ll):
        return -np.inf, {}
    
    return lp + ll, spars


# ============================================================================
# FUNCIÓN WRAPPER PARA PARALELIZACIÓN
# ============================================================================

def make_log_prob_func(S_base, props, store, adjust_func, return_blobs=False):
    """
    Crea una función de log-probability compatible con multiprocessing.
    
    IMPORTANTE: Esta función crea un closure que encapsula los argumentos
    fijos, haciendo la función picklable para Pool.map().
    
    Uso:
    ----
    log_prob = make_log_prob_func(S, props, store, adjust_params)
    with Pool() as pool:
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob, pool=pool)
    
    Parámetros:
    -----------
    S_base : RingedSystem
        Sistema base (será copiado internamente)
    props : dict
        Espacio de parámetros
    store : dict
        Parámetros a almacenar
    adjust_func : callable
        Función de ajuste
    return_blobs : bool
        Si True, retorna observables como blobs
    
    Retorna:
    --------
    callable : Función log_prob(theta) lista para emcee
    """
    # Crear copia profunda del sistema base
    S_copy = deepcopy(S_base)
    
    if return_blobs:
        def log_prob(theta):
            return log_probability_blobs(theta, S_copy, props, store, adjust_func)
    else:
        def log_prob(theta):
            return log_probability(theta, S_copy, props, store, adjust_func)
    
    return log_prob


# ============================================================================
# UTILIDADES PARA INICIALIZACIÓN DE WALKERS
# ============================================================================

def initialize_walkers(nwalkers, props, scatter=0.1, seed=None):
    """
    Inicializa posiciones de walkers en el espacio de parámetros.
    
    Parámetros:
    -----------
    nwalkers : int
        Número de walkers
    props : dict
        Espacio de parámetros con 'range' y 'default' (opcional)
    scatter : float
        Fracción del rango para dispersión inicial
    seed : int
        Semilla para reproducibilidad
    
    Retorna:
    --------
    ndarray : Posiciones iniciales (nwalkers, ndim)
    """
    if seed is not None:
        np.random.seed(seed)
    
    ndim = len(props)
    p0 = np.zeros((nwalkers, ndim))
    
    for i, (name, vals) in enumerate(props.items()):
        low, high = vals['range']
        center = (low + high) / 2
        width = (high - low) * scatter
        
        # Usar default si está disponible
        if 'default' in vals:
            center = vals['default']
        
        p0[:, i] = center + np.random.uniform(-width, width, nwalkers)
        
        # Asegurar que estén dentro de límites
        p0[:, i] = np.clip(p0[:, i], low, high)
    
    return p0


def samples_to_dataframe(sampler, props, burn_in=0, thin=1):
    """
    Convierte las cadenas MCMC a un DataFrame de pandas.
    
    Parámetros:
    -----------
    sampler : emcee.EnsembleSampler
        Sampler ejecutado
    props : dict
        Espacio de parámetros
    burn_in : int
        Pasos iniciales a descartar
    thin : int
        Factor de adelgazamiento
    
    Retorna:
    --------
    DataFrame : Muestras con columnas nombradas
    """
    import pandas as pd
    
    # Obtener cadenas aplanadas
    flat_samples = sampler.get_chain(discard=burn_in, thin=thin, flat=True)
    
    # Crear DataFrame
    columns = list(props.keys())
    df = pd.DataFrame(flat_samples, columns=columns)
    
    return df


def compute_derived_quantities(df, S_base, props, store, adjust_func, verbose=True):
    """
    Calcula cantidades derivadas para un DataFrame de muestras.
    
    Parámetros:
    -----------
    df : DataFrame
        DataFrame con parámetros muestreados
    S_base : RingedSystem
        Sistema base
    props : dict
        Espacio de parámetros
    store : dict
        Parámetros derivados a calcular
    adjust_func : callable
        Función de ajuste
    verbose : bool
        Si True, muestra barra de progreso
    
    Retorna:
    --------
    DataFrame : DataFrame ampliado con cantidades derivadas
    """
    from tqdm import tqdm
    import pandas as pd
    
    # Preparar columnas para resultados
    store_cols = list(store.keys())
    results = {col: [] for col in store_cols}
    
    iterator = df.iterrows()
    if verbose:
        iterator = tqdm(iterator, total=len(df), desc="Computing derived quantities")
    
    for _, row in iterator:
        theta = [row[col] for col in props.keys()]
        _, spars = log_likelihood(theta, S_base, props, store, adjust_func)
        
        for col in store_cols:
            results[col].append(spars.get(col, np.nan))
    
    # Añadir al DataFrame
    for col in store_cols:
        df[col] = results[col]
    
    return df


# ============================================================================
# DIAGNÓSTICOS
# ============================================================================

def compute_acceptance_fraction(sampler):
    """
    Calcula la fracción de aceptación del sampler.
    
    Retorna la fracción promedio y por walker.
    """
    acceptance = sampler.acceptance_fraction
    return {
        'mean': np.mean(acceptance),
        'std': np.std(acceptance),
        'min': np.min(acceptance),
        'max': np.max(acceptance),
        'per_walker': acceptance
    }


def compute_autocorr_time(sampler, quiet=True):
    """
    Estima el tiempo de autocorrelación.
    
    Retorna None si la cadena es demasiado corta.
    """
    try:
        tau = sampler.get_autocorr_time(quiet=quiet)
        return {
            'tau': tau,
            'mean': np.mean(tau),
            'effective_samples': sampler.flatchain.shape[0] / np.mean(tau)
        }
    except Exception as e:
        return {'error': str(e), 'tau': None}


def convergence_summary(sampler, burn_in=0):
    """
    Resumen de diagnósticos de convergencia.
    """
    acceptance = compute_acceptance_fraction(sampler)
    autocorr = compute_autocorr_time(sampler)
    
    chain = sampler.get_chain(discard=burn_in)
    
    return {
        'nsteps': chain.shape[0],
        'nwalkers': chain.shape[1],
        'ndim': chain.shape[2],
        'acceptance_fraction': acceptance,
        'autocorrelation': autocorr
    }
