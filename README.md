# The Inspiration

We wanted to build something that would genuinely solve a real banking problem. After researching regulatory compliance challenges, we discovered that adverse media screening-the process of monitoring negative news about customers and counterparties-is one of the most time-consuming manual tasks in banking compliance.

Banks are legally required to screen entities for financial crimes, sanctions violations, and other risks under FinCEN and FATF regulations. Currently, compliance analysts spend 2-4 hours manually Googling company names and reading hundreds of articles per screening. For large banks screening thousands of entities monthly, this costs millions of dollars annually and creates regulatory risk when analysts miss critical signals.

We realized AI could automate this, reducing screening time from hours to minutes while maintaining bank-grade accuracy. That's when RiskRadar AI came to fruition.

# What We Learned

* OpenRouter’s multi-model setup kept costs low (~$2 for the hackathon) and avoided lock-in.
* Prompt calibration matters. Early prompts biased toward negative news and inflated scores by 30–40 points; stricter rubrics and conservative phrasing fixed this.
* Structured outputs (Instructor + Pydantic) removed brittle JSON parsing and crashes.
* UI quality affects trust; CSS, Plotly, and clean layout improved perceived reliability.
* Fortune 500 “background noise” needs dampening and reality checks.

---

# How We Built It 

* **News aggregation** - 
  Google News RSS (free), caching, balanced retrieval (positive/neutral/negative), 10–100 articles per screening.
* **AI screening** - 
  OpenRouter to GPT/Claude/Gemini; Instructor + Pydantic schemas; 7 risk categories; sentence-level evidence with importance; clear rationales.
* **Dashboard** -
  Streamlit, custom CSS, Plotly visuals; tabs (Analysis / Articles / Trends / Export); CSV/JSON export.

---

# Calibration & Guardrails 

1. Removed negative-only filters → pull full-spectrum news.
2. Strict scoring rubric → routine lawsuits score 10–20, not 70+.
3. Enterprise dampening → −25% for mega-caps unless evidence is exceptional (≥95).
4. Lower temperature → 0.2 for consistency.

---
# Development Process 
Prototype → test → surface calibration issues → rewrite prompts/rubrics → add caching & exports → refine UI/UX → finalize analytics

---

# Key Challenges
* Model availability/name churn on free tiers → standardized on `gpt-3.5-turbo`.
* Production-ready UI took real design work (layout, typography, charts).
* Time pressure forced prioritization of core value first.

---

# Why It’s Special
* Buffalo Proud: showcases UB talent building credible, production-ready fintech.
* Real business value and immediate ROI on a high-cost manual process.
* Explainable by design: each score cites sentence-level evidence suitable for audits.
* Low operating cost: free RSS + inexpensive LLM calls.
* Deployable polish: stable code, caching, exports, professional dashboard.

---

# What’s Next for RiskRadar AI
* **Expand data sources:** Add NewsAPI, Finnhub, SEC filings, court documents, non-English and historical coverage.
* **Improve accuracy:** Ensemble GPT-4/Claude/Gemini; fine-tune on real screening data to match compliance priorities.
* **Integrations:** REST API for M&T’s LOS, webhooks for Valmar’s Totality LMS, Odoo plugin for partner screening.
* **Continuous monitoring:** Automatic re-screening every 24 hours with spike alerts.
* **Performance:** Parallelize processing, smarter caching, batch LLM calls; support overnight batch screenings.
* **Audit features:** PDF reports with citations, history logs, configurable thresholds, RBAC.
* **User testing:** Put in front of compliance officers; iterate on workflow needs.
