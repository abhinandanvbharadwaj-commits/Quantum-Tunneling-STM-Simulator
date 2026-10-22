"""
Quantum Tunneling & STM Simulator - Visualizations
=================================================
High-performance Plotly visual components for:
1. Wavefunction Decay & Potential Barrier Layout
2. Transmission Sensitivity Curve (T vs Barrier Width a)
3. STM Engineering Real-World Case Study (I vs Tip Separation s)
4. STM Nanoscale Feedback Architecture Schematic
"""

import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any
import physics_engine as pe

# Modern Dark Science Color Palette
DARK_BG = "#0B0F19"
CARD_BG = "#111827"
GRID_COLOR = "#1F2937"
TEXT_COLOR = "#E5E7EB"
CYAN_ACCENT = "#00F0FF"
EMERALD_ACCENT = "#00FFA3"
AMBER_ACCENT = "#F59E0B"
PURPLE_ACCENT = "#A855F7"
ROSE_ACCENT = "#F43F5E"
BARRIER_FILL = "rgba(168, 85, 247, 0.18)"
BARRIER_LINE = "#A855F7"


def create_wavefunction_barrier_plot(
    wave_data: Dict[str, Any],
    view_mode: str = "Energy-Offset Wavefunction"
) -> go.Figure:
    """
    Plot 1: Wavefunction Decay & Potential Barrier Layout.
    Draws a rectangular potential barrier block of height V0 and width 'a'.
    Superimposes the sinusoidal wave in Region I, exponential decay in Region II,
    and reduced-amplitude transmitted sinusoidal wave in Region III.
    """
    x = wave_data["x"]
    barrier_width = wave_data["barrier_width_nm"]
    barrier_height = wave_data["barrier_height_ev"]
    energy = wave_data["energy_ev"]

    fig = go.Figure()

    # Determine scaling for wavefunction superposition
    max_amp = np.max(np.abs(wave_data["psi_real"]))
    if max_amp <= 0:
        max_amp = 1.0
    scale_factor = (barrier_height * 0.35) / max_amp

    if view_mode == "Energy-Offset Wavefunction":
        y_wave = energy + wave_data["psi_real"] * scale_factor
        wave_label = "Wavefunction Re(ψ) [Centered at E]"
    elif view_mode == "Probability Density |ψ|²":
        y_wave = energy + (wave_data["prob_density"] / np.max(wave_data["prob_density"])) * (barrier_height * 0.4)
        wave_label = "Probability Density |ψ|² [Offset at E]"
    else:  # Raw Normalized
        y_wave = wave_data["psi_real"]
        wave_label = "Normalized Wavefunction Re(ψ)"

    # 1. Potential Barrier Rectangular Block
    # Stepped potential profile: 0 for x<0, V0 for 0<=x<=a, 0 for x>a
    fig.add_trace(go.Scatter(
        x=[-max(0.8, barrier_width * 1.2), 0, 0, barrier_width, barrier_width, barrier_width + max(0.8, barrier_width * 1.2)],
        y=[0, 0, barrier_height, barrier_height, 0, 0],
        mode="lines",
        name=f"Potential Barrier V₀ ({barrier_height:.1f} eV)",
        line=dict(color=BARRIER_LINE, width=3),
        fill="tozeroy",
        fillcolor=BARRIER_FILL,
        hoverinfo="name+y"
    ))

    # 2. Particle Energy Level (E)
    x_min = float(x[0])
    x_max = float(x[-1])
    fig.add_trace(go.Scatter(
        x=[x_min, x_max],
        y=[energy, energy],
        mode="lines",
        name=f"Incident Energy E ({energy:.2f} eV)",
        line=dict(color=AMBER_ACCENT, width=2.5, dash="dash"),
        hoverinfo="name+y"
    ))

    # 3. Superimposed Wavefunction in 3 Regions
    # Region I: Incident & Reflected (x < 0)
    mask_I = x < 0.0
    fig.add_trace(go.Scatter(
        x=x[mask_I],
        y=y_wave[mask_I],
        mode="lines",
        name="Region I: Incident + Reflected",
        line=dict(color=CYAN_ACCENT, width=2.5),
        hoverinfo="x+y"
    ))

    # Region II: Barrier Penetration (0 <= x <= a)
    mask_II = (x >= 0.0) & (x <= barrier_width)
    fig.add_trace(go.Scatter(
        x=x[mask_II],
        y=y_wave[mask_II],
        mode="lines",
        name="Region II: Exponential Decay",
        line=dict(color=ROSE_ACCENT, width=3.2),
        hoverinfo="x+y"
    ))

    # Region III: Transmitted Wave (x > a)
    mask_III = x > barrier_width
    fig.add_trace(go.Scatter(
        x=x[mask_III],
        y=y_wave[mask_III],
        mode="lines",
        name="Region III: Transmitted Wave",
        line=dict(color=EMERALD_ACCENT, width=2.5),
        hoverinfo="x+y"
    ))

    # Boundary vertical marker lines
    fig.add_vline(x=0.0, line_width=1.5, line_dash="dot", line_color="#9CA3AF")
    fig.add_vline(x=barrier_width, line_width=1.5, line_dash="dot", line_color="#9CA3AF")

    # Region Annotations
    y_annotation = barrier_height * 1.15
    fig.add_annotation(
        x=-max(0.8, barrier_width * 1.2) / 2.0,
        y=y_annotation,
        text="<b>REGION I</b><br>Incident / Standing Wave",
        showarrow=False,
        font=dict(color=CYAN_ACCENT, size=11),
        align="center"
    )
    fig.add_annotation(
        x=barrier_width / 2.0,
        y=y_annotation,
        text=f"<b>REGION II</b><br>Barrier Tunneling (a = {barrier_width:.2f} nm)",
        showarrow=False,
        font=dict(color=PURPLE_ACCENT, size=11),
        align="center"
    )
    fig.add_annotation(
        x=barrier_width + max(0.8, barrier_width * 1.2) / 2.0,
        y=y_annotation,
        text="<b>REGION III</b><br>Transmitted Wave (Attenuated)",
        showarrow=False,
        font=dict(color=EMERALD_ACCENT, size=11),
        align="center"
    )

    # Barrier height and energy labels
    fig.add_annotation(
        x=barrier_width / 2.0,
        y=barrier_height / 2.0,
        text=f"<b>V₀ = {barrier_height:.1f} eV</b><br>Barrier",
        showarrow=False,
        font=dict(color="#D8B4FE", size=12),
        align="center"
    )

    # Layout styling
    y_axis_title = "Energy (eV)" if "Offset" in view_mode else "Wavefunction Amplitude"
    fig.update_layout(
        title=dict(
            text="<b>Plot 1: Wavefunction Decay & Potential Barrier Layout</b>",
            font=dict(size=17, color=TEXT_COLOR)
        ),
        xaxis=dict(
            title="Spatial Position x (nm)",
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showgrid=True,
            color=TEXT_COLOR
        ),
        yaxis=dict(
            title=y_axis_title,
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showgrid=True,
            range=[-0.2, barrier_height * 1.3],
            color=TEXT_COLOR
        ),
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color=TEXT_COLOR),
            bgcolor="rgba(17, 24, 39, 0.7)"
        ),
        hovermode="x unified",
        margin=dict(l=55, r=25, t=95, b=45)
    )

    return fig


