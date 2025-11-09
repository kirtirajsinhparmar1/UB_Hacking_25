# The Inspiration

Adverse media screening is a slow, manual compliance task. Analysts spend 2–4 hours per entity reading hundreds of articles—costly and error-prone at scale. I built RiskRadar AI to automate this end-to-end, cutting screening time from hours to minutes while preserving bank-grade accuracy.

---

# What I Learned

* Prompt calibration matters. Early prompts biased toward negative news and inflated scores by 30–40 points; stricter rubrics and conservative phrasing fixed this.
* Structured outputs (Instructor + Pydantic) removed brittle JSON parsing and crashes.
* UI quality affects trust; CSS, Plotly, and clean layout improved perceived reliability.
* OpenRouter’s multi-model setup kept costs low (~$2 for the hackathon) and avoided lock-in.
* Human oversight is essential; Fortune 500 “background noise” needs dampening and reality checks.

---

# How I Built It 

* **News aggregation** — `src/utils/news_fetcher.py`
  Google News RSS (free), caching, balanced retrieval (positive/neutral/negative), 10–100 articles per screening.
* **AI screening** — `src/models/screener.py`
  OpenRouter to GPT/Claude/Gemini; Instructor + Pydantic schemas; 7 risk categories; sentence-level evidence with importance; clear rationales.
* **Dashboard** — `app.py`
  Streamlit, custom CSS, Plotly visuals; tabs (Analysis / Articles / Trends / Export); CSV/JSON export.

---

# Calibration & Guardrails 

1. Removed negative-only filters → pull full-spectrum news.
2. Strict scoring rubric → routine lawsuits score 10–20, not 70+.
3. Enterprise dampening → −25% for mega-caps unless evidence is exceptional (≥95).
4. Lower temperature → 0.2 for consistency.
   *Result: Bank of America ~35–45/100; Tesla ~25–35/100.*

---

# Development Process 

Prototype → test → surface calibration issues → rewrite prompts/rubrics → add caching & exports → refine UI/UX → finalize analytics and evidence views.

---

# Key Challenges

* Model availability/name churn on free tiers → standardized on `gpt-3.5-turbo`.
* Production-ready UI took real design work (layout, typography, charts).
* Time pressure forced prioritization of core value first.

---

# Why It’s Special

* Real business value and immediate ROI on a high-cost manual process.
* Explainable by design: each score cites sentence-level evidence suitable for audits.
* Low operating cost: free RSS + inexpensive LLM calls.
* Deployable polish: stable code, caching, exports, professional dashboard.
* Buffalo Proud: showcases UB talent building credible, production-ready fintech.

---

# What’s Next for RiskRadar AI

* **Expand data sources:** Add NewsAPI, Finnhub, SEC filings, court documents, non-English and historical coverage.
* **Improve accuracy:** Ensemble GPT-4/Claude/Gemini; fine-tune on real screening data to match compliance priorities.
* **Integrations:** REST API for M&T’s LOS, webhooks for Valmar’s Totality LMS, Odoo plugin for partner screening.
* **Continuous monitoring:** Automatic re-screening every 24 hours with spike alerts.
* **Performance:** Parallelize processing, smarter caching, batch LLM calls; support overnight batch screenings.
* **Audit features:** PDF reports with citations, history logs, configurable thresholds, RBAC.
* **User testing:** Put in front of compliance officers; iterate on workflow needs.

---

*Bottom line: RiskRadar AI turns a manual compliance burden into fast, explainable, cost-effective automation—without sacrificing accuracy.*
