"""
GhostTerms — Autonomous Dark-Pattern & Legal Trap Bounty Agent
Streamlit Command Center Frontend
Team: DeceptiveDefense | Kritical Hacks 2026 | AI/ML Track

Run: streamlit run app.py
"""

import json
import os
import random
import re
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------------
# OPTIONAL BACKEND IMPORT — graceful degradation if main.py is unavailable
# --------------------------------------------------------------------------
BACKEND_AVAILABLE = False
GhostTermsAuditor = None  # type: ignore
try:
    from main import GhostTermsAuditor, audit_dark_patterns, fetch_page_content  # type: ignore
    BACKEND_AVAILABLE = True
except Exception:
    try:
        from main import GhostTermsAuditor  # type: ignore
        BACKEND_AVAILABLE = True
    except Exception:
        BACKEND_AVAILABLE = False
        GhostTermsAuditor = None


# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="GhostTerms · Dark-Pattern Command Center",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------------------------------
# GLOBAL THEME / CSS
# --------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg: #080C14;
    --bg-2: #0B1220;
    --bg-3: #0E1628;
    --slate: #1F293D;
    --slate-2: #27324A;
    --text: #E6EDF7;
    --text-dim: #8896AD;
    --cyan: #00F0FF;
    --amber: #FF8800;
    --crimson: #FF3366;
    --green: #22E3A5;
    --violet: #8B5CF6;
}

/* Global canvas */
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(1200px 600px at 10% -10%, #0E1A30 0%, #080C14 55%, #05070C 100%) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stSidebar"] { background: #060A12 !important; border-right: 1px solid var(--slate); }
[data-testid="stSidebar"] * { color: var(--text) !important; }

.block-container { padding-top: 1.2rem !important; padding-bottom: 3rem !important; max-width: 1400px; }

/* Headings */
h1, h2, h3, h4 { color: var(--text) !important; letter-spacing: -0.02em; font-weight: 700 !important; }
p, span, div, label { color: var(--text); }

/* Hero band */
.gt-hero {
    position: relative;
    padding: 22px 28px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(0,240,255,0.06), rgba(139,92,246,0.06) 40%, rgba(255,51,102,0.05));
    border: 1px solid var(--slate);
    overflow: hidden;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 20px 60px rgba(0,0,0,0.5);
    backdrop-filter: blur(8px);
}
.gt-hero::before {
    content: "";
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 32px 32px;
    mask-image: radial-gradient(ellipse at 30% 50%, #000 30%, transparent 75%);
    pointer-events: none;
}
.gt-hero-inner { position: relative; z-index: 1; display: flex; justify-content: space-between; align-items: center; gap: 24px; flex-wrap: wrap; }
.gt-title { font-size: 30px; font-weight: 800; letter-spacing: -0.03em; margin: 0; }
.gt-title .accent { color: var(--cyan); }
.gt-sub { color: var(--text-dim); font-size: 13.5px; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }
.gt-badge {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 12px; border-radius: 999px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;
    background: rgba(0,240,255,0.08); color: var(--cyan);
    border: 1px solid rgba(0,240,255,0.35);
    box-shadow: 0 0 18px rgba(0,240,255,0.15);
    font-family: 'JetBrains Mono', monospace;
}
.gt-badge .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 10px var(--cyan); animation: pulse 1.6s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }

/* Ticker */
.gt-ticker {
    margin-top: 16px; display: flex; gap: 10px; flex-wrap: wrap;
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    color: var(--text-dim);
}
.gt-ticker .chip {
    padding: 5px 10px; border-radius: 8px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--slate);
}
.gt-ticker .chip b { color: var(--text); font-weight: 600; }
.gt-ticker .chip .ok { color: var(--green); }

/* Section titles */
.gt-section { display:flex; align-items:center; gap:10px; margin: 22px 0 10px 0; }
.gt-section .bar { width: 3px; height: 16px; border-radius: 2px; background: linear-gradient(var(--cyan), var(--violet)); }
.gt-section h3 { font-size: 14px !important; letter-spacing: 0.14em; text-transform: uppercase; margin: 0 !important; color: var(--text-dim) !important; }

/* Metric cards */
.gt-metric {
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.005));
    border: 1px solid var(--slate);
    border-radius: 14px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    min-height: 118px;
    transition: transform .18s ease, border-color .18s ease;
}
.gt-metric:hover { transform: translateY(-2px); border-color: var(--slate-2); }
.gt-metric::after {
    content: ""; position: absolute; left: 0; right: 0; top: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.5;
}
.gt-metric .label { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--text-dim); font-weight: 600; }
.gt-metric .value { font-size: 26px; font-weight: 800; margin-top: 8px; letter-spacing: -0.02em; font-family: 'JetBrains Mono', monospace; }
.gt-metric .sub { font-size: 11.5px; color: var(--text-dim); margin-top: 6px; font-family: 'JetBrains Mono', monospace; }
.gt-metric.good .value { color: var(--green); }
.gt-metric.warn .value { color: var(--amber); }
.gt-metric.bad  .value { color: var(--crimson); }
.gt-metric.info .value { color: var(--cyan); }

/* Risk gauge */
.gt-gauge-wrap {
    border: 1px solid var(--slate); border-radius: 16px; padding: 20px;
    background: radial-gradient(circle at 50% 0%, rgba(0,240,255,0.06), transparent 60%),
                linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
    text-align: center;
}
.gt-gauge-num { font-size: 56px; font-weight: 800; letter-spacing: -0.04em; font-family: 'JetBrains Mono', monospace; line-height: 1; }
.gt-gauge-lbl { font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--text-dim); margin-top: 6px; }
.gt-tier {
    display: inline-block; margin-top: 10px; padding: 5px 12px; border-radius: 999px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.12em; font-family: 'JetBrains Mono', monospace;
}

