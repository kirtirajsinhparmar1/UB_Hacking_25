"""sentinel-ai.app
Sentinel AI - Enterprise Adverse Media Screening Platform

This Streamlit application provides an AI-powered adverse media
screening interface used during Buffalo Hackathon 2025. The file
contains UI layout, interactions, and wiring to the screening
business-logic located in ``src/models`` and ``src/utils``.

Refactor notes:
- Compact design tokens and simplified CSS for accessibility and clarity.
- Replaced deprecated use_container_width with width="stretch".
- Kept all business logic, keys, and exports unchanged.
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Ensure src is importable
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from utils.news_fetcher import NewsFetcher
from models.screener import AdverseMediaScreener


# -----------------------
# Design tokens & compact CSS
# -----------------------
TOKENS_CSS = """
<style>
:root{
  --color-bg: #0B0C0E;
  --color-surface: #FFFFFF;
  --color-primary: #1F6FEB;
  --color-success: #16A34A;
  --color-warning: #D97706;
  --color-danger: #DC2626;
  --text-strong: #0F172A;
  --text-muted: #6B7280;
  --radius: 12px;
  --shadow: 0 6px 24px rgba(2,6,23,0.08);
  --space-4: 4px;
  --space-8: 8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-24: 24px;
  --space-32: 32px;
  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* Reset & layout */
body { font-family: var(--font-stack); color: var(--text-strong); background: #f7f9fc; }

/* Header */
.header-bar {
  background: var(--color-surface);
  border-bottom: 1px solid #e6edf8;
  padding: var(--space-16) var(--space-24);
  display: flex;
  align-items: center;
  gap: var(--space-16);
  box-shadow: var(--shadow);
  border-radius: 0 0 var(--radius) var(--radius);
}
.header-title { font-size: 22px; font-weight: 700; margin: 0; }
.header-tagline { color: var(--text-muted); font-size: 14px; margin: 0; }

/* Card */
.card {
  background: var(--color-surface);
  padding: var(--space-16);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin-bottom: var(--space-16);
}

/* Input hero */
.input-hero { max-width: 980px; margin: var(--space-24) auto; }

/* Metric cards */
.metric-row { display:flex; gap: var(--space-16); }
.metric-card { flex:1; padding: var(--space-16); border-radius: var(--radius); background: var(--color-surface); box-shadow: var(--shadow); }
.metric-label { color: var(--text-muted); font-size: 13px; margin-bottom: 6px; }
.metric-value { font-size: 22px; font-weight: 700; color: var(--text-strong); }

/* Severity badges */
.badge { padding: 6px 12px; border-radius: 999px; color: white; font-weight: 700; font-size: 12px; display: inline-block; }
.badge-low { background: var(--color-success); }
.badge-medium { background: var(--color-warning); }
.badge-high { background: #c2410c; }
.badge-critical { background: var(--color-danger); }

/* Results container */
.results-container { max-width: 1200px; margin: var(--space-16) auto; }

/* Risk progress bar */
.risk-progress { background: #eef2ff; border-radius: 8px; height: 12px; overflow: hidden; margin-top: 6px; }
.risk-fill { height: 100%; text-align:right; padding-right:8px; color: white; font-size: 12px; line-height:12px; }

.small-muted { color: var(--text-muted); font-size: 13px; }
.footer { text-align:center; color: var(--text-muted); padding: var(--space-16); font-size:13px; }
</style>
"""

st.set_page_config(page_title="Sentinel AI", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

st.markdown(TOKENS_CSS, unsafe_allow_html=True)


# -----------------------
# Helpers
# -----------------------
def _safe_entity_fragment(name: str) -> str:
    if not isinstance(name, str):
        name = str(name or "unknown")
    return name.strip().replace(" ", "_")


def _export_filename(entity_name: str, ext: str = "json") -> str:
    fragment = _safe_entity_fragment(entity_name)
    return f"sentinel_{fragment}_{datetime.now().strftime('%Y%m%d')}.{ext}"


# -----------------------
# Session state defaults
# -----------------------
if "screening_result" not in st.session_state:
    st.session_state.screening_result = None
if "screening_history" not in st.session_state:
    st.session_state.screening_history = []


# -----------------------
# Header
# -----------------------
st.markdown(
    """
    <div class="header-bar card" role="banner">
        <div style="display:flex; flex-direction:column;">
            <div class="header-title">Sentinel AI</div>
            <div class="header-tagline">Adverse media screening for compliance teams — clear, fast, and credible.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------
# Main: input when no result
# -----------------------
if not st.session_state.screening_result:
    # If an example was selected on previous run, use it as initial value for the input.
    initial_entity = ""
    if st.session_state.get("example_entity"):
        initial_entity = st.session_state.pop("example_entity", "")

    st.markdown('<div class="input-hero">', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Screen an entity", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Enter the legal entity / company name to screen adverse media.</div>", unsafe_allow_html=True)

    cols = st.columns([3, 1])
    with cols[0]:
        # Pass an initial value safely — Streamlit will use session state if present.
        entity_name_widget = st.text_input(
            "Entity Name",
            value=initial_entity,
            placeholder="e.g., Tesla, JP Morgan, Wells Fargo",
            label_visibility="collapsed",
            key="entity_input",
        )

    with cols[1]:
        scan_clicked = st.button("🚀 Scan Now", type="primary", width="stretch")

    # Advanced options in an expander (minimal styling)
    with st.expander("⚙️ Advanced options", expanded=False):
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        with adv_col1:
            days_back = st.select_slider(
                "Time range",
                options=[7, 30, 60, 90, 180, 365],
                value=90,
                format_func=lambda x: f"{x} days",
                key="days_back",
            )
        with adv_col2:
            max_articles = st.select_slider(
                "Max articles",
                options=[10, 25, 50, 75, 100],
                value=50,
                key="max_articles",
            )
        with adv_col3:
            model_choice = st.selectbox(
                "AI model",
                options=[
                    "openai/gpt-3.5-turbo",
                    "openai/gpt-4o",
                    "anthropic/claude-3-haiku",
                    "anthropic/claude-3.5-sonnet",
                ],
                index=0,
                key="model_choice",
            )

    st.markdown("---")

    # Quick Start examples (writes a one-time session key and reruns)
    st.markdown("#### 💡 Quick start")
    example_cols = st.columns(5)
    examples = ["Tesla", "JP Morgan", "Wells Fargo", "Binance", "Bank of America"]
    for col, example in zip(example_cols, examples):
        with col:
            if st.button(example, key=f"example_{example}", width="stretch"):
                st.session_state["example_entity"] = example
                st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)  # close card
    st.markdown("</div>", unsafe_allow_html=True)  # close input-hero

    # Process scan: use the widget-backed session value to read the entity
    if scan_clicked and st.session_state.get("entity_input"):
        entity_name = st.session_state.get("entity_input")
        # Simple progress & discrete status updates
        progress = st.progress(0)
        status = st.empty()
        try:
            status.info("Fetching recent articles...")
            progress.progress(20)

            fetcher = NewsFetcher()
            articles = fetcher.fetch_all_news(entity_name, days_back, max_articles)

            if not articles:
                status.error(f"No articles found for '{entity_name}'. Try wider time range or spelling.")
                progress.empty()
                st.stop()

            status.info(f"Analyzing {len(articles)} articles...")
            progress.progress(50)
            time.sleep(0.25)

            screener = AdverseMediaScreener(model=model_choice)
            result = screener.screen_entity(articles, entity_name)

            # Store result and history (unchanged business logic)
            st.session_state.screening_result = result
            st.session_state.screening_history.append(
                {
                    "entity": entity_name,
                    "timestamp": datetime.now().isoformat(),
                    "severity": result.get("overall_severity"),
                }
            )

            progress.progress(100)
            status.success("Analysis complete")
            time.sleep(0.25)
            progress.empty()
            status.empty()
            st.experimental_rerun()

        except Exception as exc:
            status.error(f"Error: {exc}")
            progress.empty()
            st.stop()


# -----------------------
# Results view
# -----------------------
if st.session_state.screening_result:
    result = st.session_state.screening_result

    st.markdown('<div class="results-container">', unsafe_allow_html=True)

    # Top header + new scan button
    header_col, action_col = st.columns([4, 1])
    with header_col:
        st.markdown(f"## 📊 Risk report — {result['entity_name']}")
        st.markdown(f"<div class='small-muted'>Analyzed {result.get('articles_analyzed', 0)} articles • {result.get('screening_date', '')[:19]}</div>", unsafe_allow_html=True)
    with action_col:
        if st.button("← New scan", width="stretch"):
            st.session_state.screening_result = None
            st.experimental_rerun()

    st.markdown("---")

    # Severity badge logic (visual only)
    severity = result.get("overall_severity", 0)
    if severity > 75:
        badge_class = "badge-critical"
        severity_label = "CRITICAL"
    elif severity > 50:
        badge_class = "badge-high"
        severity_label = "HIGH"
    elif severity > 25:
        badge_class = "badge-medium"
        severity_label = "MEDIUM"
    else:
        badge_class = "badge-low"
        severity_label = "LOW"

    # Executive summary metrics
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Overall severity</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{severity}/100</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-top:8px;"><span class="badge {badge_class}">{severity_label}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[1]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        articles_count = result.get("articles_analyzed", 0)
        st.markdown('<div class="metric-label">Articles screened</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{articles_count}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[2]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        high_count = len(result.get("high_risk_articles", []))
        st.markdown('<div class="metric-label">High-risk alerts</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{high_count}</div>', unsafe_allow_html=True)
        if articles_count:
            pct = (high_count / articles_count) * 100
            st.markdown(f'<div class="small-muted">{pct:.1f}% flagged</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[3]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        primary = result.get("primary_risk", "N/A").replace("_", " ").title()
        st.markdown('<div class="metric-label">Primary risk</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{primary}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close card

    # Tabs: Breakdown / Alerts / Analytics / Export
    tab_breakdown, tab_alerts, tab_analytics, tab_export = st.tabs(
        ["Risk breakdown", "Alerts", "Analytics", "Export"]
    )

    # --- Risk breakdown ---
    with tab_breakdown:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        risk_scores = result.get("risk_scores", {})
        df_risks = pd.DataFrame(
            {
                "Category": [k.replace("_", " ").title() for k in risk_scores.keys()],
                "Score": list(risk_scores.values()),
            }
        ).sort_values("Score", ascending=True)

        # Bar chart: simple theme
        fig = px.bar(
            df_risks,
            y="Category",
            x="Score",
            orientation="h",
            text="Score",
            color="Score",
            color_continuous_scale=[ "#16A34A", "#D97706", "#DC2626"],
        )
        fig.update_layout(title_text="Risk category scores", xaxis_title="Score (0-100)", yaxis_title="", height=420, template="plotly_white")
        fig.update_traces(texttemplate="%{text}", textposition="outside")
        st.plotly_chart(fig, width="stretch")

        # Right-side compact list of risk bars
        st.markdown("<hr/>", unsafe_allow_html=True)
        for cat, score in sorted(risk_scores.items(), key=lambda x: x[1], reverse=True):
            color = "#16A34A"
            if score > 60:
                color = "#DC2626"
            elif score > 30:
                color = "#D97706"
            st.markdown(f"**{cat.replace('_',' ').title()}** — {score}/100")
            st.markdown(
                f'<div class="risk-progress"><div class="risk-fill" style="width:{score}%; background:{color};"></div></div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Alerts ---
    with tab_alerts:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        high_articles = result.get("high_risk_articles", [])
        if high_articles:
            st.markdown(f"### ⚠️ {len(high_articles)} high-risk articles", unsafe_allow_html=True)
            for art in sorted(high_articles, key=lambda x: x.get("overall_severity", 0), reverse=True)[:15]:
                sev = art.get("overall_severity", 0)
                icon = "🔴" if sev > 75 else ("🟠" if sev > 60 else "🟡")
                title = art.get("article_title", "Untitled")
                with st.expander(f"{icon} [{sev}/100] {title[:120]}"):
                    st.markdown(f"**Source:** {art.get('source', 'Unknown')} — **Date:** {art.get('publish_date', '')[:10]}")
                    st.markdown(f"**Primary risk:** {art.get('primary_risk', 'N/A').replace('_',' ').title()}")
                    st.markdown("**Key evidence:**")
                    for sent in art.get("key_sentences", [])[:3]:
                        if isinstance(sent, dict):
                            st.markdown(f"- {sent.get('sentence','')}")
                    st.info(art.get("explanation", "No explanation provided"))
                    if art.get("article_url"):
                        st.markdown(f"[Open full article]({art.get('article_url')})")
        else:
            st.success("No high-risk articles detected")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Analytics ---
    with tab_analytics:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # Pie / distribution
        labels = [k.replace("_", " ").title() for k in risk_scores.keys()]
        values = list(risk_scores.values())
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
        fig_pie.update_layout(title_text="Risk distribution", height=380)
        st.plotly_chart(fig_pie, width="stretch")

        # Severity histogram
        all_sev = [a.get("overall_severity", 0) for a in result.get("all_assessments", [])]
        fig_hist = go.Figure(data=[go.Histogram(x=all_sev, nbinsx=20, marker_color="#1F6FEB")])
        fig_hist.update_layout(title_text="Severity distribution", xaxis_title="Severity score", yaxis_title="Article count", height=380)
        st.plotly_chart(fig_hist, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Export ---
    with tab_export:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            json_data = json.dumps(result, indent=2)
            st.download_button(
                "Download JSON",
                data=json_data,
                file_name=_export_filename(result.get("entity_name", "entity"), ext="json"),
                mime="application/json",
                key="download_json",
                width="stretch",
            )
        with col2:
            summary_df = pd.DataFrame(
                [
                    {
                        "Entity": result.get("entity_name"),
                        "Date": result.get("screening_date", "")[:10],
                        "Severity": result.get("overall_severity"),
                        "Primary_Risk": result.get("primary_risk"),
                        **result.get("risk_scores", {}),
                    }
                ]
            )
            st.download_button(
                "Download CSV",
                data=summary_df.to_csv(index=False),
                file_name=_export_filename(result.get("entity_name", "entity"), ext="csv"),
                mime="text/csv",
                key="download_csv",
                width="stretch",
            )
        with col3:
            st.markdown("<div class='small-muted'>Export the screening result for downstream reporting. Filenames use a consistent format.</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close results-container


# -----------------------
# Footer
# -----------------------
st.markdown("<div class='footer'>Sentinel AI — Adverse media screening • Prototype</div>", unsafe_allow_html=True)

# End of file
