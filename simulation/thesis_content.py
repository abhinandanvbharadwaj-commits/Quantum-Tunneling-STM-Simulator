"""
Quantum Tunneling & STM Simulator - Thesis Documentation & Engineering Guidelines
==================================================================================
Comprehensive scientific content aligning with:
- Section 13.5: Barrier Penetration and Quantum Tunneling Theory
- Section 13.6: Scanning Tunneling Microscopy (STM) & Real-World Engineering Applications
"""

THESIS_SECTION_13_5 = r"""
### Section 13.5: Barrier Penetration & Quantum Tunneling

#### 1. Mathematical Foundation
In classical Newtonian mechanics, a particle of mass $m$ and total mechanical energy $E$ incident upon a potential energy barrier of height $V_0$ is strictly forbidden from entering any region where $E < V_0$. The classical kinetic energy:
$$K = E - V_0 < 0$$
would imply an imaginary momentum ($p = \sqrt{2m(E - V_0)}$), resulting in instantaneous and total reflection at the barrier boundary ($T = 0$, $R = 1$).

In wave mechanics, the physical state of the particle is governed by the **Time-Independent Schrödinger Equation (TISE)**:
$$-\\frac{\\hbar^2}{2m} \\frac{d^2\\psi(x)}{dx^2} + V(x)\\psi(x) = E\\psi(x)$$

#### 2. Three Physical Regions
For a rectangular barrier of width $a$ where $V(x) = V_0$ for $0 \\le x \\le a$ and $0$ elsewhere:

* **Region I ($x < 0$, $V=0$):**
  $$\\psi_I(x) = A e^{i k_1 x} + B e^{-i k_1 x}, \\quad k_1 = \\frac{\\sqrt{2mE}}{\\hbar}$$
  Superposition of an incident plane wave traveling to the right and a reflected wave traveling to the left.

* **Region II ($0 \\le x \\le a$, $V=V_0 > E$):**
  $$\\frac{d^2\\psi_{II}}{dx^2} = \\kappa^2 \\psi_{II}(x), \\quad \\kappa = \\frac{\\sqrt{2m(V_0 - E)}}{\\hbar}$$
  The solution is an **evanescent decaying exponential**:
  $$\\psi_{II}(x) = C e^{-\\kappa x} + D e^{\\kappa x}$$
  Because $\\psi(x)$ cannot terminate abruptly without inducing infinite kinetic energy, the wavefunction *penetrates* through the barrier.

* **Region III ($x > a$, $V=0$):**
  $$\\psi_{III}(x) = F e^{i k_1 (x - a)}$$
  A purely transmitted plane wave with identical wavelength $\\lambda = 2\\pi / k_1$ but severely attenuated amplitude $|F| \\ll |A|$.

#### 3. Transmission Probability (WKB Approximation)
Applying Dirichlet and Neumann boundary conditions (continuity of $\\psi$ and $d\\psi/dx$) at $x=0$ and $x=a$, when the barrier is wide or high ($\\kappa a \\gg 1$), the transmission probability simplifies to the famous exponential decay relation:
$$T = \\frac{|F|^2}{|A|^2} \\approx e^{-2 \\kappa a}$$

#### 4. Critical Role of Particle Mass ($m$)
Because the decay constant $\\kappa$ scales with $\\sqrt{m}$:
$$\\kappa = \\frac{\\sqrt{2m(V_0 - E)}}{\\hbar}$$
a heavier particle undergoes drastic exponential suppression. For instance:
* An electron ($m = 1.0\\,m_e$) has $\\kappa \\approx 8.87\\text{ nm}^{-1}$ for $V_0 - E = 3\\text{ eV}$.
* A proton ($m_p \\approx 1836\\,m_e$) under identical conditions has $\\kappa_p = \\sqrt{1836} \\times 8.87 \\approx 380\\text{ nm}^{-1}$.
Its transmission through a $0.5\\text{ nm}$ barrier is attenuated by $e^{-380} \\approx 10^{-165}$, rendering proton tunneling practically unobservable in this regime!
"""

