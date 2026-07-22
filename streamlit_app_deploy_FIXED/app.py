import base64
import streamlit as st
from pipeline import recruitment_app

# ---------------------------------------------------------------------------
# Favicon SVG (ikon kompas dengan background gradient indigo/ungu,
# senada dengan hero-icon). Streamlit tidak menerima string SVG langsung
# di page_icon, jadi di-encode dulu sebagai data URI base64.
# ---------------------------------------------------------------------------
FAVICON_SVG = """<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#4F46E5"/>
<stop offset="100%" stop-color="#7C3AED"/>
</linearGradient>
</defs>
<rect width="64" height="64" rx="16" fill="url(#g)"/>
<circle cx="32" cy="32" r="19" stroke="#FFFFFF" stroke-width="3.2"/>
<path d="M39.5 22.5L34.6 33.4L23.5 38.5L28.4 27.6L39.5 22.5Z" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="1" stroke-linejoin="round"/>
</svg>"""

FAVICON_URI = "data:image/svg+xml;base64," + base64.b64encode(FAVICON_SVG.encode("utf-8")).decode("utf-8")

st.set_page_config(
    page_title="Multi-Agent AI Recruitment System",
    page_icon=FAVICON_URI,
    layout="wide",
)

# ---------------------------------------------------------------------------
# SVG Icons (stroke-based, mengikuti warna tema indigo/ungu)
# ---------------------------------------------------------------------------
ICON_COMPASS = """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="12" cy="12" r="9" stroke="#FFFFFF" stroke-width="1.7"/>
<path d="M15.5 8.5L13.2 13.2L8.5 15.5L10.8 10.8L15.5 8.5Z" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="0.6" stroke-linejoin="round"/>
</svg>"""

ICON_COMPASS_SMALL = """<svg width="17" height="17" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="12" cy="12" r="9" stroke="#FFFFFF" stroke-width="1.8"/>
<path d="M15.5 8.5L13.2 13.2L8.5 15.5L10.8 10.8L15.5 8.5Z" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="0.6" stroke-linejoin="round"/>
</svg>"""

ICON_LLM = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="4" y="7" width="16" height="12" rx="2.5" stroke="currentColor" stroke-width="1.8"/>
<path d="M9 3.5V7M15 3.5V7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
<circle cx="9" cy="13" r="1.2" fill="currentColor"/>
<circle cx="15" cy="13" r="1.2" fill="currentColor"/>
<path d="M9 16.5C9.8 17.2 10.9 17.5 12 17.5C13.1 17.5 14.2 17.2 15 16.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
</svg>"""

ICON_RAG = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M4 5.5C4 4.7 4.7 4 5.5 4H11V19H5.5C4.7 19 4 18.3 4 17.5V5.5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
<path d="M20 5.5C20 4.7 19.3 4 18.5 4H13V19H18.5C19.3 19 20 18.3 20 17.5V5.5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
</svg>"""

