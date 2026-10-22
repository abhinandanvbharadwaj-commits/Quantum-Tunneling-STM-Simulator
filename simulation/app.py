"""
Quantum Tunneling & STM Simulator
=================================
An interactive, high-precision scientific dashboard demonstrating:
- 1D Quantum Barrier Penetration and Evanescent Wave Decay (Section 13.5)
- Scanning Tunneling Microscopy (STM) Nanoscale Feedback Physics (Section 13.6)

Framework: Streamlit + Plotly + NumPy
Author: Expert Quantum Physics & UI/UX Developer
"""

import streamlit as st
import numpy as np
import pandas as pd
import physics_engine as pe
import visualization as viz
import styles
import thesis_content as tc

# ==============================================================================
# PAGE CONFIGURATION (Scientific Dark Theme)
# ==============================================================================
st.set_page_config(
    page_title="Quantum Tunneling & STM Simulator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom modern CSS
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)


# ==============================================================================
# STATE MANAGEMENT & PRESETS
# ==============================================================================
if "mass" not in st.session_state:
    st.session_state["mass"] = 1.0
if "energy" not in st.session_state:
    st.session_state["energy"] = 2.0
if "barrier_height" not in st.session_state:
    st.session_state["barrier_height"] = 5.0
if "barrier_width" not in st.session_state:
    st.session_state["barrier_width"] = 0.5
if "allow_overbarrier" not in st.session_state:
    st.session_state["allow_overbarrier"] = False


def apply_preset(preset_key: str):
    """Applies parameters from selected thesis engineering preset."""
    preset = tc.ENGINEERING_PRESETS[preset_key]
    st.session_state["mass"] = preset["m"]
    st.session_state["energy"] = preset["E"]
    st.session_state["barrier_height"] = preset["V0"]
    st.session_state["barrier_width"] = preset["a"]
    if preset["E"] >= preset["V0"]:
        st.session_state["allow_overbarrier"] = True


