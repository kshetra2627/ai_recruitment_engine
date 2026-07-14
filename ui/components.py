"""
UI Components for TechVest Recruitment Dashboard — Premium Dark SaaS Theme.
Inspired by Linear, Vercel, Stripe, Notion AI, and Cursor aesthetics.
"""

import streamlit as st
import json


def load_css():
    """Inject premium dark SaaS theme CSS."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg: #0B1020;
        --surface: #141B2D;
        --sidebar: #101624;
        --primary: #6C63FF;
        --primary-glow: rgba(108,99,255,0.25);
        --accent: #8B5CF6;
        --success: #22C55E;
        --success-glow: rgba(34,197,94,0.2);
        --warning: #F59E0B;
        --warning-glow: rgba(245,158,11,0.2);
        --danger: #EF4444;
        --danger-glow: rgba(239,68,68,0.2);
        --text: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-tertiary: #64748B;
        --border: rgba(255,255,255,0.06);
        --border-hover: rgba(108,99,255,0.25);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --shadow-card: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
        --shadow-elevated: 0 10px 40px rgba(0,0,0,0.4), 0 2px 8px rgba(0,0,0,0.3);
        --shadow-glow: 0 0 20px rgba(108,99,255,0.15);
        --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* ── Base ── */
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; box-sizing: border-box; }
    
    body { background: var(--bg); color: var(--text); }
    .stApp { background: var(--bg); }
    .main { background: var(--bg); }
    .main > div { padding: 0 1.5rem !important; max-width: 100% !important; }
    .block-container { padding: 1.2rem 2rem !important; max-width: 100% !important; }
    
    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }
    
    /* ── Brand Bar (Sticky Top Nav) ── */
    .brand-bar {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(16,22,36,0.85);
        backdrop-filter: blur(20px) saturate(1.5);
        -webkit-backdrop-filter: blur(20px) saturate(1.5);
        padding: 0.7rem 2rem;
        margin: -1.2rem -2rem 1.5rem -2rem;
        border-bottom: 1px solid var(--border);
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: calc(100% + 4rem);
        box-sizing: content-box;
    }
    .brand-left { display: flex; flex-direction: column; }
    .brand-left h1 {
        color: var(--text) !important;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.3;
        letter-spacing: -0.4px;
    }
    .brand-left h1 span { color: var(--primary); }
    .brand-left p { color: var(--text-tertiary) !important; font-size: 0.7rem; margin: 0.05rem 0 0 0; }
    .brand-right { display: flex; align-items: center; gap: 0.6rem; }
    .badge-model {
        background: rgba(108,99,255,0.12);
        color: #A5B4FC !important;
        padding: 0.2rem 0.8rem;
        border-radius: 100px;
        font-size: 0.65rem;
        font-weight: 600;
        border: 1px solid rgba(108,99,255,0.2);
        letter-spacing: 0.2px;
    }
    
    /* ── Metric Cards ── */
    .metric-card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 1.1rem 1.2rem;
        box-shadow: var(--shadow-card);
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
        text-align: center;
        min-height: 85px;
        transition: var(--transition);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-elevated);
        border-color: var(--border-hover);
    }
    .metric-card .label {
        color: var(--text-tertiary) !important;
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 0 0 0.15rem 0;
    }
    .metric-card .value {
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.8px;
        font-variant-numeric: tabular-nums;
    }
    
    /* ── Premium Card (generic) ── */
    .premium-card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 1.2rem 1.5rem;
        box-shadow: var(--shadow-card);
        border: 1px solid var(--border);
        transition: var(--transition);
    }
    .premium-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow-elevated);
    }
    
    /* ── Glass Card ── */
    .glass-card {
        background: rgba(20,27,45,0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: var(--radius-lg);
        padding: 1.2rem 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-card);
        transition: var(--transition);
    }
    .glass-card:hover {
        border-color: var(--border-hover);
    }
    
    /* ── Badges ── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.15rem 0.65rem;
        border-radius: 100px;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.2px;
        white-space: nowrap;
    }
    .badge::before {
        content: '';
        display: inline-block;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        margin-right: 2px;
    }
    .badge-select, .badge-interview {
        background: rgba(34,197,94,0.1);
        color: #4ADE80 !important;
        border: 1px solid rgba(34,197,94,0.2);
    }
    .badge-select::before, .badge-interview::before { background: #22C55E; box-shadow: 0 0 6px rgba(34,197,94,0.5); }
    .badge-hold {
        background: rgba(245,158,11,0.1);
        color: #FBBF24 !important;
        border: 1px solid rgba(245,158,11,0.2);
    }
    .badge-hold::before { background: #F59E0B; box-shadow: 0 0 6px rgba(245,158,11,0.5); }
    .badge-reject {
        background: rgba(239,68,68,0.1);
        color: #F87171 !important;
        border: 1px solid rgba(239,68,68,0.2);
    }
    .badge-reject::before { background: #EF4444; box-shadow: 0 0 6px rgba(239,68,68,0.5); }
    
    /* ── Status Chips ── */
    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.2rem 0.7rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 500;
    }
    .status-chip .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
    }
    .status-chip.approved { background: rgba(34,197,94,0.1); color: #4ADE80; border: 1px solid rgba(34,197,94,0.2); }
    .status-chip.pending { background: rgba(245,158,11,0.1); color: #FBBF24; border: 1px solid rgba(245,158,11,0.2); }
    .status-chip.rejected { background: rgba(239,68,68,0.1); color: #F87171; border: 1px solid rgba(239,68,68,0.2); }
    
    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0.5rem;
        padding-bottom: 1.5rem;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #D1D5DB !important;
    }
    section[data-testid="stSidebar"] h3 {
        color: var(--text-tertiary) !important;
        font-size: 0.6rem !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600 !important;
        padding: 0 0.5rem;
    }
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        border-radius: var(--radius-md);
        font-weight: 600;
        font-size: 0.8rem;
        padding: 0.5rem 0.8rem;
        border: none;
        transition: var(--transition);
    }
    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white !important;
        box-shadow: var(--shadow-glow);
    }
    section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(108,99,255,0.3);
        transform: translateY(-1px);
    }
    section[data-testid="stSidebar"] .stButton button[kind="secondary"] {
        background: rgba(255,255,255,0.03);
        color: var(--text-secondary) !important;
        border: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
        background: rgba(255,255,255,0.06);
        border-color: var(--border-hover);
    }
    
    /* Upload cards in sidebar */
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, var(--surface) 0%, rgba(16,22,36,0.8) 100%);
        border: 1px dashed rgba(108,99,255,0.25);
        border-radius: var(--radius-md);
        padding: 1rem;
        transition: var(--transition);
    }
    section[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
        border-color: rgba(108,99,255,0.5);
        background: linear-gradient(135deg, rgba(20,27,45,0.8) 0%, rgba(16,22,36,0.9) 100%);
    }
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] small { color: var(--text-tertiary) !important; }
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        background: var(--primary);
        color: white !important;
        border: none;
        border-radius: var(--radius-sm);
        font-size: 0.7rem;
        padding: 0.25rem 0.7rem;
    }
    
    /* Sidebar Status Card */
    .sidebar-status {
        background: rgba(255,255,255,0.02);
        border-radius: var(--radius-md);
        padding: 0.9rem 1rem;
        border: 1px solid var(--border);
    }
    .sidebar-status p { color: var(--text-secondary) !important; font-size: 0.72rem; margin: 0.35rem 0; }
    .sidebar-status .label { color: var(--text-tertiary) !important; font-size: 0.58rem; text-transform: uppercase; letter-spacing: 0.7px; font-weight: 600; }
    .sidebar-status b { color: var(--text) !important; font-weight: 600; }
    
    /* Sidebar divider */
    section[data-testid="stSidebar"] hr { 
        margin: 0.8rem 0; 
        border-color: var(--border) !important;
        opacity: 0.5;
    }
    
    /* ── Progress Bars ── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary), #8B83FF) !important;
        border-radius: 10px !important;
    }
    .stProgress > div > div {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        height: 5px !important;
    }
    
    /* Custom progress bar */
    .custom-progress {
        background: rgba(255,255,255,0.06);
        border-radius: 8px;
        height: 6px;
        overflow: hidden;
        position: relative;
    }
    .custom-progress .fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .custom-progress .fill::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
        animation: shimmer 2s infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* ── Expanders ── */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 0.82rem;
        color: var(--text);
        border-radius: var(--radius-md);
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 0.55rem 1rem !important;
        transition: var(--transition);
    }
    .streamlit-expanderHeader:hover {
        border-color: var(--border-hover);
        background: rgba(20,27,45,0.8);
    }
    .streamlit-expanderHeader svg { fill: var(--text-secondary) !important; }
    .stExpander {
        border: none;
        border-radius: var(--radius-md);
        margin-bottom: 0.5rem;
    }
    .stExpander .stMarkdown p { color: var(--text-secondary); }
    
    /* ── DataFrames ── */
    [data-testid="stDataFrame"] {
        border-radius: var(--radius-md);
        overflow: hidden;
        border: 1px solid var(--border);
    }
    [data-testid="stDataFrame"] table {
        width: 100%;
        border-collapse: collapse;
    }
    [data-testid="stDataFrame"] td {
        color: var(--text);
        background: var(--surface);
        border-bottom: 1px solid rgba(255,255,255,0.03);
        padding: 0.45rem 0.6rem !important;
        font-size: 0.78rem;
    }
    [data-testid="stDataFrame"] th {
        color: var(--text-tertiary);
        background: rgba(16,22,36,0.6);
        font-weight: 600;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        border-bottom: 1px solid var(--border);
        padding: 0.5rem 0.6rem !important;
    }
    [data-testid="stDataFrame"] tr:hover td {
        background: rgba(108,99,255,0.04);
    }
    [data-testid="stDataFrame"] tr:last-child td {
        border-bottom: none;
    }
    
    /* ── Info / Alert ── */
    .stInfo {
        border-radius: var(--radius-md);
        border: none;
        background: rgba(108,99,255,0.08);
        border-left: 3px solid var(--primary);
        padding: 0.75rem 1rem !important;
    }
    .stInfo p { color: var(--text-secondary) !important; font-size: 0.85rem; }
    .stAlert {
        background: var(--surface);
        border: 1px solid var(--border);
        color: var(--text);
        border-radius: var(--radius-md);
    }
    div[data-testid="stNotification"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
    }
    
    /* ── Horizontal Rule ── */
    hr { 
        margin: 1.2rem 0; 
        border-color: var(--border) !important;
        opacity: 0.6;
    }
    
    /* ── Tabs ── */
    .stTabs {
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
        background: rgba(255,255,255,0.02);
        border-radius: var(--radius-md);
        padding: 0.15rem;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-tertiary);
        font-weight: 500;
        font-size: 0.8rem;
        padding: 0.35rem 0.85rem;
        border-radius: var(--radius-sm);
        transition: var(--transition);
        border: none;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text);
        background: rgba(108,99,255,0.12);
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text);
        background: rgba(255,255,255,0.04);
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
    /* ── Inputs ── */
    input, textarea, .stTextInput input, .stSelectbox div, .stTextInput div {
        background: var(--surface) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.85rem !important;
        transition: var(--transition);
    }
    input:focus, textarea:focus, .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(108,99,255,0.12) !important;
    }
    input::placeholder, textarea::placeholder {
        color: var(--text-tertiary) !important;
    }
    label { color: var(--text-tertiary) !important; font-weight: 500 !important; font-size: 0.82rem !important; }
    .st-dt, .st-ae, .st-af, .st-ag { color: var(--text) !important; }
    .st-emotion-cache-1v0mbdj { color: var(--text) !important; }
    
    /* ── Selectbox ── */
    .stSelectbox div[data-baseweb="select"] > div {
        background: var(--surface) !important;
        border-color: var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }
    .stSelectbox ul {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-elevated);
    }
    .stSelectbox li {
        color: var(--text) !important;
        font-size: 0.82rem !important;
    }
    .stSelectbox li:hover {
        background: rgba(108,99,255,0.1) !important;
    }
    .stSelectbox li[aria-selected="true"] {
        background: rgba(108,99,255,0.15) !important;
    }
    
    /* ── Buttons ── */
    div.stButton > button:not([kind]) {
        border-radius: var(--radius-sm);
        font-size: 0.72rem;
        font-weight: 500;
        border: 1px solid var(--border);
        background: var(--surface);
        color: var(--text-secondary);
        transition: var(--transition);
        padding: 0.35rem 0.9rem;
    }
    div.stButton > button:not([kind]):hover {
        border-color: var(--border-hover);
        background: rgba(20,27,45,0.8);
        color: var(--text);
        box-shadow: var(--shadow-glow);
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
        color: white !important;
        border: none !important;
        box-shadow: var(--shadow-glow) !important;
        border-radius: var(--radius-sm) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 25px rgba(108,99,255,0.3) !important;
        transform: translateY(-1px);
    }
    
    /* ── Success / Warning / Error ── */
    .stSuccess {
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.15);
        color: #4ADE80;
        border-radius: var(--radius-md);
        padding: 0.6rem 1rem !important;
    }
    .stWarning {
        background: rgba(245,158,11,0.08);
        border: 1px solid rgba(245,158,11,0.15);
        color: #FBBF24;
        border-radius: var(--radius-md);
        padding: 0.6rem 1rem !important;
    }
    .stError {
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.15);
        color: #F87171;
        border-radius: var(--radius-md);
        padding: 0.6rem 1rem !important;
    }
    
    /* ── Metrics ── */
    [data-testid="stMetricLabel"] { color: var(--text-tertiary) !important; font-size: 0.7rem !important; }
    [data-testid="stMetricValue"] { color: var(--text) !important; font-size: 1.3rem !important; font-weight: 700 !important; }
    [data-testid="stMetricDelta"] { color: var(--text-tertiary) !important; }
    
    /* ── Candidate Avatar ── */
    .candidate-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        color: white;
        flex-shrink: 0;
    }
    
    /* ── Score Badge ── */
    .score-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.15rem 0.6rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 700;
        font-variant-numeric: tabular-nums;
    }
    .score-badge.high { background: rgba(34,197,94,0.12); color: #4ADE80; border: 1px solid rgba(34,197,94,0.2); }
    .score-badge.medium { background: rgba(245,158,11,0.12); color: #FBBF24; border: 1px solid rgba(245,158,11,0.2); }
    .score-badge.low { background: rgba(239,68,68,0.12); color: #F87171; border: 1px solid rgba(239,68,68,0.2); }
    
    /* ── Responsive ── */
    @media (max-width: 768px) {
        .main > div { padding: 0 0.8rem !important; }
        .block-container { padding: 0.8rem 1rem !important; }
        .brand-bar { padding: 0.5rem 1rem; margin: -0.8rem -1rem 1rem -1rem; width: calc(100% + 2rem); }
        .brand-left h1 { font-size: 0.9rem; }
    }
    
    /* ── Candidate Row Animation ── */
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .candidate-row-animate {
        animation: fadeSlideIn 0.3s ease forwards;
    }
    
    /* ── Multi-line text truncation ── */
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)


def brand_header():
    st.markdown("""
    <div class="brand-bar">
        <div class="brand-left">
            <h1>🧠 TechVest · <span>AI Recruitment</span> Agent</h1>
            <p>Intelligent candidate evaluation · LangGraph + GPT-4o Mini</p>
        </div>
        <div class="brand-right">
            <span class="badge-model">⚡ LangGraph Pipeline</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value, color: str = "#6C63FF"):
    st.markdown(f"""
    <div class="metric-card" style="border-top-color:{color};">
        <div class="label">{label}</div>
        <div class="value" style="color:{color};">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def recommendation_badge(decision: str) -> str:
    cls_map = {"SHORTLIST": "badge badge-select", "Interview": "badge badge-interview",
               "REJECT": "badge badge-reject", "Reject": "badge badge-reject",
               "HOLD": "badge badge-hold", "Hold": "badge badge-hold"}
    cls = cls_map.get(decision, "badge badge-hold")
    return f'<span class="{cls}">{decision}</span>'


def render_sidebar_status():
    status = st.session_state.get("agent_status", "Idle")
    colors = {"Idle": "#6B7280", "Running": "#6C63FF", "Complete": "#22C55E", "Error": "#EF4444"}
    dot_color = colors.get(status, "#6B7280")
    
    st.markdown(f"""
    <div class="sidebar-status">
        <p><span class="label">Status</span><br>
        <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{dot_color};margin-right:6px;box-shadow:0 0 8px {dot_color}60;"></span>
        <b>{status}</b></p>
        <p><span class="label">Step</span><br>{st.session_state.get("current_step","—") or "—"}</p>
        <p><span class="label">Candidate</span><br>{st.session_state.get("current_candidate","—") or "—"}</p>
        <p><span class="label">Injection</span><br>{"✅ Clean" if not st.session_state.get("injection_log") else "⚠️ Detected"}</p>
        <p><span class="label">Human Approval</span><br>{"✅ Approved" if st.session_state.get("human_approved",False) else "⏳ Pending"}</p>
    </div>
    """, unsafe_allow_html=True)


def candidate_row(rank: int, name: str, score: float, decision: str, slot_str: str = ""):
    """Render a premium candidate row with avatar and score badge."""
    initials = "".join(w[0] for w in name.split()[:2]).upper() if name else "?"
    score_pct = min(score, 1.0)
    score_cls = "high" if score_pct >= 0.7 else "medium" if score_pct >= 0.4 else "low"
    rank_color = "#6C63FF" if rank <= 3 else "#64748B"
    
    cols = st.columns([0.5, 2.5, 1, 1.5, 1.5, 1.8])
    with cols[0]: 
        st.markdown(f"<p style='font-weight:700;color:{rank_color};margin:0;font-size:0.85rem;font-variant-numeric:tabular-nums;'>#{rank}</p>", unsafe_allow_html=True)
    with cols[1]: 
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.5rem;">
            <div class="candidate-avatar">{initials}</div>
            <p style="margin:0;color:var(--text);font-weight:600;font-size:0.85rem;">{name}</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]: 
        st.markdown(f'<span class="score-badge {score_cls}">{score:.2f}</span>', unsafe_allow_html=True)
    with cols[3]: 
        st.markdown(f"""
        <div class="custom-progress">
            <div class="fill" style="width:{score_pct*100}%;background:linear-gradient(90deg, {rank_color}, {rank_color}dd);"></div>
        </div>
        """, unsafe_allow_html=True)
    with cols[4]: 
        st.markdown(recommendation_badge(decision), unsafe_allow_html=True)
    with cols[5]:
        if slot_str: 
            st.markdown(f"<p style='color:var(--text-tertiary);font-size:0.75rem;margin:0;'>📅 {slot_str}</p>", unsafe_allow_html=True)
        else: 
            st.markdown("<p style='color:var(--text-tertiary);margin:0;font-size:0.75rem;'>—</p>", unsafe_allow_html=True)


def criterion_bars(criteria: list):
    for c in criteria:
        name = c.get("name", "")
        score = c.get("score", 0)
        weight = c.get("weight", 0)
        evidence = (c.get("evidence", "") or "")[:90]
        pct = score / 5.0
        bar_color = "#22C55E" if score >= 4 else "#F59E0B" if score >= 2 else "#EF4444"
        
        st.markdown(f"""
        <div style="margin:0.8rem 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;margin-bottom:0.25rem;">
                <span style="color:var(--text);font-weight:600;">{name}</span>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <span style="color:var(--text-secondary);">{score}/5</span>
                    <span style="color:var(--text-tertiary);font-size:0.7rem;">{weight}%</span>
                </div>
            </div>
            <div class="custom-progress" style="height:5px;">
                <div class="fill" style="width:{pct*100}%;background:{bar_color};"></div>
            </div>
            <div style="font-size:0.7rem;color:var(--text-tertiary);margin-top:0.2rem;line-height:1.4;">{evidence}</div>
        </div>
        """, unsafe_allow_html=True)


def trajectory_step(step_num: int, entry: dict):
    tool = entry.get("tool_used", "—")
    observation = entry.get("observation", "")[:80]
    dec = entry.get("decision", "")
    
    dec_colors = {"PASSED": "#22C55E", "FLAGGED": "#F59E0B", "ERROR": "#EF4444", "SHORTLIST": "#22C55E", "REJECT": "#EF4444", "HOLD": "#F59E0B"}
    dec_color = dec_colors.get(dec, "#6C63FF")
    
    tool_icons = {
        "parse_jd": "📄", "generate_rubric": "📋", "parse_resume": "👤",
        "score_candidate": "📊", "make_decision": "⚖️", "schedule_interview": "📅"
    }
    icon = tool_icons.get(tool, "🔧")
    
    st.markdown(f"""
    <div style="display:flex;gap:0.8rem;margin:0.4rem 0;padding:0.4rem 0;animation:fadeSlideIn 0.3s ease forwards;">
        <div style="display:flex;flex-direction:column;align-items:center;min-width:36px;">
            <div style="width:28px;height:28px;border-radius:50%;background:rgba(108,99,255,0.12);border:2px solid rgba(108,99,255,0.3);display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:700;color:#A5B4FC;">{step_num}</div>
            <div style="width:1.5px;flex:1;background:rgba(255,255,255,0.04);margin:3px 0;"></div>
        </div>
        <div class="glass-card" style="flex:1;padding:0.7rem 1rem;margin-bottom:0.3rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.2rem;">
                <span style="font-weight:600;color:var(--text);font-size:0.82rem;"> {icon} {tool}</span>
                {f'<span class="status-chip" style="background:{dec_color}15;color:{dec_color};border:1px solid {dec_color}30;padding:0.1rem 0.5rem;border-radius:100px;font-size:0.65rem;font-weight:600;">{dec}</span>' if dec else ''}
            </div>
            <div style="font-size:0.72rem;color:var(--text-secondary);margin-bottom:0.2rem;line-height:1.4;">{entry.get('thought','')[:120]}</div>
            <div style="font-size:0.7rem;color:var(--text-tertiary);line-height:1.4;">{entry.get('observation','')[:120]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def interview_card(name: str, score: float, slot, approved: bool):
    border = "#22C55E" if approved else "#6C63FF"
    status = "✅ Approved" if approved else "⏳ Pending Approval"
    status_color = "#22C55E" if approved else "#F59E0B"
    initials = "".join(w[0] for w in name.split()[:2]).upper() if name else "?"
    
    st.markdown(f"""
    <div class="premium-card" style="padding:1rem 1.2rem;margin:0.6rem 0;border-left:4px solid {border};">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div style="display:flex;align-items:center;gap:0.6rem;">
                <div class="candidate-avatar">{initials}</div>
                <div>
                    <span style="font-weight:700;font-size:0.95rem;color:var(--text);">{name}</span>
                    <span style="margin-left:0.4rem;">{recommendation_badge('Interview')}</span>
                </div>
            </div>
            <div style="text-align:right;">
                <span style="font-size:0.75rem;color:var(--text-tertiary);">Score: </span>
                <span style="font-weight:700;color:var(--text);font-size:0.9rem;">{score:.2f}</span>
            </div>
        </div>
        <div style="margin-top:0.5rem;display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:0.78rem;color:var(--text-secondary);">📅 {slot.date} at {slot.time} · <span style="color:var(--text-tertiary);">{slot.format}</span></span>
            <span class="status-chip {'approved' if approved else 'pending'}" style="font-size:0.7rem;">{status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)