def create_transmission_curve_plot(
    kappa_nm: float,
    current_a_nm: float,
    mass_ratio: float,
    energy_ev: float,
    barrier_height_ev: float,
    log_scale: bool = True
) -> go.Figure:
    """
    Plot 2: Transmission Sensitivity Curve.
    Plots T vs Barrier Width (a) across [0.05, 2.0] nm with a dynamic marker
    at the currently selected slider value.
    """
    a_values = np.linspace(0.05, 2.0, 350)
    is_classical = energy_ev >= barrier_height_ev

    t_approx_values = np.array([
        pe.calculate_transmission_probability(kappa_nm, a, is_classical)
        for a in a_values
    ])

    t_exact_values = np.array([
        pe.calculate_exact_transmission_probability(mass_ratio, energy_ev, barrier_height_ev, a)
        for a in a_values
    ])

    current_t_approx = pe.calculate_transmission_probability(kappa_nm, current_a_nm, is_classical)

    fig = go.Figure()

    # 1. Approximate WKB Transmission T = exp(-2 * kappa * a)
    fig.add_trace(go.Scatter(
        x=a_values,
        y=t_approx_values,
        mode="lines",
        name="WKB Approx: T = exp(-2κa)",
        line=dict(color=CYAN_ACCENT, width=3),
        hovertemplate="Barrier Width a: %{x:.3f} nm<br>Approx T: %{y:.3e}<extra></extra>"
    ))

    # 2. Exact Quantum Transmission (for comparison and educational depth)
    fig.add_trace(go.Scatter(
        x=a_values,
        y=t_exact_values,
        mode="lines",
        name="Exact 1D Barrier Solution",
        line=dict(color=PURPLE_ACCENT, width=2, dash="dot"),
        hovertemplate="Barrier Width a: %{x:.3f} nm<br>Exact T: %{y:.3e}<extra></extra>"
    ))

    # 3. Dynamic Marker at current operating point
    fig.add_trace(go.Scatter(
        x=[current_a_nm],
        y=[current_t_approx],
        mode="markers",
        name=f"Current Operating Point (a={current_a_nm:.2f} nm)",
        marker=dict(
            color=AMBER_ACCENT,
            size=14,
            symbol="diamond",
            line=dict(color="#FFFFFF", width=2)
        ),
        hovertemplate="<b>Selected Width: %{x:.2f} nm</b><br>Transmission T: %{y:.4e}<extra></extra>"
    ))

    # Operating point annotation
    fig.add_annotation(
        x=current_a_nm,
        y=np.log10(max(current_t_approx, 1e-18)) if log_scale else current_t_approx,
        text=f"<b>Current: a = {current_a_nm:.2f} nm</b><br>T ≈ {current_t_approx:.2e}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor=AMBER_ACCENT,
        ax=45 if current_a_nm < 1.0 else -55,
        ay=-45,
        font=dict(color="#FFFFFF", size=11),
        bgcolor="rgba(17, 24, 39, 0.85)",
        bordercolor=AMBER_ACCENT,
        borderwidth=1.5
    )

    y_axis_type = "log" if log_scale else "linear"
    y_min = 1e-16 if log_scale else 0.0

    fig.update_layout(
        title=dict(
            text="<b>Plot 2: Transmission Sensitivity Curve [T vs Barrier Width (a)]</b>",
            font=dict(size=17, color=TEXT_COLOR)
        ),
        xaxis=dict(
            title="Barrier Width / STM Separation a (nm)",
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showgrid=True,
            color=TEXT_COLOR
        ),
        yaxis=dict(
            title="Transmission Probability T" + (" (Log Scale)" if log_scale else " (Linear Scale)"),
            type=y_axis_type,
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showgrid=True,
            range=[-16, 0.2] if log_scale else [-0.02, 1.05],
            color=TEXT_COLOR
        ),
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color=TEXT_COLOR),
            bgcolor="rgba(17, 24, 39, 0.7)"
        ),
        margin=dict(l=55, r=25, t=95, b=45)
    )

    return fig


