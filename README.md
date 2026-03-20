# Kepler-51b Ringed Exoplanet Research Project

## Project Overview

This research project investigates the possibility that the anomalous properties of Kepler-51 planets, particularly Kepler-51b, may be explained by the presence of planetary rings rather than being intrinsically ultra-low-density "super-puff" planets. The project employs asterodensity profiling and the PhotoRing effect to identify and characterize potential ring systems.

**Primary Authors**: Sebastián Numpaque, Jorge I. Zuluaga, Jaime A. Alvarado-Montes, David Kipping

**Affiliations**:
- SEAP/FACom, Instituto de Física - FCEN, Universidad de Antioquia, Colombia
- Australian Astronomical Optics & Astrophysics and Space Technologies Research Centre, Macquarie University
- Columbia University

## Scientific Background

### The PhotoRing Effect

The **PhotoRing (PR) effect** is a systematic bias in transit-derived stellar density caused by unmodeled ring systems. When a ringed planet transits its host star:

1. **Increased Transit Depth**: The projected area of rings increases the observed transit depth δ, leading to overestimated planetary radius
2. **Modified Contact Times**: Rings extend transit duration T14 (earlier first contact, later fourth contact) and reduce full-transit duration T23
3. **Biased Stellar Density**: These geometric distortions propagate through transit fitting, causing ρ_star,obs < ρ_star,true

This negative deviation distinguishes rings from other effects like:
- **PhotoEccentric**: produces positive deviation due to eccentric orbits
- **PhotoBlend**: caused by unresolved stellar companions
- **PhotoSpot**: from unocculted stellar spots

### Kepler-51 System

Kepler-51 hosts four known transiting planets (b, c, d, and recently discovered e), all with exceptionally low densities (ρ < 0.1 g/cm³). The system characteristics:

**Stellar Properties**:
- Mass: M_star = 0.915 ± 0.050 M_sun
- Radius: R_star = 0.869 ± 0.029 R_sun
- True stellar density: ρ_true from asteroseismology/spectroscopy

**Kepler-51b Properties** (Masuda et al. 2024):
- Orbital period: P = 45.154 ± 0.0004 days
- Planetary radius: R_p = 0.609 ± 0.012 R_jup (observed, possibly inflated by rings)
- Planetary mass: M_p = 0.011 ± 0.007 M_jup (from TTVs)
- Impact parameter: b = 0.074 ± 0.072
- Orbital inclination: i_orb ≈ 89.93°

**Minimum Physical Radius**: R_p,min = 0.138 R_jup (assuming maximum density for M_p)

## Project Structure

```
Zuluaga_etal_kepler51b/
├── Overleaf/698b538e174868a77302d5f6/
│   └── main.tex                          # Draft manuscript (AASTeX format)
│
├── Zuluaga_PhotoRing/                    # Core analysis directory
│   ├── GeoTrans/
│   │   ├── geotrans2.py                  # Main library for ringed-planet transit modeling
│   │   ├── system.py                     # System configuration classes
│   │   ├── lightcurve.py                 # Light curve computation
│   │   └── photoring.py                  # PhotoRing effect calculations
│   │
│   ├── algorithm-ring-development.ipynb  # Algorithm development notebook
│   ├── algorithm-ring-implementation.ipynb # Full algorithm implementation
│   ├── mcra-planet-b.ipynb              # MCMC analysis for Kepler-51b
│   ├── mcra-planet-c.ipynb              # MCMC analysis for Kepler-51c
│   ├── mcra-planet-d.ipynb              # MCMC analysis for Kepler-51d
│   └── legacy/                          # Previous versions and tests
│
├── analysis/                            # Additional analysis scripts
│   ├── notebooks/                       # Analysis notebooks
│   └── emcee_analysis/                  # EMCEE MCMC implementation
│
├── bibliography/
│   ├── papers/                          # Reference papers
│   │   ├── Zuluaga_2015_ApJL_803_L14.pdf  # Original PhotoRing paper
│   │   ├── Kipping_2014_AP.pdf            # Asterodensity profiling
│   │   └── Seager_2003_ApJ_585_1038.pdf   # Transit theory fundamentals
│   └── AI_review/                       # AI-assisted literature review
│
└── data/                                # Observational data (currently empty)
```