# ==============================================================================
# SIDEBAR CONTROLS & THESIS GUIDELINES
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎛️ Simulation Controls")

    # Engineering Presets Selector
    preset_choice = st.selectbox(
        "Load Thesis Case Preset:",
        options=["Custom Configuration"] + list(tc.ENGINEERING_PRESETS.keys()),
        index=0,
        help="Quickly load validated physical parameters matching thesis chapters."
    )
    if preset_choice != "Custom Configuration":
        apply_preset(preset_choice)
        st.caption(f"💡 *{tc.ENGINEERING_PRESETS[preset_choice]['description']}*")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # 1. Particle Mass (m) Slider
    # Range [0.1, 10.0] in units of electron mass (m_e), Default = 1.0
    mass_ratio = st.slider(
        "Particle Mass (m / mₑ):",
        min_value=0.1,
        max_value=10.0,
        value=float(st.session_state["mass"]),
        step=0.1,
        help="Mass in units of electron rest mass m_e (9.109 × 10⁻³¹ kg). Heavier particles attenuate exponentially faster."
    )
    st.session_state["mass"] = mass_ratio

    # 2. Particle Energy (E) Slider
    # Range [0.1, 10.0] eV, Default = 2.0 eV
    energy_ev = st.slider(
        "Particle Energy E (eV):",
        min_value=0.1,
        max_value=10.0,
        value=float(st.session_state["energy"]),
        step=0.1,
        help="Kinetic energy of the incident particle in electronvolts (eV)."
    )
    st.session_state["energy"] = energy_ev

    # Optional Edge-Case Testing Toggle
    allow_overbarrier = st.checkbox(
        "Allow Over-Barrier Regime (E ≥ V₀)",
        value=bool(st.session_state["allow_overbarrier"]),
        help="Check this to test classical over-barrier transmission when E exceeds V0."
    )
    st.session_state["allow_overbarrier"] = allow_overbarrier

    # 3. Barrier Height (V0) Slider
    # Ensure V0 > E unless over-barrier regime is explicitly permitted
    min_v0 = 0.1 if allow_overbarrier else round(min(energy_ev + 0.1, 14.9), 2)
    default_v0 = max(min_v0, float(st.session_state["barrier_height"]))
    if default_v0 > 15.0:
        default_v0 = 15.0

    barrier_height_ev = st.slider(
        "Barrier Height V₀ (eV):",
        min_value=min_v0,
        max_value=15.0,
        value=float(default_v0),
        step=0.1,
        help="Potential energy barrier height V0 in eV. By default maintained > E for tunneling regime."
    )
    st.session_state["barrier_height"] = barrier_height_ev

    # 4. Barrier Width / STM Separation (a or s) Slider
    # Range [0.05, 2.0] nm, Default = 0.5 nm
    barrier_width_nm = st.slider(
        "Barrier Width / STM Gap a, s (nm):",
        min_value=0.05,
        max_value=2.0,
        value=float(st.session_state["barrier_width"]),
        step=0.05,
        help="Barrier thickness 'a' or STM tip-to-sample vacuum separation 's' in nanometers (1 nm = 10 Å)."
    )
    st.session_state["barrier_width"] = barrier_width_nm

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Advanced STM Parameters
    with st.expander("⚙️ Advanced STM Instrument Settings", expanded=False):
        i0_ref = st.number_input(
            "Contact Setpoint Current I₀ (nA):",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.5,
            help="Tunneling current scale factor at zero separation."
        )
        delta_s_step = st.number_input(
            "Topographic Perturbation Δs (nm):",
            min_value=0.01,
            max_value=0.5,
            value=0.10,
            step=0.01,
            help="Atomic lattice step displacement (standard 0.10 nm = 1.0 Ångström step)."
        )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Sidebar Accordion for Thesis Sections 13.5 and 13.6
    st.markdown("### 📚 Thesis Guidelines")
    with st.expander("📖 Section 13.5: Tunneling Theory", expanded=False):
        st.markdown(tc.THESIS_SECTION_13_5)

    with st.expander("🔬 Section 13.6: STM Nanotechnology", expanded=False):
        st.markdown(tc.THESIS_SECTION_13_6)


# ==============================================================================
# MATHEMATICAL ENGINE CALCULATIONS
# ==============================================================================
# 1. Decay constant kappa
kappa_m, kappa_nm, is_classical = pe.calculate_decay_constant(
    mass_ratio=mass_ratio,
    energy_ev=energy_ev,
    barrier_height_ev=barrier_height_ev
)

# 2. Transmission probability T
t_prob = pe.calculate_transmission_probability(
    kappa_nm=kappa_nm,
    barrier_width_nm=barrier_width_nm,
    is_classical=is_classical
)

# 3. STM Tunneling Current I
i_tunnel = pe.calculate_stm_current(
    kappa_nm=kappa_nm,
    separation_nm=barrier_width_nm,
    i0_na=i0_ref,
    is_classical=is_classical
)

# 4. STM Relative Change for 0.1 nm (1 Å) atomic step
stm_change = pe.calculate_stm_relative_change(
    kappa_nm=kappa_nm,
    delta_s_nm=delta_s_step,
    is_classical=is_classical
)

# Penetration depth delta = 1 / kappa
penetration_depth_nm = (1.0 / kappa_nm) if kappa_nm > 1e-12 else float('inf')
penetration_depth_angstrom = penetration_depth_nm * 10.0


# ==============================================================================
# MAIN DASHBOARD INTERFACE
# ==============================================================================