def create_stm_case_study_plot(
    kappa_nm: float,
    current_s_nm: float,
    i0_na: float = 1.0,
    delta_s_nm: float = 0.1,
    is_classical: bool = False,
    log_scale: bool = False
) -> go.Figure:
    """
    Plot 3: STM Engineering Real-world Case Study.
    Plots 'Tunneling Current (I) vs Tip-Surface Separation (s)'.
    Highlights how a 0.1nm change drastically drops/increases current to simulate
    nanoscale topographic feedback.
    """
    s_values = np.linspace(0.1, 1.5, 300)
    current_curve = [pe.calculate_stm_current(kappa_nm, s, i0_na, is_classical) for s in s_values]

    # Calculate points of interest
    s_curr = current_s_nm
    i_curr = pe.calculate_stm_current(kappa_nm, s_curr, i0_na, is_classical)

    s_perturbed = min(current_s_nm + delta_s_nm, 1.5)
    i_perturbed = pe.calculate_stm_current(kappa_nm, s_perturbed, i0_na, is_classical)

    drop_info = pe.calculate_stm_relative_change(kappa_nm, delta_s_nm, is_classical)
    drop_pct = drop_info["percent_change"]
    drop_factor = drop_info["drop_factor"]

    fig = go.Figure()

    # 1. Main STM Current vs Separation Curve
    fig.add_trace(go.Scatter(
        x=s_values,
        y=current_curve,
        mode="lines",
        name=f"Tunneling Current I(s) [I₀ = {i0_na:.1f} nA]",
        line=dict(color=EMERALD_ACCENT, width=3.5),
        fill="tozeroy",
        fillcolor="rgba(0, 255, 163, 0.08)",
        hovertemplate="Separation s: %{x:.3f} nm<br>Current I: %{y:.4e} nA<extra></extra>"
    ))

    # 2. Shaded atomic step perturbation region [s_curr, s_perturbed]
    s_band = np.linspace(s_curr, s_perturbed, 50)
    i_band = [pe.calculate_stm_current(kappa_nm, s, i0_na, is_classical) for s in s_band]
    fig.add_trace(go.Scatter(
        x=np.concatenate([s_band, s_band[::-1]]),
        y=np.concatenate([i_band, np.zeros_like(i_band)]),
        fill="toself",
        fillcolor="rgba(244, 63, 94, 0.25)",
        line=dict(color="rgba(244, 63, 94, 0.6)", width=1),
        name=f"Atomic Step Perturbation (+{delta_s_nm} nm)",
        hoverinfo="skip"
    ))

    # 3. Current Operating Setpoint Marker
    fig.add_trace(go.Scatter(
        x=[s_curr],
        y=[i_curr],
        mode="markers",
        name=f"Setpoint Current ({s_curr:.2f} nm, {i_curr:.3e} nA)",
        marker=dict(color=CYAN_ACCENT, size=13, symbol="circle", line=dict(color="#FFFFFF", width=2))
    ))

    # 4. Perturbed Tip Position Marker
    fig.add_trace(go.Scatter(
        x=[s_perturbed],
        y=[i_perturbed],
        mode="markers",
        name=f"Perturbed Position (+{delta_s_nm:.1f} nm)",
        marker=dict(color=ROSE_ACCENT, size=13, symbol="diamond", line=dict(color="#FFFFFF", width=2))
    ))

    # Callout Arrow and Annotation
    arrow_text = (
        f"<b>Nanoscale Topographic Feedback:</b><br>"
        f"• Δs = +{delta_s_nm:.1f} nm (1 Å atomic step)<br>"
        f"• Current Change: <b>{drop_pct:.1f}%</b><br>"
        f"• Signal Drop Factor: <b>{drop_factor:.1f}×</b><br>"
        f"<i>Piezo scanner triggers rapid z-retraction</i>"
    )

    y_pos_annot = (i_curr + i_perturbed) / 2.0 if not log_scale else np.sqrt(max(i_curr * i_perturbed, 1e-15))

    fig.add_annotation(
        x=(s_curr + s_perturbed) / 2.0,
        y=y_pos_annot,
        text=arrow_text,
        showarrow=True,
        arrowhead=2,
        arrowsize=1.2,
        arrowwidth=2,
        arrowcolor=ROSE_ACCENT,
        ax=80,
        ay=-55,
        font=dict(color="#FFFFFF", size=11),
        bgcolor="rgba(17, 24, 39, 0.92)",
        bordercolor=ROSE_ACCENT,
        borderwidth=2
    )

    fig.update_layout(
        title=dict(
            text="<b>Plot 3: STM Engineering Real-world Case Study [Current (I) vs Tip Separation (s)]</b>",
            font=dict(size=17, color=TEXT_COLOR)
        ),
        xaxis=dict(
            title="Tip-to-Surface Separation s (nm)",
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showgrid=True,
            color=TEXT_COLOR
        ),
        yaxis=dict(
            title="Tunneling Current I (nA)" + (" [Log Scale]" if log_scale else " [Linear Scale]"),
            type="log" if log_scale else "linear",
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            showgrid=True,
            color=TEXT_COLOR
        ),
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color=TEXT_COLOR),
            bgcolor="rgba(17, 24, 39, 0.7)"
        ),
        margin=dict(l=55, r=25, t=95, b=45)
    )

    return fig