## Key Computational Components

### GeoTrans Library (geotrans2.py)

The core numerical library for modeling ringed exoplanet transits. Key features:

**Physical Constants**:
```python
RJUP = 69911.0 km       # Jupiter radius
MJUP = 1.898e27 kg      # Jupiter mass
RSUN = 696342.0 km      # Solar radius
MSUN = 1.98855e30 kg    # Solar mass
AU = 149597871.0 km     # Astronomical unit
GCONST = 6.674e-11      # Gravitational constant
```

**Core Classes**:
- `RingedSystem`: Main class for ringed planet-star systems
- `Point`, `Figure`: Geometric primitives for transit calculations
- Transit geometry and area computation methods
- PhotoRing effect calculation: `calculate_PR()`

**Key Parameters**:
- `Mstar`, `Rstar`: Stellar mass and radius
- `Rplanet`, `Mplanet`: Planetary mass and radius
- `ap`: Semi-major axis
- `iorb`: Orbital inclination
- `fe`, `fi`: Ring outer/inner radius (in units of Rp)
- `ir`: Ring inclination relative to orbit
- `phir`: Ring roll angle (azimuthal orientation)
- `tau`: Ring optical depth/opacity

### MCMC Sampling Methodology

**Algorithm**: Monte Carlo Rejection-Acceptance (MCRA) with parallel processing

**Sampled Parameters** (typical configuration):
1. `fe`: Ring outer radius factor [1.1, 10.0] × R_p
2. `Rplanet`: Physical planetary radius [R_p,min, R_p,obs]
3. `ir`: Ring inclination [0°, 90°]
4. `phir`: Ring roll angle [0°, 90°]
5. `tau`: Ring opacity [2.0, 10.0] (optional)

**Target Distributions**:
- `p(ρ_obs)`: Observed stellar density from transit fitting
- `p(δ)`: Transit depth distribution (Gaussian around measured value)
- Acceptance probability: α = p(ρ_obs) × p(δ) / (p_max,ρ × p_max,δ)

**Stellar Grid**: 5×5 grid in (M_star, R_star) space with multivariate Gaussian weights accounting for mass-radius correlation (ρ_MR = -0.2)

**Derived Quantities**:
- `ieff`: Effective ring inclination (apparent, in sky plane)
- `teff`: Effective ring tilt angle
- `PR`: PhotoRing effect magnitude = (ρ_obs - ρ_true) / ρ_true
- `delta`: Normalized transit depth = Area_ring / π

### Key Notebooks

#### mcra-planet-b.ipynb
**Purpose**: Parameter estimation for Kepler-51b ring system

**Workflow**:
1. Load stellar density distributions (true vs observed)
2. Define parameter space and priors
3. Run parallel MCMC sampling across stellar parameter grid
4. Generate corner plots and posterior distributions
5. Identify maximum likelihood ring configuration

**Key Functions**:
- `mcra_grid_general()`: Core MCMC sampling routine
- `parallel_mcra_grid()`: Parallel execution wrapper
- `plotSample()`: Visualization of posteriors
- `get_maximum_kde()`: Find peak probability configuration
- `adjust_params()`: Ensure orbital consistency

**Output**: CSV files with samples in `tmp/ringed_sample-*.csv`

#### algorithm-ring-implementation.ipynb & algorithm-ring-development.ipynb
**Purpose**: Development and testing of ringed transit algorithms

**Content**:
- Mathematical formulation of asterodensity profiling
- PhotoRing effect physics and statistics
- Bayesian framework for ring parameter inference
- Validation tests and sensitivity analysis

## Physical Model Details

### Asterodensity Profiling Equations

**Stellar Density from Transits** (Seager & Mallén-Ornelas 2003):
```
ρ_star,obs = (3π / GP²) × (a/R_star)³_obs
```

**Scaled Semi-major Axis**:
```
(a/R_star)²_obs = [(1 + √δ)² - b²_obs(1 - sin²(πT14/P))] / sin²(πT14/P)
```

**Impact Parameter**:
```
b²_obs = [(1 - √δ)² - sin²(πT23/P)/sin²(πT14/P) × (1 + √δ)²] /
         [1 - sin²(πT23/P)/sin²(πT14/P)]
```

