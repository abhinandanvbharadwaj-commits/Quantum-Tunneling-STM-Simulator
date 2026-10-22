"""
Quantum Tunneling & STM Simulator - Physics Engine
=================================================
Core mathematical and analytical calculations for quantum barrier penetration,
transmission probability, and scanning tunneling microscopy (STM) current.
Directly aligns with Sections 13.5 & 13.6 of Quantum Mechanics / Engineering Physics.
"""

import numpy as np
from typing import Dict, Tuple, Any

# ==============================================================================
# PHYSICAL CONSTANTS (CODATA 2018 Recommended Values)
# ==============================================================================
HBAR = 1.054571817e-34       # Reduced Planck constant in J·s
M_E = 9.1093837015e-31       # Rest mass of electron in kg
EV_TO_JOULES = 1.602176634e-19  # Conversion factor: 1 eV in Joules
NM_TO_METERS = 1.0e-9        # Conversion factor: 1 nm in meters
ANGSTROM_TO_METERS = 1.0e-10 # Conversion factor: 1 Å in meters


def calculate_decay_constant(
    mass_ratio: float,
    energy_ev: float,
    barrier_height_ev: float
) -> Tuple[float, float, bool]:
    """
    Calculate the decay constant kappa (κ) in the barrier region.
    
    Formula:
        kappa = sqrt(2 * m * (V0 - E)) / hbar
        
    Parameters:
        mass_ratio: Particle mass in units of electron mass (m / m_e).
        energy_ev: Particle kinetic energy in electronvolts (eV).
        barrier_height_ev: Potential barrier height in electronvolts (eV).
        
    Returns:
        kappa_m: Decay constant in units of m^-1.
        kappa_nm: Decay constant in units of nm^-1.
        is_classical: True if E >= V0 (over-barrier classical transmission).
    """
    if energy_ev >= barrier_height_ev:
        # Classical transmission regime (E >= V0)
        return 0.0, 0.0, True

    mass_kg = mass_ratio * M_E
    delta_v_joules = (barrier_height_ev - energy_ev) * EV_TO_JOULES
    
    # kappa = sqrt(2 * m * delta_V) / hbar
    kappa_m = np.sqrt(2.0 * mass_kg * delta_v_joules) / HBAR
    kappa_nm = kappa_m * NM_TO_METERS
    
    return float(kappa_m), float(kappa_nm), False


def calculate_transmission_probability(
    kappa_nm: float,
    barrier_width_nm: float,
    is_classical: bool = False
) -> float:
    """
    Calculate the approximate transmission probability T through the potential barrier.
    
    Formula:
        T = exp(-2 * kappa * a)
        
    Parameters:
        kappa_nm: Decay constant in nm^-1.
        barrier_width_nm: Barrier width 'a' in nm.
        is_classical: Boolean flag indicating if E >= V0.
        
    Returns:
        T: Transmission probability in range [0.0, 1.0].
    """
    if is_classical:
        return 1.0

    exponent = -2.0 * kappa_nm * barrier_width_nm
    
    # Prevent numerical underflow for large negative exponents
    if exponent < -700.0:
        return 0.0
        
    t_val = np.exp(exponent)
    return float(np.clip(t_val, 0.0, 1.0))


def calculate_exact_transmission_probability(
    mass_ratio: float,
    energy_ev: float,
    barrier_height_ev: float,
    barrier_width_nm: float
) -> float:
    """
    Calculate the exact quantum mechanical transmission coefficient for a 1D rectangular barrier.
    
    Formula:
        T_exact = [1 + (V0^2 * sinh^2(kappa * a)) / (4 * E * (V0 - E))]^-1  for E < V0
        T_exact = [1 + (V0^2 * sin^2(k' * a)) / (4 * E * (E - V0))]^-1       for E > V0
        
    Returns:
        T_exact: Exact transmission coefficient in range [0.0, 1.0].
    """
    if energy_ev <= 0:
        return 0.0

    mass_kg = mass_ratio * M_E
    a_m = barrier_width_nm * NM_TO_METERS

    if energy_ev < barrier_height_ev:
        delta_v_j = (barrier_height_ev - energy_ev) * EV_TO_JOULES
        kappa = np.sqrt(2.0 * mass_kg * delta_v_j) / HBAR
        ka = kappa * a_m
        
        # Guard against overflow in sinh
        if ka > 100.0:
            # Asymptotic limit: T ~ 16 * E * (V0 - E) / (V0^2) * exp(-2 * ka)
            prefactor = 16.0 * energy_ev * (barrier_height_ev - energy_ev) / (barrier_height_ev**2)
            return float(np.clip(prefactor * np.exp(-2.0 * ka), 0.0, 1.0))
            
        sinh_ka = np.sinh(ka)
        denom = 1.0 + (barrier_height_ev**2 * sinh_ka**2) / (4.0 * energy_ev * (barrier_height_ev - energy_ev))
        return float(1.0 / denom)
        
    elif energy_ev > barrier_height_ev:
        delta_e_j = (energy_ev - barrier_height_ev) * EV_TO_JOULES
        k_prime = np.sqrt(2.0 * mass_kg * delta_e_j) / HBAR
        k_prime_a = k_prime * a_m
        sin_term = np.sin(k_prime_a)
        denom = 1.0 + (barrier_height_ev**2 * sin_term**2) / (4.0 * energy_ev * (energy_ev - barrier_height_ev))
        return float(1.0 / denom)
    else:
        # At E = V0: T = [1 + m * V0 * a^2 / (2 * hbar^2)]^-1
        v0_j = barrier_height_ev * EV_TO_JOULES
        val = 1.0 / (1.0 + (mass_kg * v0_j * a_m**2) / (2.0 * HBAR**2))
        return float(val)