def create_stm_topography_schematic(
    current_s_nm: float,
    delta_s_nm: float = 0.1
) -> go.Figure:
    """
    Interactive Nanoscale STM Architecture Schematic.
    Visually depicts the metallic tip, vacuum tunneling gap, and atomic lattice
    with an atomic step defect to demonstrate constant-current feedback.
    """
    fig = go.Figure()

    # Surface substrate with atomic step at x = 0
    x_sub = np.linspace(-1.5, 1.5, 300)
    # Step at x=0
    y_sub = np.zeros_like(x_sub)
    y_sub[x_sub >= 0.0] = delta_s_nm  # Atomic terrace step height

    # 1. Atomic substrate block
    fig.add_trace(go.Scatter(
        x=x_sub,
        y=y_sub,
        mode="lines",
        name="Conductive Sample Surface (e.g., Au / Si)",
        line=dict(color=AMBER_ACCENT, width=3),
        fill="tozeroy",
        fillcolor="rgba(245, 158, 11, 0.15)"
    ))

    # Add atomic spheres on the surface
    x_atoms = np.linspace(-1.4, 1.4, 15)
    for xa in x_atoms:
        ya = delta_s_nm if xa >= 0.0 else 0.0
        fig.add_shape(
            type="circle",
            x0=xa - 0.07, y0=ya - 0.07,
            x1=xa + 0.07, y1=ya + 0.07,
            fillcolor="#F59E0B",
            line_color="#B45309",
            opacity=0.8
        )

    # 2. STM Atomically Sharp Tip
    # Tip vertex at x = -0.5, y = current_s_nm
    tip_x = np.array([-0.8, -0.5, -0.2])
    tip_y = np.array([current_s_nm + 0.6, current_s_nm, current_s_nm + 0.6])

    fig.add_trace(go.Scatter(
        x=tip_x,
        y=tip_y,
        mode="lines",
        name="STM Metallic Tip (Tungsten / Pt-Ir)",
        line=dict(color=CYAN_ACCENT, width=3),
        fill="toself",
        fillcolor="rgba(0, 240, 255, 0.25)"
    ))

    # Tip apex single atom
    fig.add_shape(
        type="circle",
        x0=-0.5 - 0.05, y0=current_s_nm - 0.05,
        x1=-0.5 + 0.05, y1=current_s_nm + 0.05,
        fillcolor=CYAN_ACCENT,
        line_color="#FFFFFF"
    )

    # Tunneling gap arrows
    fig.add_annotation(
        x=-0.5,
        y=current_s_nm / 2.0,
        text=f"<b>Vacuum Gap</b><br>s = {current_s_nm:.2f} nm",
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowcolor=EMERALD_ACCENT,
        font=dict(color=EMERALD_ACCENT, size=11),
        bgcolor="rgba(17, 24, 39, 0.8)",
        bordercolor=EMERALD_ACCENT
    )

    # Atomic step annotation
    fig.add_annotation(
        x=0.0,
        y=delta_s_nm + 0.15,
        text=f"<b>Atomic Terrace Step</b><br>Δz = {delta_s_nm:.2f} nm (1 Å)",
        showarrow=True,
        arrowhead=2,
        arrowcolor=AMBER_ACCENT,
        font=dict(color=AMBER_ACCENT, size=10),
        bgcolor="rgba(17, 24, 39, 0.8)"
    )

    fig.update_layout(
        title=dict(
            text="<b>STM Nanoscale Physical Setup & Atomic Step Topography</b>",
            font=dict(size=15, color=TEXT_COLOR)
        ),
        xaxis=dict(
            title="Lateral Scanner Coordinate x (nm)",
            gridcolor=GRID_COLOR,
            color=TEXT_COLOR,
            range=[-1.5, 1.5]
        ),
        yaxis=dict(
            title="Vertical Height z (nm)",
            gridcolor=GRID_COLOR,
            color=TEXT_COLOR,
            range=[-0.2, current_s_nm + 0.8]
        ),
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=9, color=TEXT_COLOR)
        ),
        margin=dict(l=45, r=25, t=75, b=40)
    )

    return fig
