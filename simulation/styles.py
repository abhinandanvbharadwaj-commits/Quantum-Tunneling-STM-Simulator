"""
Quantum Tunneling & STM Simulator - Custom CSS & UI Styling
===========================================================
Modern, dark-themed scientific UI styling with glassmorphism, glowing badges,
and responsive KPI metric cards.
"""

def get_custom_css() -> str:
    """
    Returns embedded CSS for a high-end dark scientific aesthetic.
    """
    return """
    <style>
    /* Dark Theme Core Styles */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 96%;
    }

    /* Header Title Container */
    .header-banner {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(0, 240, 255, 0.25);
        border-radius: 12px;
        padding: 1.2rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4), 0 0 15px rgba(0, 240, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .header-title {
        font-size: 1.85rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00F0FF, #A855F7, #00FFA3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .header-subtitle {
        color: #9CA3AF;
        font-size: 0.92rem;
        margin-top: 0.25rem;
        font-weight: 400;
    }

    /* KPI Metric Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .kpi-card {
        background: rgba(17, 24, 39, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
    }

    .kpi-cyan {
        border-left: 4px solid #00F0FF;
    }
    .kpi-cyan:hover {
        border-color: rgba(0, 240, 255, 0.5);
    }

    .kpi-purple {
        border-left: 4px solid #A855F7;
    }
    .kpi-purple:hover {
        border-color: rgba(168, 85, 247, 0.5);
    }

    .kpi-emerald {
        border-left: 4px solid #00FFA3;
    }
    .kpi-emerald:hover {
        border-color: rgba(0, 255, 163, 0.5);
    }

    .kpi-rose {
        border-left: 4px solid #F43F5E;
    }
    .kpi-rose:hover {
        border-color: rgba(244, 63, 94, 0.5);
    }

    .kpi-amber {
        border-left: 4px solid #F59E0B;
    }
    .kpi-amber:hover {
        border-color: rgba(245, 158, 11, 0.5);
    }

    .kpi-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #9CA3AF;
        margin-bottom: 0.35rem;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 1.45rem;
        font-weight: 700;
        color: #F3F4F6;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }

    .kpi-caption {
        font-size: 0.75rem;
        color: #6B7280;
    }

    /* Warning Banner for Classical Transmission */
    .alert-banner {
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-left: 5px solid #F59E0B;
        border-radius: 8px;
        padding: 0.85rem 1.2rem;
        margin-bottom: 1.2rem;
        color: #FDE68A;
        font-size: 0.9rem;
    }

    /* Sidebar Customizations */
    [data-testid="stSidebar"] {
        background-color: #0E131F !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Pills & Badges */
    .pill-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .pill-cyan {
        background: rgba(0, 240, 255, 0.15);
        color: #00F0FF;
        border: 1px solid rgba(0, 240, 255, 0.3);
    }

    .pill-amber {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .pill-purple {
        background: rgba(168, 85, 247, 0.15);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }

    /* Section divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
        margin: 1.5rem 0;
    }

    /* Footer styling */
    .dashboard-footer {
        text-align: center;
        color: #6B7280;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """


def render_kpi_card(
    label: str,
    value: str,
    caption: str,
    color_class: str = "kpi-cyan"
) -> str:
    """
    Renders an HTML-styled metric card with glowing accent border.
    """
    return f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-caption">{caption}</div>
    </div>
    """