ICON_DATAMINING = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M4 20V10" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
<path d="M10 20V4" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
<path d="M16 20V13" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
<path d="M4 20H20" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
</svg>"""

ICON_MULTIAGENT = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="6" cy="6" r="2.6" stroke="currentColor" stroke-width="1.7"/>
<circle cx="18" cy="6" r="2.6" stroke="currentColor" stroke-width="1.7"/>
<circle cx="12" cy="18" r="2.6" stroke="currentColor" stroke-width="1.7"/>
<path d="M8.2 7.4L10.3 15.6M15.8 7.4L13.7 15.6M8.6 6H15.4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""


def icon_html(svg: str, color: str = "#4A4842") -> str:
    """Sisipkan SVG inline dengan warna currentColor mengikuti parameter color."""
    return f'<span style="display:inline-flex;vertical-align:middle;color:{color};">{svg}</span>'


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background-color: #FAFAF9; }

/* --- FIX: header bawaan Streamlit dibuat transparan & tidak menutupi konten --- */
header[data-testid="stHeader"] {
    background: transparent;
    height: 0rem;
}

/* --- FIX: tambah padding-top agar hero header (logo + badge) tidak ketutup --- */
.block-container { padding-top: 3.5rem; padding-bottom: 2rem; max-width: 980px; }

.app-subtitle { color: #6B6963; font-size: 0.95rem; margin-top: -0.6rem; margin-bottom: 2rem; }

/* --- Kartu step --- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #E8E6E1 !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 1.4rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div { padding: 0.4rem 0.4rem; }

.step-header-box {
    border: 1.5px solid #C7BEFF;
    border-radius: 10px;
    background: #FAFAF9;
    padding: 0.9rem 1.1rem 0.9rem 1.1rem;
    margin-bottom: 1.3rem;
}
.step-label {
    display: inline-flex; align-items: center; justify-content: center;
    width: 26px; height: 26px; border-radius: 50%;
    background: #EDEAFF; color: #4F46E5; font-weight: 600; font-size: 0.85rem;
    margin-right: 0.6rem;
}
.step-title { font-size: 1.1rem; font-weight: 700; color: #1C1B1A; vertical-align: middle; }
.step-desc { color: #8A8780; font-size: 0.85rem; margin: 0.35rem 0 0 2.1rem; }

/* ===========================================================================
   HERO HEADER (background gradient mengikuti tema footer)
   =========================================================================== */
.hero-wrap {
    background: linear-gradient(135deg, #1C1B2E 0%, #2D2A5C 55%, #4F46E5 100%);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    box-shadow: 0 8px 24px rgba(45, 42, 92, 0.18);
    margin-top: 0.5rem;   /* jarak aman dari tepi atas */
    margin-bottom: 2rem;
    position: relative;
    z-index: 1;
}
.hero-header {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.hero-icon {
    flex-shrink: 0;
    width: 52px; height: 52px;
    border-radius: 14px;
    background: rgba(255,255,255,0.14);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.hero-title-group { flex: 1; }
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.12);
    color: #E8E6FF;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    margin-bottom: 0.6rem;
    border: 1px solid rgba(255,255,255,0.16);
}
.hero-eyebrow-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #22C55E;
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.35);
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin: 0 0 0.5rem 0 !important;
    color: #FFFFFF !important;
}
.hero-title .accent { color: #C7BEFF !important; }
.hero-subtitle {
    color: rgba(255,255,255,0.72);
    font-size: 1rem;
    line-height: 1.5;
    max-width: 640px;
    margin: 0;
}
.hero-tags {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.9rem;
    flex-wrap: wrap;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #E8E6FF;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.16);
    padding: 0.3rem 0.7rem;
    border-radius: 8px;
}

/* --- Text area & text input --- */
.stTextArea textarea,
.stTextInput input {
    background-color: #FFFFFF !important;
    color: #1C1B1A !important;
    border: 1px solid #D8D5CE !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
.stTextArea textarea::placeholder,
.stTextInput input::placeholder { color: #A6A39C !important; opacity: 1; }

/* --- Number input --- */
.stNumberInput > div > div,
.stNumberInput input {
    background-color: #FFFFFF !important;
    color: #1C1B1A !important;
    border-color: #D8D5CE !important;
    box-shadow: none !important;
}
.stNumberInput div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D8D5CE !important;
    border-radius: 8px !important;
}
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D8D5CE !important;
    color: #4A4842 !important;
}
button[data-testid="stNumberInputStepDown"]:hover,
button[data-testid="stNumberInputStepUp"]:hover {
    background-color: #F1F0EC !important;
    border-color: #4F46E5 !important;
}
button[data-testid="stNumberInputStepDown"] svg,
button[data-testid="stNumberInputStepUp"] svg { fill: #4A4842 !important; }

/* --- Selectbox & Multiselect --- */
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stMultiSelect"] div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D8D5CE !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
/* FIX: border sempat hilang saat penyederhanaan CSS sebelumnya — dikembalikan
   di sini, khusus untuk wrapper luar selectbox saja (bukan menyentuh tag). */
div[data-testid="stSelectbox"] > div,
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div,
div[data-testid="stMultiSelect"] > div > div[data-baseweb="select"] {
    border: 1px solid #D8D5CE !important;
    border-radius: 8px !important;
    background-color: #FFFFFF !important;
}
/* FIX: semua elemen di DALAM kotak select dibuat transparan by default.
   Sebelumnya banyak div dipaksa putih, salah satunya menumpuk di atas tag
   pertama dan menutupi huruf "K" pada "KTP". */
div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] * {
    background-color: transparent !important;
    background-image: none !important;
    background: transparent !important;
    color: #1C1B1A !important;
    -webkit-text-fill-color: #1C1B1A !important;
}

/* Ikon panah dropdown dibiarkan default (tidak disentuh CSS) supaya tidak rusak bentuknya */

div[data-baseweb="popover"] div[data-baseweb="menu"],
ul[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E8E6E1 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08) !important;
}
ul[data-baseweb="menu"] li,
div[data-baseweb="popover"] li {
    background-color: #FFFFFF !important;
    color: #1C1B1A !important;
}
ul[data-baseweb="menu"] li:hover,
div[data-baseweb="popover"] li:hover {
    background-color: #F1EFFF !important;
    color: #4F46E5 !important;
}

div[data-testid="stMultiSelect"] div[data-baseweb="select"] div[data-baseweb="tag"],
div[data-testid="stMultiSelect"] div[data-baseweb="select"] span[data-baseweb="tag"] {
    background-color: #EDEAFF !important;
    border: 1.5px solid #B7ABFF !important;
    border-radius: 6px !important;
    padding: 0.2rem 0.4rem !important;
    overflow: visible !important;
    display: inline-flex !important;
    align-items: center !important;
    position: relative !important;
    z-index: 5 !important;
}
/* FIX: elemen di dalam tag dibuat transparan (bukan diwarnai ulang), supaya
   tidak muncul kotak background ganda/gelap di belakang teks */
div[data-testid="stMultiSelect"] div[data-baseweb="select"] div[data-baseweb="tag"] div,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] div[data-baseweb="tag"] span,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] span[data-baseweb="tag"] div,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] span[data-baseweb="tag"] span {
    background-color: transparent !important;
    background: transparent !important;
    overflow: visible !important;
    white-space: nowrap !important;
    max-width: none !important;
}
div[data-baseweb="tag"] span,
span[data-baseweb="tag"] span {
    color: #4F46E5 !important;
}
div[data-baseweb="tag"] svg,
span[data-baseweb="tag"] svg { fill: #4F46E5 !important; }
div[data-baseweb="tag"]:hover,
span[data-baseweb="tag"]:hover {
    background-color: #E1DBFF !important;
}
div[data-baseweb="tag"]:hover div,
div[data-baseweb="tag"]:hover span,
span[data-baseweb="tag"]:hover div,
span[data-baseweb="tag"]:hover span {
    background-color: transparent !important;
    background: transparent !important;
}
/* FIX: pastikan tidak ada elemen ancestor yang memotong (clip) huruf pertama tag */
div[data-testid="stMultiSelect"] div[data-baseweb="select"],
div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div > div {
    overflow: visible !important;
    flex-wrap: wrap !important;
}
/* Jarak antar tag supaya border tiap tag terlihat jelas terpisah */
div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    gap: 0.4rem !important;
    row-gap: 0.4rem !important;
    padding-left: 0.5rem !important;
}
/* FIX: input pencarian/kursor di multiselect dibuat transparan & tidak melebar,
   supaya tidak ada kotak putih yang menumpuk di atas tag */
div[data-testid="stMultiSelect"] input {
    background: transparent !important;
    width: auto !important;
    min-width: 40px !important;
    flex: 1 1 auto !important;
    position: static !important;
}

.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] { color: #8A8780 !important; }

.stSlider label, .stNumberInput label, .stSelectbox label,
.stMultiSelect label, .stTextInput label, .stTextArea label {
    font-weight: 500 !important; color: #4A4842 !important; font-size: 0.9rem !important;
}

.stExpander {
    background-color: #FFFFFF !important;
    border: 1px solid #E8E6E1 !important;
    border-radius: 10px !important;
}
.stExpander summary { color: #1C1B1A !important; }

div.stButton > button, div.stFormSubmitButton > button {
    background-color: #4F46E5;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 0.7rem 0;
    transition: background-color 0.15s ease;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    background-color: #4338CA;
    color: white;
}

.result-badge {
    display: inline-block; padding: 0.35rem 0.9rem; border-radius: 999px;
    font-weight: 600; font-size: 0.9rem; margin-bottom: 0.8rem;
}
.badge-lanjut { background: #E7F6EC; color: #15803D; }
.badge-tolak { background: #FDEBEB; color: #B91C1C; }
.badge-review { background: #FFF6E5; color: #B45309; }

.result-header-box {
    border: 1px solid #E8E6E1;
    border-left: 4px solid #22C55E; /* di-override inline per status */
    border-radius: 10px;
    background: #FAFAF9;
    padding: 1.1rem 1.3rem;
}
.result-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1C1B1A;
    margin-bottom: 0.5rem;
}
.result-summary {
    color: #4A4842;
    font-size: 0.95rem;
    line-height: 1.6;
}

.agent-status-card {
    border: 1px solid #E8E6E1;
    border-left: 4px solid #22C55E; /* di-override inline per status */
    border-radius: 10px;
    background: #FAFAF9;
    padding: 1rem 1.2rem;
}
.agent-status-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.82rem;
    margin-bottom: 0.6rem;
}
.agent-status-reason {
    color: #4A4842;
    font-size: 0.93rem;
    line-height: 1.6;
}
.agent-caption {
    margin-top: 0.7rem;
    padding-top: 0.6rem;
    border-top: 1px dashed #E8E6E1;
    color: #8A8780;
    font-size: 0.8rem;
}

.dm-prob-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.9rem;
    margin-bottom: 0.4rem;
}
.dm-prob-label {
    color: #6B6963;
    font-size: 0.85rem;
}
.dm-prob-value {
    font-weight: 700;
    font-size: 0.95rem;
}
.dm-prob-track {
    width: 100%;
    height: 10px;
    background: #EDEBE6;
    border-radius: 999px;
    overflow: hidden;
}
.dm-prob-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.3s ease;
}

/* ===========================================================================
   FOOTER
   =========================================================================== */
footer, #MainMenu { visibility: hidden; }

.app-footer-wrap {
    margin-top: 3rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #1C1B2E 0%, #2D2A5C 55%, #4F46E5 100%);
    padding: 1.8rem 2rem;
    box-shadow: 0 8px 24px rgba(45, 42, 92, 0.18);
}
.app-footer-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    padding-bottom: 1.1rem;
    margin-bottom: 1.1rem;
    border-bottom: 1px solid rgba(255,255,255,0.14);
}
.app-footer-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.app-footer-brand-icon {
    width: 34px; height: 34px;
    border-radius: 9px;
    background: rgba(255,255,255,0.12);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.app-footer-brand-text {
    color: #FFFFFF;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: -0.01em;
}
.app-footer-badges {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.app-footer-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: #E8E6FF;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.16);
    padding: 0.28rem 0.65rem;
    border-radius: 999px;
}
.app-footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.6rem;
}
.app-footer-caption {
    color: rgba(255,255,255,0.65);
    font-size: 0.8rem;
}
.app-footer-project {
    color: rgba(255,255,255,0.9);
    font-size: 0.8rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="hero-header">
            <div class="hero-icon">{ICON_COMPASS}</div>
            <div class="hero-title-group">
                <div class="hero-eyebrow">
                    <span class="hero-eyebrow-dot"></span> Sistem Aktif
                </div>
                <h1 class="hero-title">Enterprise Multi-Agent <span class="accent">AI Recruitment System</span></h1>
                <p class="hero-subtitle">
                    Menggunakan LLM (Llama 3), RAG, dan Data Mining untuk mendukung
                    seleksi awal kandidat secara otomatis, konsisten, dan berbasis data.
                </p>
                <div class="hero-tags">
                    <span class="hero-tag">{icon_html(ICON_LLM, '#E8E6FF')} LLM · Llama 3</span>
                    <span class="hero-tag">{icon_html(ICON_RAG, '#E8E6FF')} RAG</span>
                    <span class="hero-tag">{icon_html(ICON_DATAMINING, '#E8E6FF')} Data Mining</span>
                    <span class="hero-tag">{icon_html(ICON_MULTIAGENT, '#E8E6FF')} Multi-Agent</span>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


def step_header(number: str, title: str, desc: str):
    st.markdown(
        f'<div class="step-header-box">'
        f'<span class="step-label">{number}</span><span class="step-title">{title}</span>'
        f'<div class="step-desc">{desc}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _clean_detail_text(status: str, detail: str) -> str:
    """Buang prefix 'STATUS: ... ALASAN:' yang duplikat dari teks detail,
    supaya tidak tampil dobel dengan badge status yang sudah ditampilkan."""
    text = detail.strip()
    upper = text.upper()
    if "ALASAN:" in upper:
        idx = upper.find("ALASAN:")
        text = text[idx + len("ALASAN:"):].strip()
    elif upper.startswith("STATUS:"):
        # buang "STATUS: <status>" di awal kalau tidak ada kata ALASAN
        text = text[len("STATUS:"):].strip()
        if text.upper().startswith(status.upper()):
            text = text[len(status):].strip(" :-")
    return text if text else detail.strip()


def render_agent_status(status: str, detail: str, extra_caption: str = ""):
    """Render status agent sebagai badge berwarna + teks alasan yang rapi."""
    status_lower = status.lower()
    negative_keywords = ["tidak", "belum", "gagal", "kurang"]
    is_negative = any(k in status_lower for k in negative_keywords)

    if is_negative:
        badge_bg, badge_color, accent = "#FDEBEB", "#B91C1C", "#EF4444"
    else:
        badge_bg, badge_color, accent = "#E7F6EC", "#15803D", "#22C55E"

    reason = _clean_detail_text(status, detail)

    caption_html = (
        f'<div class="agent-caption">{extra_caption}</div>' if extra_caption else ""
    )

    st.markdown(
        f"""
        <div class="agent-status-card" style="border-left-color:{accent};">
            <span class="agent-status-badge" style="background:{badge_bg}; color:{badge_color};">{status}</span>
            <div class="agent-status-reason">{reason}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Form