def calculate_stm_current(
    kappa_nm: float,
    separation_nm: float,
    i0_na: float = 1.0,
    is_classical: bool = False
) -> float:
    """
    Calculate the qualitative STM tunneling current.
    
    Formula:
        I = I0 * exp(-2 * kappa * s)
        
    Parameters:
        kappa_nm: Decay constant in nm^-1.
        separation_nm: Tip-to-surface separation 's' in nm.
        i0_na: Reference contact current (at s=0) in nanoamperes (nA). Default = 1.0 nA.
        is_classical: Boolean flag indicating if E >= V0.
        
    Returns:
        Current I in nanoamperes (nA).
    """
    if is_classical:
        return float(i0_na)
        
    exponent = -2.0 * kappa_nm * separation_nm
    if exponent < -700.0:
        return 0.0
    return float(i0_na * np.exp(exponent))


def calculate_stm_relative_change(
    kappa_nm: float,
    delta_s_nm: float = 0.1,
    is_classical: bool = False
) -> Dict[str, float]:
    """
    Calculate the relative and percentage change in STM current for a displacement delta_s.
    Simulates atomic-step topographic feedback (e.g. 0.1 nm = 1 Ångström step).
    
    Formula:
        I(s + delta_s) / I(s) = exp(-2 * kappa * delta_s)
        Relative Change = [I(s + delta_s) - I(s)] / I(s) = exp(-2 * kappa * delta_s) - 1
        
    Returns:
        Dictionary containing:
            - ratio: I(s + delta_s) / I(s)
            - percent_change: ((I_new - I_old) / I_old) * 100%
            - drop_factor: I_old / I_new
            - sensitivity_per_angstrom: percentage change per 0.1 nm
    """
    if is_classical or kappa_nm <= 0.0:
        return {
            "ratio": 1.0,
            "percent_change": 0.0,
            "drop_factor": 1.0,
            "sensitivity_per_angstrom": 0.0
        }
        
    exponent = -2.0 * kappa_nm * delta_s_nm
    ratio = np.exp(exponent)
    percent_change = (ratio - 1.0) * 100.0
    drop_factor = 1.0 / ratio if ratio > 1e-15 else float('inf')
    
    return {
        "ratio": float(ratio),
        "percent_change": float(percent_change),
        "drop_factor": float(drop_factor),
        "sensitivity_per_angstrom": float(abs(percent_change))
    }