Where:
- T14: Total transit duration (first to fourth contact)
- T23: Full transit duration (second to third contact)
- δ: Transit depth (fractional flux)
- P: Orbital period

### Ring System Geometry

**Effective Angles**:
- `ieff`: Apparent ring inclination in sky plane
- `teff`: Effective tilt determines projected ellipse orientation

**Physical Constraints**:
- Rings must lie within planetary Roche limit (gravitational stability)
- Opacity τ ≥ 1 for detectable photometric signatures
- Ring inner edge typically fi = 1 (at planetary surface)

## Data Files

### Input Data
- `rho_true_fun.pkl`: Interpolated true stellar density PDF
- `rho_obs_b_fun.pkl`: Observed stellar density for Kepler-51b
- `rho_obs_c_fun.pkl`: Observed stellar density for Kepler-51c
- `rho_obs_d_fun.pkl`: Observed stellar density for Kepler-51d
- `GKTHCatalog_Table4.csv`: Stellar parameters from Gaia-Kepler catalog

### Output Data (in `tmp/` and `figures/`)
- `ringed_sample-*.csv`: MCMC posterior samples
- Corner plots showing parameter degeneracies
- Target distribution comparisons (ρ_obs, ρ_true, δ)

## Key Results (Preliminary)

### Best-fit Configuration for Kepler-51b

**Scenario 1: Fixed Minimum Radius** (R_p = R_p,min = 0.138 R_jup)
- Ring outer radius: fe ≈ 6.5 R_p
- Ring inclination: ir ≈ 75°
- Ring roll: phir ≈ 57°
- Effective inclination: ieff ≈ 58°
- Transit depth: δ ≈ 0.5%
- Acceptance rate: moderate efficiency

**Scenario 2: Free Planetary Radius** (R_p variable)
- Planetary radius: R_p ≈ 0.52 R_jup
- Ring outer radius: fe ≈ 2.4 R_p
- Ring inclination: ir ≈ 78°
- Ring roll: phir ≈ 83°
- Ring contributes significant projected area beyond planetary disk

Both scenarios produce observed stellar density consistent with ρ_obs while maintaining physical plausibility.

## Software Dependencies

### Python Packages
- **Core**: `numpy`, `scipy`, `matplotlib`
- **MCMC**: Custom implementation with `multiprocess` for parallelization
- **Statistics**: `pandas`, `scipy.stats`, `gaussian_kde`
- **Fitting** (optional): `lmfit`, `emcee`
- **Notebooks**: `jupyter`, `ipywidgets`, `tqdm`

### External Tools
- **Pryngles**: Forward modeling package for ringed planet photometry (reflected light, polarization)
- **AASTeX 7.0.1**: LaTeX template for manuscript preparation

## Workflow Guide

### Running MCMC Analysis

1. **Prepare Input Data**:
   ```python
   # Load density distributions
   with open('rho_true_fun.pkl', 'rb') as f:
       rho_true_fun = pickle.load(f)
   with open('rho_obs_b_fun.pkl', 'rb') as f:
       rho_obs_b_fun = pickle.load(f)
   ```

2. **Configure System**:
   ```python
   System = RingedSystem(
       system = dict(
           Mstar=Ms_mean, Rstar=Rs_mean,
           Rplanet=Rp_mean, Mplanet=Mp_mean,
           ap=ap_mean, iorb=iorb_mean*DEG,
           fe=1, fi=1, ir=0.0*DEG, phir=0.0*DEG, tau=1.0
       )
   )
   ```

3. **Define Parameter Space**:
   ```python
   props = dict(
       fe = dict(label=r"$f_e$", range=[1.1, 10.0], scale=1),
       Rplanet = dict(label=r"$R_p$", range=[Rp_min, Rp_max], scale=RJUP),
       ir = dict(label=r"$i_r$", range=[0.0, 90.0], scale=DEG),
       phir = dict(label=r"$\phi_r$", range=[0.0, 90.0], scale=DEG),
   )
   ```

4. **Run Parallel MCMC**:
   ```python
   Ns = 10000  # Total samples
   Nw = 8      # Number of parallel workers
   results = parallel_mcra_grid(S, props, store_params, adjust_params, Nw, Ns)
   ```