# ---------------------------------------------------------------------------
with st.form("candidate_form"):

    with st.container(border=True):
        step_header("1", "CV & job description", "Tempel isi CV kandidat dan lowongan yang dilamar")
        col1, col2 = st.columns(2)
        with col1:
            cv_text = st.text_area("CV kandidat", height=200, placeholder="Tempel isi CV kandidat di sini...")
        with col2:
            job_description = st.text_area("Job description", height=200, placeholder="Tempel isi job description di sini...")

    with st.container(border=True):
        step_header("2", "Skor asesmen kandidat", "Diisi berdasarkan hasil tes/wawancara — dipakai oleh Data Mining Agent")

        s1, s2, s3 = st.columns(3)
        with s1:
            interview_score = st.slider("Interview score", 0, 100, 78)
        with s2:
            skill_score = st.slider("Skill score", 0, 100, 82)
        with s3:
            personality_score = st.slider("Personality score", 0, 100, 74)

        b1, b2, b3 = st.columns(3)
        with b1:
            age = st.number_input("Usia", min_value=18, max_value=65, value=26)
        with b2:
            gender = st.selectbox("Jenis kelamin", ["Male", "Female"])
        with b3:
            education_level = st.selectbox(
                "Pendidikan terakhir", [1, 2, 3, 4], index=2,
                format_func=lambda x: {1: "SMA", 2: "D3", 3: "S1", 4: "S2/S3"}[x],
            )

        with st.expander("Detail lanjutan (opsional)"):
            d1, d2, d3 = st.columns(3)
            with d1:
                experience_years = st.number_input("Experience years", min_value=0, max_value=40, value=3)
            with d2:
                previous_companies = st.number_input("Previous companies", min_value=0, max_value=20, value=2)
            with d3:
                distance_from_company = st.number_input("Jarak ke kantor (km)", min_value=0.0, value=12.5)
            recruitment_strategy = st.selectbox(
                "Recruitment strategy", [1, 2, 3], index=1,
                format_func=lambda x: {1: "Referral", 2: "Job portal", 3: "Headhunter"}[x],
            )

    with st.container(border=True):
        step_header("3", "Finance & legal", "Ekspektasi gaji, level posisi, dan dokumen yang sudah dimiliki kandidat")

        f1, f2 = st.columns(2)
        with f1:
            expected_salary = st.number_input("Ekspektasi gaji (Rp)", min_value=0, value=10_000_000, step=500_000)
            position_level = st.selectbox(
                "Level posisi", ["Staff", "Officer/Senior Staff", "Supervisor", "Manager"], index=1
            )
        with f2:
            legal_documents = st.multiselect(
                "Dokumen legal yang sudah dimiliki kandidat",
                ["KTP", "Ijazah", "SKCK", "NPWP", "Kartu Keluarga", "Surat Keterangan Sehat"],
                default=["KTP", "Ijazah", "SKCK", "NPWP"],
            )
            candidate_id = st.text_input("Candidate ID", value="CAND-WEB-001")

    submitted = st.form_submit_button("Proses kandidat", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Hasil
# ---------------------------------------------------------------------------
if submitted:
    if not cv_text.strip() or not job_description.strip():
        st.error("CV dan job description tidak boleh kosong.")
    else:
        initial_state = {
            "candidate_id": candidate_id,
            "cv_text": cv_text,
            "job_description": job_description,
            "candidate_data": {
                "features": {
                    "Age": age,
                    "Gender": gender,
                    "EducationLevel": education_level,
                    "ExperienceYears": experience_years,
                    "PreviousCompanies": previous_companies,
                    "DistanceFromCompany": distance_from_company,
                    "InterviewScore": interview_score,
                    "SkillScore": skill_score,
                    "PersonalityScore": personality_score,
                    "RecruitmentStrategy": recruitment_strategy,
                },
                "expected_salary": expected_salary,
                "position_level": position_level,
                "legal_documents": legal_documents,
            },
            "hr_check": {},
            "skill_match": {},
            "finance_check": {},
            "legal_check": {},
            "prediction_result": {},
            "final_recommendation": "",
        }

        with st.spinner("Memproses kandidat melalui seluruh agent..."):
            try:
                final_state = recruitment_app.invoke(initial_state)
            except Exception as e:
                st.error(f"Terjadi error saat menjalankan pipeline: {e}")
                st.stop()

        st.markdown("---")

        decision_text = final_state["final_recommendation"].lower()
        if "lanjut" in decision_text and "tidak" not in decision_text.split("keputusan")[-1][:40]:
            badge_class, badge_text = "badge-lanjut", "Lanjut ke interview"
            accent_color = "#22C55E"
        elif "review" in decision_text:
            badge_class, badge_text = "badge-review", "Perlu review manual"
            accent_color = "#F59E0B"
        else:
            badge_class, badge_text = "badge-tolak", "Tidak lanjut"
            accent_color = "#EF4444"

        with st.container(border=True):
            st.markdown(
                f'<div class="result-header-box" style="border-left-color:{accent_color};">'
                f'<span class="result-badge {badge_class}">{badge_text}</span>'
                f'<div class="result-title">Ringkasan untuk {candidate_id}</div>'
                f'<div class="result-summary">{final_state["final_recommendation"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with st.container(border=True):
            step_header("i", "Detail per agent", "Rincian hasil pemeriksaan dari masing-masing agent")
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["HR", "Skill matching", "Finance", "Legal", "Data mining"]
            )
            with tab1:
                render_agent_status(
                    final_state["hr_check"]["status"],
                    final_state["hr_check"]["detail"],
                )
            with tab2:
                score = final_state["skill_match"]["score"]
                render_agent_status(
                    f"Skor {score}",
                    final_state["skill_match"]["detail"],
                )
            with tab3:
                render_agent_status(
                    "Selesai diperiksa",
                    final_state["finance_check"]["detail"],
                    extra_caption=f"Sumber dokumen: {', '.join(final_state['finance_check']['sources'])}",
                )
            with tab4:
                render_agent_status(
                    "Selesai diperiksa",
                    final_state["legal_check"]["detail"],
                    extra_caption=f"Sumber dokumen: {', '.join(final_state['legal_check']['sources'])}",
                )
            with tab5:
                label = final_state["prediction_result"]["label"]
                probability = final_state["prediction_result"]["probability"]

                label_lower = label.lower()
                is_negative_pred = any(
                    k in label_lower for k in ["tidak", "belum", "gagal", "kurang"]
                )
                if is_negative_pred:
                    pred_bg, pred_color, pred_accent = "#FDEBEB", "#B91C1C", "#EF4444"
                else:
                    pred_bg, pred_color, pred_accent = "#E7F6EC", "#15803D", "#22C55E"

                pct = probability * 100
                st.markdown(
                    f"""
                    <div class="agent-status-card" style="border-left-color:{pred_accent};">
                        <span class="agent-status-badge" style="background:{pred_bg}; color:{pred_color};">{label}</span>
                        <div class="dm-prob-row">
                            <span class="dm-prob-label">Probabilitas keyakinan model</span>
                            <span class="dm-prob-value" style="color:{pred_color};">{pct:.2f}%</span>
                        </div>
                        <div class="dm-prob-track">
                            <div class="dm-prob-fill" style="width:{pct:.2f}%; background:{pred_accent};"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="app-footer-wrap">
        <div class="app-footer-top">
            <div class="app-footer-brand">
                <div class="app-footer-brand-icon">{ICON_COMPASS_SMALL}</div>
                <div class="app-footer-brand-text">AI Recruitment System</div>
            </div>
            <div class="app-footer-badges">
                <span class="app-footer-badge">{icon_html(ICON_LLM, '#E8E6FF')} Llama 3</span>
                <span class="app-footer-badge">{icon_html(ICON_RAG, '#E8E6FF')} RAG</span>
                <span class="app-footer-badge">{icon_html(ICON_MULTIAGENT, '#E8E6FF')} Multi-Agent</span>
            </div>
        </div>
        <div class="app-footer-bottom">
            <div class="app-footer-caption">Enterprise Multi-Agent AI Recruitment System</div>
            <div class="app-footer-project">Final Project · ST167 CPMK22.6</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