THESIS_SECTION_13_6 = r"""
### Section 13.6: STM Nanotechnology & Engineering Applications

#### 1. Historical Milestone
The **Scanning Tunneling Microscope (STM)** was invented in 1981 by **Gerd Binnig** and **Heinrich Rohrer** at the IBM Zürich Research Laboratory. Their groundbreaking innovation earned them the **1986 Nobel Prize in Physics**, inaugurating the era of modern nanotechnology by allowing humanity to directly image individual atoms on solid surfaces.

#### 2. Operating Principle: Atomic Vacuum Tunneling
An atomically sharpened conductive tip (etched tungsten wire or platinum-iridium alloy) is brought within sub-nanometer proximity ($s \\approx 0.3 - 1.0\\text{ nm}$) of a conductive sample surface.
Applying a small bias voltage $V_{\\text{bias}}$ ($10\\text{ mV} - 2\\text{ V}$) permits conduction electrons to tunnel through the vacuum gap:
$$I(s) = I_0 \\exp(-2 \\kappa s)$$
where the vacuum barrier height is the effective work function $\\Phi$:
$$\\kappa \\approx \\frac{\\sqrt{2 m_e \\Phi}}{\\hbar}$$
For standard metallic surfaces ($\Phi \\approx 4.0 - 5.0\\text{ eV}$), $\\kappa \\approx 10\\text{ nm}^{-1} = 1.0\\text{ Å}^{-1}$.

#### 3. Topographic Feedback & Extreme Spatial Sensitivity
The sensitivity of the tunneling current to tip-surface displacement is defined by the spatial derivative:
$$\\left|\\frac{d \\ln I}{ds}\\right| = 2\\kappa \\approx 2.0\\text{ Å}^{-1}$$

If the tip encounters a single atomic terrace step ($\\Delta s = 0.1\\text{ nm} = 1.0\\text{ Å}$):
$$\\frac{I(s + 0.1\\text{ nm})}{I(s)} = e^{-2 \\kappa (0.1\\text{ nm})} = e^{-2.0} \\approx 0.135$$
The current **drops by over 86%**! Conversely, decreasing the tip gap by $1\\text{ Å}$ increases the current by **over 700%**!

#### 4. Piezoelectric Feedback Control Architecture
Because current varies exponentially with separation, a closed-loop electronic feedback controller coupled to a piezoelectric ceramic scanner ($PZT$) maintains the setpoint current:
* **Constant Current Mode:** As the tip rasters in the $(x,y)$ plane, the feedback loop dynamically adjusts the vertical piezo voltage $V_z$ to keep $I = I_{\\text{set}}$. The applied voltage $V_z(x,y)$ directly yields a sub-picometer topographic map of the atomic lattice.
* **Constant Height Mode:** The tip scans at a fixed vertical coordinate $z$, and the rapid fluctuations in current $\\Delta I(x,y)$ are recorded.

#### 5. Cross-Disciplinary Engineering Takeaways
1. **Flash Memory (NAND/NOR):** Floating-gate non-volatile memory utilizes **Fowler-Nordheim tunneling** through a thin silicon dioxide ($SiO_2$) dielectric layer to write and erase binary state charges.
2. **Esaki Tunnel Diodes:** Heavily doped p-n junctions exhibit quantum tunneling across narrow depletion regions, yielding **Negative Differential Resistance (NDR)** capable of microwave-frequency switching.
3. **Sub-3nm CMOS Gate Leakage:** As gate oxide thicknesses in FinFETs and Gate-All-Around (GAA) nanosheets approach $1\\text{ nm}$, unwanted quantum tunneling leakage emerges as the primary dissipation bottleneck in semiconductor scaling.
4. **Nuclear Alpha Decay (Gamow Theory):** Explains the Geiger-Nuttall law, where tiny changes in alpha-particle energy cause half-lives to vary from nanoseconds to billions of years.
"""

ENGINEERING_PRESETS = {
    "Standard STM (Au / Pt-Ir Tip)": {
        "m": 1.0,
        "E": 2.0,
        "V0": 5.0,
        "a": 0.5,
        "description": "Standard STM imaging conditions on noble metal surface (work function Φ ~ 3-5 eV, separation 5 Å)."
    },
    "High-Work-Function Barrier": {
        "m": 1.0,
        "E": 1.5,
        "V0": 8.0,
        "a": 0.6,
        "description": "Higher work function barrier representing oxide surface or wide-bandgap passivated substrate."
    },
    "Heavy Particle Suppression": {
        "m": 4.0,
        "E": 2.0,
        "V0": 5.0,
        "a": 0.4,
        "description": "Demonstrates why heavier ions or muons experience catastrophic exponential tunneling attenuation."
    },
    "Near-Barrier Resonance Regime": {
        "m": 1.0,
        "E": 4.8,
        "V0": 5.0,
        "a": 0.5,
        "description": "Particle energy close to barrier peak (E ~ V0), showing shallow evanescent decay and high transmission."
    },
    "Classical Over-Barrier (E >= V0)": {
        "m": 1.0,
        "E": 6.5,
        "V0": 5.0,
        "a": 0.5,
        "description": "Edge case: Incident energy exceeds barrier height. Classical over-barrier propagation occurs without evanescent decay."
    }
}
