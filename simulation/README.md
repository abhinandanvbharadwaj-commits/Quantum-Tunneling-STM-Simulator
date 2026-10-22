# Quantum Tunneling & STM Simulator

An interactive, high-precision scientific web dashboard designed to simulate and visualize 1D Quantum Barrier Penetration, Wavefunction Evanescent Decay, and Scanning Tunneling Microscopy (STM) Nanoscale Topographic Feedback based directly on Thesis Sections 13.5 and 13.6.

---

## 🌟 Core Features

### 1. Mathematical & Physics Engine (`physics_engine.py`)
- **Decay Constant Calculation:**
  $$\kappa = \frac{\sqrt{2m(V_0 - E)}}{\hbar}$$
- **WKB Transmission Probability:**
  $$T \approx \exp(-2\kappa a)$$
- **Exact 1D Rectangular Barrier Coefficient:**
  $$T_{\text{exact}} = \left[1 + \frac{V_0^2 \sinh^2(\kappa a)}{4E(V_0 - E)}\right]^{-1}$$
- **STM Tunneling Current:**
  $$I(s) = I_0 \exp(-2\kappa s)$$
- **Relative Topographic Current Sensitivity:**
  $$\frac{\Delta I}{I} = \exp(-2\kappa \Delta s) - 1$$
- **Graceful Edge-Case Handling:** When $E \ge V_0$, classical transmission occurs ($T=1.0$), accompanied by a prominent warning banner.

### 2. Interactive Sidebar Controls
- **Particle Mass ($m$):** Range $[0.1, 10.0]\,m_e$, default $1.0\,m_e$
- **Particle Energy ($E$):** Range $[0.1, 10.0]\,\text{eV}$, default $2.0\,\text{eV}$
- **Barrier Height ($V_0$):** Range $[E + 0.1, 15.0]\,\text{eV}$, default $5.0\,\text{eV}$
- **Barrier Width / STM Gap ($a, s$):** Range $[0.05, 2.0]\,\text{nm}$, default $0.5\,\text{nm}$
- **Thesis Presets:** Standard STM, High-Work-Function Barrier, Heavy Particle Suppression, Near-Barrier Resonance, and Classical Over-Barrier.

### 3. Dashboard Visualizations (`visualization.py`)
- **Plot 1: Wavefunction Decay & Potential Barrier Layout:**
  - Rectangular potential block of height $V_0$ and width $a$.
  - Exact boundary-matched sinusoidal incident/reflected wave in Region I, evanescent decaying curve in Region II, and attenuated transmitted wave in Region III.
  - Multi-mode display: Energy-Offset Wavefunction, Probability Density $|\psi|^2$, or Raw $\text{Re}(\psi)$.
- **Plot 2: Transmission Sensitivity Curve ($T$ vs $a$):**
  - Continuous curve comparing WKB approximation and exact analytical solution.
  - Dynamic glowing marker at the active slider operating point.
  - Linear and Logarithmic scale toggles.
- **Plot 3: STM Engineering Real-World Case Study ($I$ vs $s$):**
  - Demonstrates how a $0.1\,\text{nm}$ ($1\,\text{Å}$) atomic step causes an $\approx 85\%$ current drop.
  - Highlights constant-current feedback loop and piezoelectric actuator response.
- **Plot 4: Nanoscale Tip & Surface Topography Cross-Section:**
  - Interactive schematic showing metallic tip, atomic lattice, single-atom terrace step, and vacuum tunneling gap.

### 4. UI Layout & Scientific Styling (`styles.py`)
- Sleek dark scientific UI theme with glowing accent cards (cyan, purple, emerald, rose, amber).
- Real-time KPI metrics grid displaying:
  1. Decay Constant ($\kappa$)
  2. Transmission Probability ($T$)
  3. Relative Current Change ($\%$)
  4. Penetration Depth ($\delta$)
  5. Tunneling Current ($I$)
- Sidebar collapsible reference manuals for **Thesis Section 13.5** and **Section 13.6**.
- One-click CSV simulation data export for lab reports and thesis defense.

---

## 🚀 Quickstart & Execution

### Prerequisites
- Python 3.10+
- `streamlit`, `plotly`, `numpy`, `pandas`, `scipy`

### Installation & Launch
```bash
# Clone or navigate to directory
cd simulation

# (Optional) Install dependencies
pip install -r requirements.txt

# Run Streamlit application
streamlit run app.py
```

---

## 📁 Repository Structure
```
simulation/
├── app.py                # Main Streamlit dashboard application
├── physics_engine.py     # Pure mathematical functions & TISE boundary solver
├── visualization.py      # Plotly interactive charting modules
├── thesis_content.py     # Curated scientific guidelines (Sections 13.5 & 13.6)
├── styles.py             # Dark-theme CSS, metric cards, and layout design
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```