def compute_wavefunction_profile(
    mass_ratio: float,
    energy_ev: float,
    barrier_height_ev: float,
    barrier_width_nm: float,
    num_points_per_region: int = 400
) -> Dict[str, Any]:
    """
    Compute boundary-matched 1D wavefunction across three regions:
      - Region I: Incident + Reflected wave (x < 0)
      - Region II: Tunneling decay (0 <= x <= a)
      - Region III: Transmitted wave (x > a)
      
    Solves the continuous matching conditions at x = 0 and x = a:
      psi_I(0) = psi_II(0),   dpsi_I/dx(0) = dpsi_II/dx(0)
      psi_II(a) = psi_III(a), dpsi_II/dx(a) = dpsi_III/dx(a)
    """
    mass_kg = mass_ratio * M_E
    e_j = energy_ev * EV_TO_JOULES
    v0_j = barrier_height_ev * EV_TO_JOULES
    a_m = barrier_width_nm * NM_TO_METERS

    # Incident wavevector in Regions I & III (outside barrier)
    k1 = np.sqrt(2.0 * mass_kg * e_j) / HBAR

    # Display window settings
    left_width_nm = max(0.8, barrier_width_nm * 1.2)
    right_width_nm = max(0.8, barrier_width_nm * 1.2)

    x_I = np.linspace(-left_width_nm, 0.0, num_points_per_region, endpoint=False)
    x_II = np.linspace(0.0, barrier_width_nm, num_points_per_region, endpoint=True)
    x_III = np.linspace(barrier_width_nm, barrier_width_nm + right_width_nm, num_points_per_region, endpoint=True)

    if energy_ev < barrier_height_ev:
        # Tunneling regime
        kappa = np.sqrt(2.0 * mass_kg * (v0_j - e_j)) / HBAR
        
        # Solve for amplitudes: [R, C, D, F]
        # psi_I(x) = exp(i*k1*x) + R*exp(-i*k1*x)
        # psi_II(x) = C*exp(-kappa*x) + D*exp(kappa*x)
        # psi_III(x) = F*exp(i*k1*(x - a))
        #
        # Matching equations:
        # 1 + R = C + D
        # i*k1*(1 - R) = -kappa*C + kappa*D
        # C*exp(-kappa*a) + D*exp(kappa*a) = F
        # -kappa*C*exp(-kappa*a) + kappa*D*exp(kappa*a) = i*k1*F
        
        ka = kappa * a_m
        # Clamp ka to prevent matrix singularity with extreme numbers
        ka_clamped = min(ka, 60.0)
        e_neg = np.exp(-ka_clamped)
        e_pos = np.exp(ka_clamped)

        M = np.array([
            [-1.0, 1.0, 1.0, 0.0],
            [1j * k1, kappa, -kappa, 0.0],
            [0.0, e_neg, e_pos, -1.0],
            [0.0, -kappa * e_neg, kappa * e_pos, -1j * k1]
        ], dtype=complex)

        b = np.array([1.0, 1j * k1, 0.0, 0.0], dtype=complex)
        
        try:
            sol = np.linalg.solve(M, b)
            R, C, D, F = sol[0], sol[1], sol[2], sol[3]
        except np.linalg.LinAlgError:
            # Fallback approximation for extreme barrier widths
            R = -1.0 + 0j
            C = 1.0 + 0j
            D = 0.0 + 0j
            F = np.exp(-ka_clamped) + 0j

        # Compute wavefunctions in meters
        x_I_m = x_I * NM_TO_METERS
        x_II_m = x_II * NM_TO_METERS
        x_III_m = x_III * NM_TO_METERS

        psi_I = np.exp(1j * k1 * x_I_m) + R * np.exp(-1j * k1 * x_I_m)
        psi_II = C * np.exp(-kappa * x_II_m) + D * np.exp(kappa * x_II_m)
        psi_III = F * np.exp(1j * k1 * (x_III_m - a_m))

    else:
        # Classical Over-Barrier Regime (E >= V0)
        delta_e = max((e_j - v0_j), 1e-25)
        k2 = np.sqrt(2.0 * mass_kg * delta_e) / HBAR
        
        k2_a = k2 * a_m
        e_neg = np.exp(-1j * k2_a)
        e_pos = np.exp(1j * k2_a)

        M = np.array([
            [-1.0, 1.0, 1.0, 0.0],
            [1j * k1, -1j * k2, 1j * k2, 0.0],
            [0.0, e_pos, e_neg, -1.0],
            [0.0, 1j * k2 * e_pos, -1j * k2 * e_neg, -1j * k1]
        ], dtype=complex)

        b = np.array([1.0, 1j * k1, 0.0, 0.0], dtype=complex)
        try:
            sol = np.linalg.solve(M, b)
            R, C, D, F = sol[0], sol[1], sol[2], sol[3]
        except np.linalg.LinAlgError:
            R, C, D, F = 0j, 1.0 + 0j, 0j, 1.0 + 0j

        x_I_m = x_I * NM_TO_METERS
        x_II_m = x_II * NM_TO_METERS
        x_III_m = x_III * NM_TO_METERS

        psi_I = np.exp(1j * k1 * x_I_m) + R * np.exp(-1j * k1 * x_I_m)
        psi_II = C * np.exp(1j * k2 * x_II_m) + D * np.exp(-1j * k2 * x_II_m)
        psi_III = F * np.exp(1j * k1 * (x_III_m - a_m))

    # Concatenate coordinates and wavefunctions
    x_all = np.concatenate([x_I, x_II, x_III])
    psi_all = np.concatenate([psi_I, psi_II, psi_III])
    prob_density = np.abs(psi_all)**2
    real_psi = np.real(psi_all)

    # Potential barrier profile V(x)
    v_profile = np.zeros_like(x_all)
    v_profile[(x_all >= 0.0) & (x_all <= barrier_width_nm)] = barrier_height_ev

    return {
        "x": x_all,
        "psi_real": real_psi,
        "prob_density": prob_density,
        "potential": v_profile,
        "x_I": x_I,
        "x_II": x_II,
        "x_III": x_III,
        "psi_I_real": np.real(psi_I),
        "psi_II_real": np.real(psi_II),
        "psi_III_real": np.real(psi_III),
        "barrier_width_nm": barrier_width_nm,
        "barrier_height_ev": barrier_height_ev,
        "energy_ev": energy_ev,
        "reflection_coeff": float(np.abs(R)**2),
        "transmission_coeff": float(np.abs(F)**2)
    }