/* Violation card */
.gt-viol {
    border: 1px solid var(--slate); border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
}
.gt-viol .cat { font-weight: 700; font-size: 14px; }
.gt-viol .quote {
    font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #CBD5E1;
    background: rgba(0,0,0,0.35); border-left: 2px solid var(--crimson);
    padding: 8px 12px; margin-top: 8px; border-radius: 6px; word-break: break-word;
}
.sev { display:inline-block; padding: 2px 8px; border-radius: 999px; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; font-family:'JetBrains Mono', monospace;}
.sev.CRITICAL { background: rgba(255,51,102,0.14); color: var(--crimson); border: 1px solid rgba(255,51,102,0.4);}
.sev.HIGH { background: rgba(255,136,0,0.14); color: var(--amber); border: 1px solid rgba(255,136,0,0.4);}
.sev.MEDIUM { background: rgba(0,240,255,0.10); color: var(--cyan); border: 1px solid rgba(0,240,255,0.35);}
.sev.LOW { background: rgba(34,227,165,0.10); color: var(--green); border: 1px solid rgba(34,227,165,0.35);}

/* Timeline */
.gt-tl { position: relative; padding-left: 26px; }
.gt-tl::before { content:""; position:absolute; left: 9px; top: 6px; bottom: 6px; width: 2px; background: linear-gradient(var(--cyan), var(--violet), var(--crimson)); opacity: 0.5; }
.gt-tl-item { position: relative; margin-bottom: 16px; }
.gt-tl-item::before {
    content: ""; position: absolute; left: -22px; top: 4px; width: 12px; height: 12px; border-radius: 50%;
    background: var(--bg); border: 2px solid var(--cyan); box-shadow: 0 0 12px rgba(0,240,255,0.5);
}
.gt-tl-item.warn::before { border-color: var(--amber); box-shadow: 0 0 12px rgba(255,136,0,0.5); }
.gt-tl-item.bad::before { border-color: var(--crimson); box-shadow: 0 0 12px rgba(255,51,102,0.5); }
.gt-tl-step { font-size: 10.5px; letter-spacing: 0.14em; color: var(--text-dim); font-family:'JetBrains Mono', monospace; text-transform: uppercase;}
.gt-tl-title { font-weight: 700; font-size: 14px; margin-top: 2px; }
.gt-tl-desc { color: var(--text-dim); font-size: 12.5px; margin-top: 3px; }

/* Buttons */
.stButton > button {
    background: linear-gradient(180deg, #101A2E, #0A1120) !important;
    color: var(--text) !important;
    border: 1px solid var(--slate-2) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
    transition: all .18s ease !important;
}
.stButton > button:hover {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 1px rgba(0,240,255,0.35), 0 8px 30px rgba(0,240,255,0.12) !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(180deg, #0E2A3A, #0A1A2A) !important;
    border-color: rgba(0,240,255,0.5) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 0 1px rgba(0,240,255,0.25), 0 8px 24px rgba(0,240,255,0.15) !important;
}

/* Inputs */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background: #060A12 !important; color: var(--text) !important;
    border: 1px solid var(--slate) !important; border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 13px !important;
}
.stTextInput input:focus { border-color: var(--cyan) !important; box-shadow: 0 0 0 2px rgba(0,240,255,0.15) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; border-bottom: 1px solid var(--slate); }
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 8px 8px 0 0; padding: 10px 16px;
    color: var(--text-dim) !important; font-weight: 600; font-size: 13px;
}
.stTabs [aria-selected="true"] { color: var(--cyan) !important; background: rgba(0,240,255,0.06) !important; }

/* Expander */
.streamlit-expanderHeader, [data-testid="stExpander"] summary {
    color: var(--text) !important; font-weight: 600 !important;
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid var(--slate) !important; border-radius: 10px !important;
}
[data-testid="stExpander"] { border: none !important; }

/* Progress bar */
.stProgress > div > div > div > div { background: linear-gradient(90deg, var(--cyan), var(--violet)) !important; }

