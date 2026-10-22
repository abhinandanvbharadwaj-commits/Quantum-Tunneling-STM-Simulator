"""
Automated Test Suite for Quantum Tunneling & STM Simulator
==========================================================
Verifies physics engine accuracy, boundary continuity, edge cases, and plot generation.
"""

import numpy as np
import physics_engine as pe
import visualization as viz

def test_decay_constant():
    # m = 1.0 m_e, E = 2.0 eV, V0 = 5.0 eV (Delta V = 3.0 eV)
    # Expected kappa ~ 8.87 nm^-1
    km, knm, is_classical = pe.calculate_decay_constant(1.0, 2.0, 5.0)
    assert not is_classical, "Should not be classical for E < V0"
    assert 8.85 < knm < 8.90, f"Expected kappa_nm ~ 8.87, got {knm}"
    print(f"[OK] Decay constant test passed: kappa = {knm:.4f} nm^-1")

def test_classical_edge_case():
    # E >= V0
    km, knm, is_classical = pe.calculate_decay_constant(1.0, 6.0, 5.0)
    assert is_classical, "Should be flagged as classical when E >= V0"
    assert knm == 0.0, "Decay constant should be 0 in classical regime"
    
    t_prob = pe.calculate_transmission_probability(knm, 0.5, is_classical=True)
    assert t_prob == 1.0, "Transmission probability should be capped at 1.0"
    print("[OK] Classical edge-case test passed: T = 1.0, is_classical = True")

def test_stm_sensitivity():
    # kappa ~ 8.87 nm^-1, delta_s = 0.1 nm (1 Angstrom)
    # 2 * kappa * delta_s ~ 2 * 8.874 * 0.1 = 1.7747
    # exp(-1.7747) ~ 0.1695
    # drop ~ -83%
    res = pe.calculate_stm_relative_change(8.8736, delta_s_nm=0.1)
    assert -84.0 < res["percent_change"] < -82.0, f"Expected ~ -83%, got {res['percent_change']}"
    assert 5.8 < res["drop_factor"] < 6.0, f"Expected ~ 5.9x drop, got {res['drop_factor']}"
    print(f"[OK] STM sensitivity test passed: dI/I = {res['percent_change']:.2f}%, Drop Factor = {res['drop_factor']:.2f}x")

def test_wavefunction_continuity():
    # Check that wavefunction values match at boundary x = 0 and x = a
    a_nm = 0.5
    res = pe.compute_wavefunction_profile(1.0, 2.0, 5.0, barrier_width_nm=a_nm, num_points_per_region=500)
    
    # Value at x = 0
    psi_I_0 = res["psi_I_real"][-1]
    psi_II_0 = res["psi_II_real"][0]
    diff_0 = abs(psi_I_0 - psi_II_0)
    assert diff_0 < 0.05, f"Discontinuity at x = 0: |{psi_I_0} - {psi_II_0}| = {diff_0}"
    
    # Value at x = a
    psi_II_a = res["psi_II_real"][-1]
    psi_III_a = res["psi_III_real"][0]
    diff_a = abs(psi_II_a - psi_III_a)
    assert diff_a < 0.05, f"Discontinuity at x = a: |{psi_II_a} - {psi_III_a}| = {diff_a}"
    print(f"[OK] Boundary continuity test passed: dpsi(0) = {diff_0:.4e}, dpsi(a) = {diff_a:.4e}")

def test_plots():
    wave = pe.compute_wavefunction_profile(1.0, 2.0, 5.0, 0.5)
    f1 = viz.create_wavefunction_barrier_plot(wave, "Energy-Offset Wavefunction")
    f2 = viz.create_transmission_curve_plot(8.87, 0.5, 1.0, 2.0, 5.0, log_scale=True)
    f3 = viz.create_stm_case_study_plot(8.87, 0.5, i0_na=1.0, delta_s_nm=0.1, log_scale=False)
    f4 = viz.create_stm_topography_schematic(0.5, 0.1)
    assert len(f1.data) >= 4, "Plot 1 should have barrier, energy, and waves"
    assert len(f2.data) >= 3, "Plot 2 should have approx, exact, and marker"
    assert len(f3.data) >= 3, "Plot 3 should have curve, shaded band, and markers"
    print("[OK] All visualization routines executed and validated successfully!")

if __name__ == "__main__":
    test_decay_constant()
    test_classical_edge_case()
    test_stm_sensitivity()
    test_wavefunction_continuity()
    test_plots()
    print("\n[SUCCESS] ALL TESTS PASSED!")