5. **Analyze Results**:
   ```python
   # Find maximum likelihood configuration
   peak_point = get_maximum_kde(results, props)

   # Generate diagnostic plots
   plotSample(results, S, props, prefix="kepler51b")
   ```

### Manuscript Compilation

```bash
cd Overleaf/698b538e174868a77302d5f6/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Important Notes for AI Assistant

### Code Style
- Heavy use of global constants (RJUP, MSUN, DEG, etc.)
- Object-oriented design with `RingedSystem` class
- Functional approach for MCMC sampling
- Parallel processing using `multiprocess` library

### Physical Assumptions
- Circular orbits (e_orb = 0) for Kepler-51 planets
- Nearly edge-on transits (i_orb ≈ 90°)
- Limb darkening can be neglected for initial analysis
- Ring particles are optically thin/thick depending on τ
- Ring is geometrically thin (negligible vertical extent)

### Numerical Tolerances
```python
ZERO = finfo(float).eps        # Machine precision
INTERTOL = 1e-10              # Intersection point tolerance
INTERFUNTOL = 1e-3            # Intersection function tolerance
ANGLETOL = 3°                 # Angle detection tolerance
NORINGTOL = 1e-5              # Ring rejection threshold
```

### Common Pitfalls
1. **Unit Consistency**: Always multiply by appropriate constants (RJUP, DEG, etc.)
2. **Parameter Adjustment**: Call `adjust_params(S)` after modifying orbital parameters
3. **System Updates**: Call `S.updateSystem()` before `S.calculate_PR()`
4. **Parallel Safety**: Use `deepcopy(System)` before parallel execution
5. **File Paths**: Code uses relative paths; run from `Zuluaga_PhotoRing/` directory

### Research Context
- This is a **draft manuscript** in preparation - conclusions are preliminary
- Results require peer review and validation
- Alternative explanations for super-puff planets (extended atmospheres, mass loss) remain viable
- Detection confidence depends on independent confirmation (e.g., spectroscopy, high-resolution imaging)

## Future Directions

### Observational Follow-up
- **JWST**: Infrared spectroscopy for atmospheric characterization
- **PLATO**: Detection of additional ringed cold Jupiters
- **ARIEL**: Spectral characterization of ring composition
- **High-contrast Imaging**: Direct detection of ring signatures
- **Polarimetry**: Ring-induced polarization signals (Veenstra et al. 2025)

### Computational Extensions
1. Extend to Kepler-51c and 51d with similar methodology
2. Incorporate Pryngles forward modeling for reflected light predictions
3. Bayesian model comparison: ringed vs ringless scenarios
4. Include eccentricity and non-zero impact parameters
5. Limb darkening effects on PhotoRing signature

### Theoretical Investigations
- Ring formation mechanisms at 0.24 AU (tidal disruption?)
- Long-term stability of ring systems in Kepler-51 environment
- Relationship between ring presence and planetary composition
- Population-level predictions: "how common are ringed exoplanets?"

## Related Publications

**Core References**:
- Zuluaga et al. (2015, ApJL, 803, L14): Original PhotoRing effect paper
- Kipping (2014): Asterodensity profiling methodology
- Seager & Mallén-Ornelas (2003): Transit density relations
- Masuda et al. (2024): Kepler-51 system characterization & 4th planet discovery

**Relevant Context**:
- Barnes & Fortney (2004): Detectability of Saturn-like rings
- Akinsanmi et al. (2020): HIP 41378 f as ringed planet candidate
- Libby-Roberts et al. (2020, 2025): Kepler-51 atmospheric studies
- Veenstra et al. (2025): Polarimetric signatures of rings

## Contact Information

For questions about this research:
- **Sebastián Numpaque**: david.rodriguez1@udea.edu.co
- **Jorge I. Zuluaga**: jorge.zuluaga@udea.edu.co
- **Jaime A. Alvarado-Montes**: jaime-andres.alvarado-montes@hdr.mq.edu.au
- **David Kipping**: dkipping@astro.columbia.edu

---

**Last Updated**: 2026-03-18
**Project Status**: Manuscript in preparation, preliminary analysis complete
**Code Repository**: Local Dropbox folder (not yet public)