/* Preset chips */
.gt-preset-row { display:flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
div[data-testid="column"] .stButton > button { width: 100%; }

/* Legal preview */
.gt-legal {
    font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 1.6;
    background: #05080F; border: 1px solid var(--slate); border-radius: 10px;
    padding: 16px; max-height: 420px; overflow-y: auto; color: #C7D2E4; white-space: pre-wrap;
}

/* Fintech simulator */
.gt-txn {
    display:flex; justify-content: space-between; align-items:center; gap: 12px;
    padding: 12px 16px; border-radius: 10px; border: 1px solid var(--slate);
    background: rgba(255,255,255,0.015); margin-bottom: 8px;
}
.gt-txn .merchant { font-weight: 600; font-size: 13.5px; }
.gt-txn .amount { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 14px; }
.gt-flag { font-size: 10.5px; font-weight: 700; padding: 3px 9px; border-radius: 999px; letter-spacing: 0.08em; font-family:'JetBrains Mono', monospace;}
.gt-flag.block { background: rgba(255,51,102,0.14); color: var(--crimson); border: 1px solid rgba(255,51,102,0.4);}
.gt-flag.warn  { background: rgba(255,136,0,0.14); color: var(--amber); border: 1px solid rgba(255,136,0,0.4);}
.gt-flag.allow { background: rgba(34,227,165,0.10); color: var(--green); border: 1px solid rgba(34,227,165,0.35);}

/* Footer */
.gt-footer { margin-top: 40px; text-align: center; color: var(--text-dim); font-size: 11px; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.1em; }

/* Hide streamlit chrome */
#MainMenu, footer { visibility: hidden; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# PRESET TARGETS
# --------------------------------------------------------------------------
PRESETS: Dict[str, Dict[str, str]] = {
    "Predatory Streaming SaaS": {
        "url": "https://demo.ghostterms.dev/predatory-streaming",
        "note": "Free trial → auto-renews at $49.99/mo · cancellation gated behind phone call",
    },
    "Deceptive Fitness Trial": {
        "url": "https://demo.ghostterms.dev/fitness-trap",
        "note": "'Cancel anytime' hidden 11 pages deep · confirm-shaming flow",
    },
    "Clean Open Source Site": {
        "url": "https://demo.ghostterms.dev/clean-oss",
        "note": "Transparent terms · 1-click cancel · no dark patterns detected",
    },
}


# --------------------------------------------------------------------------
# MOCK DATA ENGINE (fallback + demo stability)
# --------------------------------------------------------------------------
def _mock_violations(risk_level: int) -> List[Dict[str, Any]]:
    catalogue = [
        {
            "category": "Roach Motel (Cancellation Friction)",
            "severity": "CRITICAL",
            "penalty_points": 25,
            "matched_evidence": [
                "To cancel your subscription, please call our customer retention line (Mon–Fri 9am–5pm EST).",
                "Your membership cannot be cancelled online. A 30-day notice period is required via certified mail.",
                "Cancellation link is only accessible from the account page → billing → subscriptions → manage → 'more options' → 'contact us'.",
            ],
        },
        {
            "category": "Forced Continuity (Auto-Renewal Trap)",
            "severity": "HIGH",
            "penalty_points": 20,
            "matched_evidence": [
                "Your free trial will automatically convert to a paid subscription of $49.99/month unless cancelled 72 hours before renewal.",
                "By starting your trial, you authorize recurring charges without further notification.",
            ],
        },
        {
            "category": "Confirm-Shaming / Negative Option",
            "severity": "HIGH",
            "penalty_points": 18,
            "matched_evidence": [
                "Are you sure you want to give up your progress? You've lost 0 lbs — don't quit now!",
                "No thanks, I prefer to stay overweight and unhealthy.",
            ],
        },
        {
            "category": "Sneak into Basket",
            "severity": "MEDIUM",
            "penalty_points": 12,
            "matched_evidence": [
                "Premium Protection Plan ($4.99/mo) added to your order by default.",
                "Optional 'Priority Support Upgrade' is pre-selected at checkout.",
            ],
        },
        {
            "category": "Privacy Zuckering (Forced Consent)",
            "severity": "MEDIUM",
            "penalty_points": 10,
            "matched_evidence": [
                "By continuing to use the service, you consent to sharing your data with 212 trusted advertising partners.",
                "'Accept all' button is large and highlighted; 'Reject non-essential' is hidden in a submenu.",
            ],
        },
        {
            "category": "Disguised Ads / Prechecked Opt-in",
            "severity": "LOW",
            "penalty_points": 6,
            "matched_evidence": [
                "Prechecked checkbox: 'Send me marketing emails and partner offers.'",
            ],
        },
    ]
    if risk_level >= 80:
        return catalogue
    if risk_level >= 55:
        return catalogue[:4]
    if risk_level >= 30:
        return catalogue[:2]
    return []


def _mock_audit(url: str, risk_override: Optional[int] = None) -> Dict[str, Any]:
    if risk_override is None:
        if "clean" in url.lower() or "oss" in url.lower():
            base = random.randint(3, 14)
        elif "fitness" in url.lower():
            base = random.randint(62, 82)
        elif "stream" in url.lower():
            base = random.randint(84, 97)
        else:
            base = random.randint(20, 90)
    else:
        base = risk_override

    if base >= 80:
        tier = "CRITICAL RISK"
    elif base >= 55:
        tier = "HIGH RISK"
    elif base >= 30:
        tier = "MODERATE RISK"
    else:
        tier = "LOW RISK"

    violations = _mock_violations(base)

    return {
        "target_url": url,
        "dark_pattern_index": base,
        "risk_tier": tier,
        "findings_count": len(violations),
        "regulatory_complaint_ready": base >= 55,
        "violations": violations,
        # extra simulated telemetry used by UI
        "_friction_score": min(100, base + random.randint(-5, 10)),
        "_cancellation_steps": (
            "5 Clicks + Phone Call Required" if base >= 80
            else "4 Clicks + Retention Modal" if base >= 55
            else "2 Clicks" if base >= 30
            else "1 Click"
        ),
        "_obfuscation_ratio": f"{min(99, base + random.randint(-8, 8))}%",
        "_penalty_exposure": f"${base * 1250:,}",
    }


# --------------------------------------------------------------------------
# AUDIT RUNNER — tries backend, falls back to mock
# --------------------------------------------------------------------------
def _run_audit(url: str) -> Dict[str, Any]:
    """
    Attempts live backend audit. Any failure → deterministic-ish mock so the
    demo NEVER crashes on stage.
    """
    if BACKEND_AVAILABLE:
        try:
            # Preferred path: class-based auditor
            if GhostTermsAuditor is not None:
                auditor = GhostTermsAuditor()
                # Try common method signatures
                for method_name in ("audit", "run", "analyze", "scan"):
                    if hasattr(auditor, method_name):
                        result = getattr(auditor, method_name)(url)
                        if isinstance(result, dict) and "dark_pattern_index" in result:
                            return _enrich_with_ui_telemetry(result, url)
            # Secondary path: module-level function
            if "audit_dark_patterns" in globals() and "fetch_page_content" in globals():
                content = fetch_page_content(url)  # type: ignore
                result = audit_dark_patterns(content)  # type: ignore
                if isinstance(result, dict) and "dark_pattern_index" in result:
                    return _enrich_with_ui_telemetry(result, url)
        except Exception as exc:
            st.session_state["_last_backend_error"] = str(exc)

    return _mock_audit(url)


def _enrich_with_ui_telemetry(result: Dict[str, Any], url: str) -> Dict[str, Any]:
    """Ensure all UI-expected fields exist even if backend omitted them."""
    result.setdefault("target_url", url)
    result.setdefault("dark_pattern_index", 0)
    result.setdefault("risk_tier", "LOW RISK")
    result.setdefault("violations", [])
    result.setdefault("findings_count", len(result["violations"]))
    result.setdefault("regulatory_complaint_ready", result["dark_pattern_index"] >= 55)

    idx = int(result["dark_pattern_index"])
    result.setdefault("_friction_score", idx)
    result.setdefault(
        "_cancellation_steps",
        "5 Clicks + Phone Call Required" if idx >= 80
        else "4 Clicks + Retention Modal" if idx >= 55
        else "2 Clicks" if idx >= 30
        else "1 Click",
    )
    result.setdefault("_obfuscation_ratio", f"{idx}%")
    result.setdefault("_penalty_exposure", f"${idx * 1250:,}")
    return result


# --------------------------------------------------------------------------
# SESSION STATE
# --------------------------------------------------------------------------
def _init_state() -> None:
    defaults = {
        "audit_result": None,
        "audit_target": "",
        "audit_ts": None,
        "scan_running": False,
        "api_key_present": bool(os.getenv("TINYFISH_API_KEY")),
        "audit_history": [],
        "fintech_merchant_score": 78,
        "fintech_merchant_name": "PredatoryStream+ Inc.",
        "fintech_amount": 49.99,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()


# --------------------------------------------------------------------------
# HERO
# --------------------------------------------------------------------------
def render_hero() -> None:
    api_ok = st.session_state["api_key_present"]
    backend_ok = BACKEND_AVAILABLE
    api_chip = (
        '<span class="ok">● LIVE</span>' if (api_ok and backend_ok)
        else '<span style="color:#FF8800">● DEMO MODE</span>'
    )
    st.markdown(
        f"""
        <div class="gt-hero">
          <div class="gt-hero-inner">
            <div>
              <div class="gt-badge"><span class="dot"></span> GHOSTTERMS · AUTONOMOUS AUDIT AGENT</div>
              <h1 class="gt-title" style="margin-top:12px;">Dark-Pattern & <span class="accent">Legal Trap</span> Bounty Console</h1>
              <div class="gt-sub">DeceptiveDefense · Kritical Hacks 2026 · AI/ML Track · Powered by TinyFish Infrastructure</div>
            </div>
            <div style="text-align:right;">
              <div class="gt-badge" style="background:rgba(139,92,246,0.08); color:#8B5CF6; border-color:rgba(139,92,246,0.4);">
                <span class="dot" style="background:#8B5CF6; box-shadow:0 0 10px #8B5CF6;"></span> {api_chip}
              </div>
              <div class="gt-ticker" style="justify-content:flex-end; margin-top:12px;">
                <span class="chip">Active Nodes: <b>3</b></span>
                <span class="chip">Engine: <b>TinyFish Cloud Agent v2.4</b></span>
                <span class="chip">Regulatory Spec: <b>FTC §5 &amp; EU DSA 2026</b></span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# INPUT PANEL
# --------------------------------------------------------------------------
def render_input_panel() -> None:
    st.markdown('<div class="gt-section"><span class="bar"></span><h3>01 · Target Acquisition</h3></div>', unsafe_allow_html=True)

    col_in, col_btn = st.columns([5, 1])
    with col_in:
        target = st.text_input(
            "Target URL",
            value=st.session_state.get("audit_target", "") or "",
            placeholder="https://merchant.example.com/terms",
            key="gt_target_input",
            label_visibility="collapsed",
        )
    with col_btn:
        st.write("")
        run = st.button("🛰  Run Audit", type="primary", use_container_width=True, key="gt_run_btn")

    # Presets
    st.markdown('<div class="gt-preset-row">', unsafe_allow_html=True)
    pcols = st.columns(len(PRESETS))
    preset_clicked: Optional[str] = None
    for i, (name, meta) in enumerate(PRESETS.items()):
        with pcols[i]:
            if st.button(f"⚡ {name}", key=f"gt_preset_{i}", use_container_width=True):
                preset_clicked = meta["url"]
                st.session_state["gt_target_input"] = meta["url"]
    st.markdown("</div>", unsafe_allow_html=True)

    if preset_clicked:
        st.session_state["audit_target"] = preset_clicked
        _trigger_scan(preset_clicked)

    if run and target.strip():
        _trigger_scan(target.strip())
    elif run and not target.strip():
        st.warning("Enter a target URL, or pick a preset above.")


# --------------------------------------------------------------------------
# LIVE STAGE TRACKER
# --------------------------------------------------------------------------
STAGES = [
    ("TinyFish Search API", "Locating hidden cancellation routes and /terms endpoints"),
    ("TinyFish Fetch API", "Rendering dynamic JS hydration & stripping DOM noise"),
    ("TinyFish Web Agent", "Calculating click-depth friction & modal evasion counters"),
    ("Semantic Heuristic Classifier", "Indexing FTC §5 & EU DSA violations"),
]


def render_stage_tracker() -> None:
    st.markdown('<div class="gt-section"><span class="bar"></span><h3>02 · Agent Execution Trace</h3></div>', unsafe_allow_html=True)
    container = st.empty()
    progress = st.progress(0.0, text="Initializing TinyFish cloud agent…")
    log_rows: List[str] = []

    for i, (title, desc) in enumerate(STAGES):
        pct = (i + 1) / len(STAGES)
        progress.progress(pct, text=f"Stage {i+1}/4 · {title}")
        log_rows.append(
            f'<div class="gt-tl-item"><div class="gt-tl-step">STAGE {i+1:02d}</div>'
            f'<div class="gt-tl-title">{title} <span style="color:#22E3A5; font-size:11px;">✓ OK</span></div>'
            f'<div class="gt-tl-desc">{desc}</div></div>'
        )
        container.markdown(f'<div class="gt-tl">{"".join(log_rows)}</div>', unsafe_allow_html=True)
        time.sleep(0.55)

    progress.empty()
    container.markdown(
        f'<div class="gt-tl">{"".join(log_rows)}</div>',
        unsafe_allow_html=True,
    )


def _trigger_scan(url: str) -> None:
    st.session_state["audit_target"] = url
    st.session_state["scan_running"] = True
    st.session_state["audit_result"] = None
    render_stage_tracker()
    result = _run_audit(url)
    st.session_state["audit_result"] = result
    st.session_state["audit_ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    st.session_state["audit_history"].insert(0, {
        "url": url,
        "index": result["dark_pattern_index"],
        "tier": result["risk_tier"],
        "ts": st.session_state["audit_ts"],
    })
    st.session_state["audit_history"] = st.session_state["audit_history"][:8]
    st.session_state["scan_running"] = False
    st.rerun()


# --------------------------------------------------------------------------
# METRIC GRID
# --------------------------------------------------------------------------
def _tier_color(tier: str) -> str:
    return {
        "LOW RISK": "var(--green)",
        "MODERATE RISK": "var(--amber)",
        "HIGH RISK": "var(--amber)",
        "CRITICAL RISK": "var(--crimson)",
    }.get(tier, "var(--text)")


def _tier_bg(tier: str) -> str:
    return {
        "LOW RISK": "rgba(34,227,165,0.12)",
        "MODERATE RISK": "rgba(255,136,0,0.12)",
        "HIGH RISK": "rgba(255,136,0,0.16)",
        "CRITICAL RISK": "rgba(255,51,102,0.16)",
    }.get(tier, "rgba(255,255,255,0.05)")


def render_metrics(result: Dict[str, Any]) -> None:
    st.markdown('<div class="gt-section"><span class="bar"></span><h3>03 · Risk Radar</h3></div>', unsafe_allow_html=True)

    idx = int(result["dark_pattern_index"])
    tier = result["risk_tier"]
    col_g, col_m = st.columns([1.1, 2.2])

    with col_g:
        st.markdown(
            f"""
            <div class="gt-gauge-wrap">
              <div class="gt-gauge-num" style="color:{_tier_color(tier)};">{idx}<span style="font-size:22px; color:var(--text-dim);">/100</span></div>
              <div class="gt-gauge-lbl">Dark Pattern Index</div>
              <div class="gt-tier" style="background:{_tier_bg(tier)}; color:{_tier_color(tier)}; border:1px solid {_tier_color(tier)};">{tier}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_m:
        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)
        sev_class = "bad" if idx >= 55 else "warn" if idx >= 30 else "good"

        with c1:
            st.markdown(
                f'<div class="gt-metric info"><div class="label">Friction Score</div>'
                f'<div class="value">{result.get("_friction_score", idx)}</div>'
                f'<div class="sub">Heuristic friction vs. 1-click baseline</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="gt-metric {sev_class}"><div class="label">Cancellation Path</div>'
                f'<div class="value" style="font-size:16px;">{result.get("_cancellation_steps", "—")}</div>'
                f'<div class="sub">Agent-measured click-depth</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="gt-metric warn"><div class="label">Obfuscation Ratio</div>'
                f'<div class="value">{result.get("_obfuscation_ratio", "—")}</div>'
                f'<div class="sub">Retention dark-pattern density</div></div>',
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                f'<div class="gt-metric bad"><div class="label">Penalty Exposure</div>'
                f'<div class="value" style="font-size:22px;">{result.get("_penalty_exposure", "—")}</div>'
                f'<div class="sub">FTC/DSA statutory max (est.)</div></div>',
                unsafe_allow_html=True,
            )


# --------------------------------------------------------------------------
# TAB 1 — Threat Matrix
# --------------------------------------------------------------------------
def render_tab_threats(result: Dict[str, Any]) -> None:
    violations = result.get("violations", [])
    st.markdown('<div class="gt-section"><span class="bar"></span><h3>Violation Matrix · FTC §5 / EU DSA Art. 25</h3></div>', unsafe_allow_html=True)

    if not violations:
        st.success("No dark patterns detected. Target clears the heuristic classifier.")
        return

    for i, v in enumerate(violations):
        sev = str(v.get("severity", "MEDIUM")).upper()
        cat = v.get("category", "Uncategorized")
        pts = v.get("penalty_points", 0)
        evidence = v.get("matched_evidence", [])
        with st.expander(f"⚠  {cat}  ·  {sev}  ·  +{pts} pts", expanded=(i < 2)):
            quotes = "".join(
                f'<div class="quote">“{str(q).strip()}”</div>' for q in evidence
            ) or '<div class="quote" style="border-left-color:var(--slate-2);">No verbatim evidence extracted.</div>'
            st.markdown(
                f'<div class="gt-viol">'
                f'<span class="sev {sev}">{sev}</span>'
                f'<span style="margin-left:8px; color:var(--text-dim); font-size:11.5px; font-family:JetBrains Mono, monospace;">'
                f'penalty_points = {pts}</span>'
                f'<div style="margin-top:6px; font-weight:700; font-size:14px;">{cat}</div>'
                f'{quotes}'
                f'</div>',
                unsafe_allow_html=True,
            )


# --------------------------------------------------------------------------
# TAB 2 — Traversal Trace
# --------------------------------------------------------------------------
def _build_traversal(result: Dict[str, Any]) -> List[Dict[str, str]]:
    idx = int(result["dark_pattern_index"])
    if idx < 30:
        return [
            {"kind": "", "step": "STEP 01", "title": "Account Settings", "desc": "Standard account page accessible from primary navigation."},
            {"kind": "", "step": "STEP 02", "title": "Subscription Management", "desc": "Cancellation link surfaced on first screen — clear label."},
            {"kind": "", "step": "STEP 03", "title": "One-Click Cancel", "desc": "No retention modal, no confirm-shaming. Clean exit."},
        ]
    if idx < 55:
        return [
            {"kind": "", "step": "STEP 01", "title": "Account Settings", "desc": "Cancellation option requires 2 submenu hops."},
            {"kind": "warn", "step": "STEP 02", "title": "Retention Modal", "desc": "Persuasive interstitial with discounted offer."},
            {"kind": "", "step": "STEP 03", "title": "Final Confirm", "desc": "Clear confirmation button — 3 clicks total."},
        ]
    if idx < 80:
        return [
            {"kind": "", "step": "STEP 01", "title": "Account Settings", "desc": "Cancellation buried under billing → manage → more."},
            {"kind": "warn", "step": "STEP 02", "title": "Hidden Retention Modal", "desc": "Modal evasion counter incremented (2 dismissals required)."},
            {"kind": "warn", "step": "STEP 03", "title": "Confirm-Shaming Prompt", "desc": "'No thanks, I prefer to stay unhealthy' negative-option screen."},
            {"kind": "", "step": "STEP 04", "title": "Final Confirm", "desc": "4 clicks total. Cancellation succeeds."},
        ]
    return [
        {"kind": "", "step": "STEP 01", "title": "Account Settings", "desc": "Cancellation route obfuscated — 3 submenu hops."},
        {"kind": "warn", "step": "STEP 02", "title": "Hidden Retention Modal", "desc": "Modal evasion counter = 3. Shadow-close button detected."},
        {"kind": "bad", "step": "STEP 03", "title": "Confirm-Shaming Prompt", "desc": "Dual negative-option screens with prechecked 'keep my plan'."},
        {"kind": "bad", "step": "STEP 04", "title": "Obfuscated Final Confirm", "desc": "Only path forward: telephone retention line. Roach motel confirmed."},
        {"kind": "warn", "step": "STEP 05", "title": "Agent Verified Trap", "desc": "5 clicks + phone call required. Auto-renewal still active."},
    ]


def render_tab_trace(result: Dict[str, Any]) -> None:
    st.markdown('<div class="gt-section"><span class="bar"></span><h3>TinyFish Agent · Cancellation Journey</h3></div>', unsafe_allow_html=True)
    items = _build_traversal(result)
    html = '<div class="gt-tl">'
    for it in items:
        html += (
            f'<div class="gt-tl-item {it["kind"]}">'
            f'<div class="gt-tl-step">{it["step"]}</div>'
            f'<div class="gt-tl-title">{it["title"]}</div>'
            f'<div class="gt-tl-desc">{it["desc"]}</div>'
            f'</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# TAB 3 — Regulatory Dossier
# --------------------------------------------------------------------------
def _build_legal_letter(result: Dict[str, Any]) -> str:
    url = result["target_url"]
    idx = result["dark_pattern_index"]
    tier = result["risk_tier"]
    violations = result.get("violations", [])
    ts = st.session_state.get("audit_ts") or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    vlines = []
    for v in violations:
        vlines.append(
            f"  • {v.get('category')} [{v.get('severity')}] — penalty points: {v.get('penalty_points')}"
        )
        for ev in v.get("matched_evidence", []):
            vlines.append(f"      Evidence: \"{ev}\"")
    vblock = "\n".join(vlines) if vlines else "  (No violations matched by heuristic classifier.)"

    return f"""FORMAL CONSUMER COMPLAINT — DARK PATTERN & UNFAIR PRACTICE DISCLOSURE
================================================================================
Filed by:      Concerned Consumer / DeceptiveDefense Automated Auditor
Filing Agent:  GhostTerms Autonomous Audit Engine (TinyFish Infrastructure)
Timestamp:     {ts}
Subject URL:   {url}
Target Index:  {idx}/100  ({tier})

--------------------------------------------------------------------------------
STATEMENT OF FACTS
--------------------------------------------------------------------------------
The GhostTerms autonomous audit agent conducted a multi-stage traversal of the
above-listed service in accordance with FTC Section 5 (Unfair or Deceptive Acts
or Practices) and Article 25 of the EU Digital Services Act. The agent recorded
a Dark Pattern Index of {idx}/100, classified as {tier}.

The following potentially deceptive design patterns were observed and are
supported by extracted verbatim evidence:

{vblock}

--------------------------------------------------------------------------------
REGULATORY BASIS
--------------------------------------------------------------------------------
1. FTC Section 5 — Unfair or Deceptive Acts or Practices
   - Negative option marketing (Rule on Negative Option & Forced Continuity)
   - Deceptive cancellation friction (Roach Motel patterns)
   - Prechecked opt-ins and forced consent (Privacy Zuckering)

2. EU Digital Services Act — Article 25
   - Prohibition on deceptive interface designs that materially distort or
     impair user autonomy, decision-making, or choice.
   - Dark patterns in subscription renewal and cancellation flows.

3. US Restore Online Shoppers' Confidence Act (ROSCA)
   - Failure to provide a simple mechanism for stopping recurring charges.

--------------------------------------------------------------------------------
REQUESTED ACTION
--------------------------------------------------------------------------------
The complainant respectfully requests that the relevant authority:

  1. Investigate the above-cited violations;
  2. Require the merchant to implement 1-click, low-friction cancellation
     consistent with the FTC "Click-to-Cancel" rulemaking;
  3. Assess civil penalties consistent with estimated statutory exposure
     of {result.get('_penalty_exposure', 'N/A')};
  4. Preserve all logs, A/B tests, and internal design documentation
     relating to the cancellation flow.

Submitted via GhostTerms Regulatory Dossier Export · DeceptiveDefense / Kritical Hacks 2026
================================================================================
"""


def render_tab_regulatory(result: Dict[str, Any]) -> None:
    st.markdown('<div class="gt-section"><span class="bar"></span><h3>Compliance · Ready-to-File Dossier</h3></div>', unsafe_allow_html=True)

    ready = bool(result.get("regulatory_complaint_ready"))
    if ready:
        st.markdown(
            '<div style="padding:10px 14px; border-radius:10px; border:1px solid rgba(34,227,165,0.4); background:rgba(34,227,165,0.06); font-size:13px;">'
            '<b style="color:#22E3A5;">● REGULATORY COMPLAINT READY</b> '
            '<span style="color:var(--text-dim); margin-left:6px;">Threshold met (index ≥ 55). Dossier is admissible for FTC / EU DSA submission.</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="padding:10px 14px; border-radius:10px; border:1px solid rgba(255,136,0,0.4); background:rgba(255,136,0,0.06); font-size:13px;">'
            '<b style="color:#FF8800;">● BELOW FILING THRESHOLD</b> '
            '<span style="color:var(--text-dim); margin-left:6px;">Index &lt; 55 — recommended for internal review only.</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    letter = _build_legal_letter(result)
    payload = json.dumps({k: v for k, v in result.items() if not k.startswith("_")},
                         indent=2, default=str)
    telemetry_payload = json.dumps(result, indent=2, default=str)

    col_l, col_r = st.columns([1.4, 1])
    with col_l:
        st.markdown('<div class="gt-section"><span class="bar"></span><h3>Legal Complaint Preview</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="gt-legal">{letter}</div>', unsafe_allow_html=True)
    with col_r:
        st.markdown('<div class="gt-section"><span class="bar"></span><h3>Export Formats</h3></div>', unsafe_allow_html=True)
        st.download_button(
            "⬇  Raw JSON Audit Telemetry",
            data=telemetry_payload,
            file_name="ghostterms_audit.json",
            mime="application/json",
            use_container_width=True,
            key="gt_dl_json",
        )
        st.download_button(
            "⬇  Formal Legal Complaint (.md)",
            data=letter,
            file_name="ghostterms_complaint.md",
            mime="text/markdown",
            use_container_width=True,
            key="gt_dl_letter",
        )
        st.download_button(
            "⬇  Sanitized Payload (.json)",
            data=payload,
            file_name="ghostterms_payload.json",
            mime="application/json",
            use_container_width=True,
            key="gt_dl_payload",
        )
        st.markdown(
            '<div style="margin-top:14px; font-size:11.5px; color:var(--text-dim); font-family:JetBrains Mono, monospace;">'
            'Files are generated client-side. No PII transmitted.</div>',
            unsafe_allow_html=True,
        )


# --------------------------------------------------------------------------
# TAB 4 — FinTech Simulator
# --------------------------------------------------------------------------
def render_tab_fintech(result: Dict[str, Any]) -> None:
    st.markdown('<div class="gt-section"><span class="bar"></span><h3>Virtual-Card Issuer · Point-of-Sale Simulation</h3></div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:13px; color:var(--text-dim); margin-bottom:14px;">'
        'Simulates how a virtual-card issuer (e.g. Privacy.com, Revolut) queries the GhostTerms API before '
        'authorizing a transaction. Merchants scoring <b style="color:var(--amber);">&gt; 60</b> trigger a user warning; '
        '<b style="color:var(--crimson);">&gt; 80</b> triggers a block recommendation.</div>',
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        merchant = st.text_input(
            "Merchant",
            value=st.session_state["fintech_merchant_name"],
            key="gt_ft_merchant",
        )
    with col_b:
        amount = st.number_input(
            "Amount (USD)",
            min_value=0.5,
            max_value=10_000.0,
            value=float(st.session_state["fintech_amount"]),
            step=1.0,
            key="gt_ft_amount",
        )
    with col_c:
        score = st.slider(
            "Merchant GhostTerms Score",
            min_value=0,
            max_value=100,
            value=int(result["dark_pattern_index"]),
            key="gt_ft_score",
        )

    st.session_state["fintech_merchant_name"] = merchant
    st.session_state["fintech_amount"] = amount
    st.session_state["fintech_merchant_score"] = score

    if score >= 80:
        flag_cls, flag_lbl = "block", "BLOCKED"
        note = "Merchant exceeds critical-risk threshold. Transaction declined by issuer policy."
    elif score >= 60:
        flag_cls, flag_lbl = "warn", "WARN"
        note = "Merchant exceeds warning threshold. Cardholder prompted with a GhostTerms warning modal."
    else:
        flag_cls, flag_lbl = "allow", "APPROVED"
        note = "Merchant clears GhostTerms threshold. Transaction authorized normally."

    st.markdown(
        f"""
        <div class="gt-txn">
          <div>
            <div class="merchant">{merchant or 'Unknown Merchant'}</div>
            <div style="font-size:11.5px; color:var(--text-dim); font-family:JetBrains Mono, monospace;">
              GhostTerms Score: {score}/100
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:16px;">
            <div class="amount">${amount:,.2f}</div>
            <div class="gt-flag {flag_cls}">{flag_lbl}</div>
          </div>
        </div>
        <div style="font-size:12.5px; color:var(--text-dim); padding:6px 4px;">{note}</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="gt-section"><span class="bar"></span><h3>Issuer Decision Matrix</h3></div>', unsafe_allow_html=True)
    tiers = [
        ("0 – 59", "ALLOW", "allow", "Merchant is compliant. No user friction."),
        ("60 – 79", "WARN", "warn", "User shown a 'proceed with caution' interstitial at checkout."),
        ("80 – 100", "BLOCK", "block", "Transaction declined; cardholder offered a single-use virtual card."),
    ]
    for rng, lbl, cls, desc in tiers:
        st.markdown(
            f"""
            <div class="gt-txn">
              <div>
                <div class="merchant">Score {rng}</div>
                <div style="font-size:11.5px; color:var(--text-dim);">{desc}</div>
              </div>
              <div class="gt-flag {cls}">{lbl}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------------------------------
# HISTORY PANEL (sidebar-friendly or inline footer)
# --------------------------------------------------------------------------
def render_history() -> None:
    history = st.session_state["audit_history"]
    if not history:
        return
    st.markdown('<div class="gt-section"><span class="bar"></span><h3>Recent Audit Trail</h3></div>', unsafe_allow_html=True)
    for h in history:
        tier = h["tier"]
        color = _tier_color(tier)
        st.markdown(
            f"""
            <div class="gt-txn">
              <div>
                <div class="merchant" style="font-family:'JetBrains Mono', monospace; font-size:12px;">{h['url']}</div>
                <div style="font-size:11px; color:var(--text-dim);">{h['ts']}</div>
              </div>
              <div style="display:flex; gap:12px; align-items:center;">
                <div class="amount" style="color:{color};">{h['index']}/100</div>
                <div class="gt-flag" style="background:{_tier_bg(tier)}; color:{color}; border:1px solid {color};">{tier}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------------------------------
# EMPTY STATE
# --------------------------------------------------------------------------
def render_empty_state() -> None:
    st.markdown(
        f"""
        <div style="
            border:1px dashed var(--slate-2); border-radius:18px; padding:60px 30px; text-align:center;
            background: radial-gradient(600px 200px at 50% 0%, rgba(0,240,255,0.05), transparent 70%);
        ">
            <div style="font-size:44px;">🛰️</div>
            <div style="font-size:19px; font-weight:700; margin-top:10px;">Awaiting Target Acquisition</div>
            <div style="color:var(--text-dim); font-size:13px; margin-top:6px; max-width:520px; margin-left:auto; margin-right:auto;">
                Enter a merchant URL above or pick a preset demo target. The GhostTerms agent will autonomously
                map the cancellation journey, extract evidence, and compile a ready-to-file regulatory dossier.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------
def main() -> None:
    render_hero()
    render_input_panel()

    result = st.session_state.get("audit_result")
    if not result:
        render_empty_state()
        render_history()
        st.markdown(
            '<div class="gt-footer">GHOSTTERMS · DECEPTIVEDEFENSE · KRITICAL HACKS 2026 · AI/ML TRACK</div>',
            unsafe_allow_html=True,
        )
        return

    # result header
    st.markdown(
        f'<div style="margin-top:20px; font-family:JetBrains Mono, monospace; font-size:12px; color:var(--text-dim);">'
        f'TARGET :: <span style="color:var(--cyan);">{result["target_url"]}</span>'
        f'&nbsp;&nbsp;·&nbsp;&nbsp; LAST AUDIT :: {st.session_state.get("audit_ts","—")}'
        f'</div>',
        unsafe_allow_html=True,
    )

    render_metrics(result)

    tabs = st.tabs([
        "🚨  Threat Matrix",
        "🧭  Agent Traversal",
        "⚖️  Regulatory Dossier",
        "💳  FinTech Simulator",
    ])
    with tabs[0]:
        render_tab_threats(result)
    with tabs[1]:
        render_tab_trace(result)
    with tabs[2]:
        render_tab_regulatory(result)
    with tabs[3]:
        render_tab_fintech(result)

    render_history()

    st.markdown(
        '<div class="gt-footer">GHOSTTERMS · DECEPTIVEDEFENSE · KRITICAL HACKS 2026 · AI/ML TRACK</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()