# Top Title Banner
st.markdown(f"""
<div class="header-banner">
    <div>
        <h1 class="header-title">Quantum Tunneling & STM Simulator</h1>
        <div class="header-subtitle">
            Interactive Nanotechnology Simulation Platform &bull; Based on Thesis Sections 13.5 & 13.6
        </div>
    </div>
    <div>
        <span class="pill-badge pill-cyan">Quantum Engine v2.4</span>
        <span class="pill-badge pill-purple">STM Precision Feedback</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Classical Over-Barrier Warning Banner (Graceful Edge Case Handling)
if is_classical:
    st.markdown(f"""
    <div class="alert-banner">
        ⚠️ <b>CLASSICAL OVER-BARRIER TRANSMISSION REGIME (E = {energy_ev:.2f} eV ≥ V₀ = {barrier_height_ev:.2f} eV):</b><br>
        Particle kinetic energy exceeds barrier height. Classical mechanics permits unhindered transmission.
        Decay constant κ is zero; transmission probability T is capped at 1.0 (100%).
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# REAL-TIME KPI METRICS GRID
# ==============================================================================
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    kappa_display = f"{kappa_nm:.3f} nm⁻¹" if not is_classical else "0.000 nm⁻¹"
    kappa_caption = f"κ = {kappa_m:.2e} m⁻¹" if not is_classical else "E ≥ V₀ (Over-barrier)"
    st.markdown(styles.render_kpi_card(
        label="Decay Constant (κ)",
        value=kappa_display,
        caption=kappa_caption,
        color_class="kpi-cyan"
    ), unsafe_allow_html=True)

with kpi_col2:
    if t_prob >= 0.01:
        t_display = f"{t_prob * 100.0:.2f}%"
    else:
        t_display = f"{t_prob:.2e}"
    t_caption = f"T = exp(-2κa) | a = {barrier_width_nm:.2f} nm"
    st.markdown(styles.render_kpi_card(
        label="Transmission Prob (T)",
        value=t_display,
        caption=t_caption,
        color_class="kpi-purple"
    ), unsafe_allow_html=True)

with kpi_col3:
    pct_val = stm_change["percent_change"]
    pct_display = f"{pct_val:.1f}%" if not is_classical else "0.0%"
    pct_caption = f"For +{delta_s_step:.2f} nm step ({stm_change['drop_factor']:.1f}× drop)"
    st.markdown(styles.render_kpi_card(
        label="Relative ΔI / I (%)",
        value=pct_display,
        caption=pct_caption,
        color_class="kpi-rose"
    ), unsafe_allow_html=True)

with kpi_col4:
    if is_classical:
        delta_display = "Infinite"
        delta_caption = "No attenuation"
    else:
        delta_display = f"{penetration_depth_nm:.3f} nm"
        delta_caption = f"δ = 1/κ ({penetration_depth_angstrom:.2f} Å)"
    st.markdown(styles.render_kpi_card(
        label="Penetration Depth (δ)",
        value=delta_display,
        caption=delta_caption,
        color_class="kpi-emerald"
    ), unsafe_allow_html=True)

with kpi_col5:
    i_display = f"{i_tunnel:.3e} nA" if i_tunnel < 0.01 else f"{i_tunnel:.3f} nA"
    i_caption = f"At gap s = {barrier_width_nm:.2f} nm"
    st.markdown(styles.render_kpi_card(
        label="Tunneling Current (I)",
        value=i_display,
        caption=i_caption,
        color_class="kpi-amber"
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# MAIN VISUALIZATION PANELS
# ==============================================================================

# Tabs for structured exploratory workflow
tab_wave, tab_transmission, tab_stm, tab_nanocad = st.tabs([
    "📊 Plot 1: Wavefunction & Barrier Profile",
    "📈 Plot 2: Transmission Sensitivity (T vs a)",
    "⚡ Plot 3: STM Topographic Feedback (I vs s)",
    "🔬 Nanoscale STM Cross-Section & Theory"
])


# ------------------------------------------------------------------------------
# TAB 1: WAVEFUNCTION DECAY & POTENTIAL BARRIER
# ------------------------------------------------------------------------------
with tab_wave:
    col_plot1, col_info1 = st.columns([3, 1])

    with col_info1:
        st.markdown("#### 🌊 Wavefunction Controls")
        view_mode = st.radio(
            "Visualization Display Mode:",
            options=["Energy-Offset Wavefunction", "Probability Density |ψ|²", "Raw Wavefunction Re(ψ)"],
            index=0,
            help="Energy-Offset superimposes the oscillation baseline on the incident energy line E."
        )

        st.markdown("""
        **Physics Highlights (Section 13.5):**
        * **Region I ($x < 0$):** Oscillatory interference between incident and reflected waves.
        * **Region II ($0 \\le x \\le a$):** Evanescent exponential decay $\\psi(x) \\propto e^{-\\kappa x}$.
        * **Region III ($x > a$):** Pure transmitted plane wave of identical wavelength but attenuated amplitude $\\sqrt{T}$.
        """)

        st.info(f"""
        **Current Boundary State:**
        * Wavelength $\\lambda_1$: {2.0 * np.pi / (np.sqrt(2 * mass_ratio * pe.M_E * energy_ev * pe.EV_TO_JOULES) / pe.HBAR) * 1e9:.3f} nm
        * Evanescent Decay Length $\\delta$: {penetration_depth_nm:.3f} nm
        * Barrier Attenuation $\\kappa a$: {kappa_nm * barrier_width_nm:.2f}
        """)

    with col_plot1:
        with st.spinner("Computing continuous boundary-matched wavefunction..."):
            wave_profile = pe.compute_wavefunction_profile(
                mass_ratio=mass_ratio,
                energy_ev=energy_ev,
                barrier_height_ev=barrier_height_ev,
                barrier_width_nm=barrier_width_nm
            )
            fig_wave = viz.create_wavefunction_barrier_plot(wave_profile, view_mode=view_mode)
            st.plotly_chart(fig_wave, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 2: TRANSMISSION SENSITIVITY CURVE
# ------------------------------------------------------------------------------
with tab_transmission:
    col_plot2, col_info2 = st.columns([3, 1])

    with col_info2:
        st.markdown("#### 📐 Sensitivity Analysis")
        scale_choice = st.radio(
            "Y-Axis Scale:",
            options=["Logarithmic (Recommended)", "Linear Scale"],
            index=0,
            help="Logarithmic scale reveals the wide dynamic range across barrier widths."
        )
        is_log = (scale_choice == "Logarithmic (Recommended)")

        st.markdown("""
        **Exponential Sensitivity ($T \\propto e^{-2\\kappa a}$):**
        * Notice how transmission probability drops by orders of magnitude with linear width increases.
        * The purple dotted curve shows the exact analytical 1D rectangular barrier solution, matching WKB for $\\kappa a > 1$.
        """)

        # Display numeric summary
        st.success(f"""
        **Operating Point:**
        * Selected Width $a$: **{barrier_width_nm:.2f} nm** ({barrier_width_nm * 10:.1f} Å)
        * Approx Transmission $T$: **{t_prob:.3e}**
        * Attenuation Rate $2\\kappa$: **{2.0 * kappa_nm:.2f} nm⁻¹**
        """)

    with col_plot2:
        fig_trans = viz.create_transmission_curve_plot(
            kappa_nm=kappa_nm,
            current_a_nm=barrier_width_nm,
            mass_ratio=mass_ratio,
            energy_ev=energy_ev,
            barrier_height_ev=barrier_height_ev,
            log_scale=is_log
        )
        st.plotly_chart(fig_trans, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 3: STM REAL-WORLD CASE STUDY
# ------------------------------------------------------------------------------
with tab_stm:
    col_plot3, col_info3 = st.columns([3, 1])

    with col_info3:
        st.markdown("#### 🔬 STM Topographic Feedback")
        stm_scale_choice = st.radio(
            "STM Current Axis:",
            options=["Linear Scale", "Logarithmic Scale"],
            index=0,
            help="Switch between linear and logarithmic current representation."
        )
        stm_log = (stm_scale_choice == "Logarithmic Scale")

        st.markdown(f"""
        **Atomic Resolution Physics (Section 13.6):**
        * A standard atomic step displacement $\\Delta s = +{delta_s_step:.2f}\\text{{ nm}}$ ($1.0\\text{{ Å}}$) drops the tunneling current by:
        """)
        st.metric(
            label="Current Change ΔI / I",
            value=f"{stm_change['percent_change']:.1f}%",
            delta=f"Factor of {stm_change['drop_factor']:.1f}× drop"
        )

        st.markdown(f"""
        Because $I \\propto e^{{-2\\kappa s}}$, the closed-loop **piezoelectric scanner** senses this massive current deficit and immediately extends the tip downwards to restore the setpoint current $I_0 = {i0_ref:.2f}\\text{{ nA}}$.
        """)

    with col_plot3:
        fig_stm = viz.create_stm_case_study_plot(
            kappa_nm=kappa_nm,
            current_s_nm=barrier_width_nm,
            i0_na=i0_ref,
            delta_s_nm=delta_s_step,
            is_classical=is_classical,
            log_scale=stm_log
        )
        st.plotly_chart(fig_stm, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 4: NANOSCALE SCHEMATIC & THEORY
# ------------------------------------------------------------------------------
with tab_nanocad:
    col_schematic, col_theory = st.columns([1, 1])

    with col_schematic:
        st.markdown("#### 📐 Nanoscale Tip & Surface Topography")
        fig_schem = viz.create_stm_topography_schematic(
            current_s_nm=barrier_width_nm,
            delta_s_nm=delta_s_step
        )
        st.plotly_chart(fig_schem, use_container_width=True)

    with col_theory:
        st.markdown("#### 🔬 Key Engineering Formulas (Sections 13.5 & 13.6)")
        st.latex(r"\kappa = \frac{\sqrt{2m(V_0 - E)}}{\hbar}")
        st.latex(r"T(a) \approx \exp\left(-2 \kappa a\right)")
        st.latex(r"I(s) = I_0 \exp\left(-2 \kappa s\right)")
        st.latex(r"\frac{\Delta I}{I} = \exp\left(-2 \kappa \Delta s\right) - 1")

        st.markdown("""
        **Engineering Implications:**
        * **Atomic Resolution:** Lateral resolution $\\approx 0.1\\text{ nm}$, vertical resolution $\\approx 0.01\\text{ nm}$ (sub-picometer).
        * **Constant Current vs Constant Height Mode:** Constant Current is preferred for rough surfaces; Constant Height enables video-rate scanning of flat terraces.
        * **Semiconductor Scaling Limitation:** In sub-3nm GAAFET transistors, tunneling through thin gate dielectrics leads to high static leakage power.
        """)


# ==============================================================================
# DATA EXPORT & SIMULATION REPORT GENERATOR
# ==============================================================================
with st.expander("📥 Export Numerical Simulation Data (CSV / Lab Report)", expanded=False):
    st.markdown("Download full mathematical curves for external plotting, lab analysis, or thesis documentation.")
    
    # Generate tabular dataset
    a_export = np.linspace(0.05, 2.0, 100)
    t_export = [pe.calculate_transmission_probability(kappa_nm, a, is_classical) for a in a_export]
    i_export = [pe.calculate_stm_current(kappa_nm, a, i0_ref, is_classical) for a in a_export]
    
    df_export = pd.DataFrame({
        "Barrier_Width_or_Gap_nm": a_export,
        "Barrier_Width_Angstrom": a_export * 10.0,
        "Transmission_Probability_T": t_export,
        "Tunneling_Current_nA": i_export,
        "Decay_Constant_nm_inv": kappa_nm,
        "Particle_Mass_ratio": mass_ratio,
        "Energy_eV": energy_ev,
        "Barrier_Height_eV": barrier_height_ev
    })
    
    csv_bytes = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Download Simulation Data (CSV)",
        data=csv_bytes,
        file_name="quantum_tunneling_stm_simulation.csv",
        mime="text/csv"
    )

# Dashboard Footer
st.markdown("""
<div class="dashboard-footer">
    Quantum Tunneling & STM Simulator &bull; Developed in strict accordance with Thesis Guidelines Sections 13.5 & 13.6<br>
    Physical Constants: CODATA 2018 &bull; Wavevector matching: 1D Time-Independent Schrödinger Equation
</div>
""", unsafe_allow_html=True)
