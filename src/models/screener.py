"""
AI-powered adverse media screening using OpenRouter
RECALIBRATED VERSION - Conservative scoring to avoid false positives
"""
import os
from typing import Dict, List
from pydantic import BaseModel, Field
from openai import OpenAI
import instructor
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class SentenceEvidence(BaseModel):
    sentence: str
    importance_score: float = Field(ge=0, le=1)

class RiskAssessment(BaseModel):
    fraud: int = Field(ge=0, le=100)
    sanctions: int = Field(ge=0, le=100)
    money_laundering: int = Field(ge=0, le=100)
    bribery_corruption: int = Field(ge=0, le=100)
    cyber_incident: int = Field(ge=0, le=100)
    insolvency: int = Field(ge=0, le=100)
    esg_violation: int = Field(ge=0, le=100)
    primary_risk: str
    overall_severity: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    key_sentences: List[SentenceEvidence] = Field(max_length=3)
    explanation: str = Field(max_length=800)

class AdverseMediaScreener:
    """AI-powered adverse media screening with conservative calibration"""
    
    def __init__(self, model: str = None):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        self.model = model or os.getenv("DEFAULT_MODEL", "openai/gpt-3.5-turbo")
        
        self.client = instructor.from_openai(
            OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                default_headers={
                    "HTTP-Referer": os.getenv("APP_URL", "http://localhost:8501"),
                    "X-Title": os.getenv("APP_NAME", "Sentinel AI")
                }
            )
        )
    
    def screen_article(self, article_text: str, entity_name: str) -> RiskAssessment:
        """Screen article with CONSERVATIVE, RECALIBRATED scoring"""
        
        prompt = f"""You are a senior banking compliance analyst with 20 years experience. You are HIGHLY SKEPTICAL and require STRONG EVIDENCE before flagging high risks.

ENTITY: {entity_name}

ARTICLE:
{article_text}

TASK: Analyze for 7 risk categories with CONSERVATIVE scoring.

=== CRITICAL SCORING GUIDELINES ===

Most news is ROUTINE and should score 0-30. Be VERY conservative.

**FRAUD & FINANCIAL CRIME:**
- 0-20: Routine lawsuits, customer complaints, minor disputes (MOST CASES)
- 21-40: Class actions filed but not settled, investigations opened but no findings
- 41-60: Regulatory warnings issued, fines <$10M, settlements admitted
- 61-80: Criminal charges filed, fines $10M-$100M, proven accounting fraud
- 81-100: Criminal convictions, fines >$100M, systemic fraud proven

**SANCTIONS & TRADE VIOLATIONS:**
- 0-20: No sanctions issues mentioned (DEFAULT)
- 21-40: Mentioned in context of compliance programs, no violations
- 41-60: OFAC reviewing transactions, warnings issued
- 61-80: OFAC fines issued $1M-$10M, export violations proven
- 81-100: Criminal sanctions violations, fines >$10M, ongoing prosecution

**MONEY LAUNDERING (AML):**
- 0-20: Routine AML compliance mentioned, no issues (MOST CASES)
- 21-40: Enhanced monitoring required, consent orders without fines
- 41-60: FinCEN warnings, fines <$5M, AML program deficiencies
- 61-80: FinCEN fines $5M-$50M, systemic AML failures
- 81-100: Criminal AML charges, fines >$50M, BSA Act violations proven

**BRIBERY & CORRUPTION:**
- 0-20: No bribery/corruption mentioned (DEFAULT)
- 21-40: Investigations opened, no findings yet
- 41-60: FCPA settlements <$10M, minor corruption allegations
- 61-80: FCPA fines $10M-$100M, bribery proven
- 81-100: Criminal convictions, fines >$100M, systemic corruption

**CYBER INCIDENTS:**
- 0-20: No breaches mentioned OR breaches affecting <10K records (ROUTINE)
- 21-40: Breaches 10K-100K records, minor system outages
- 41-60: Breaches 100K-1M records, ransomware incidents contained
- 61-80: Breaches >1M records, major ransomware payment, regulatory fines
- 81-100: Breaches >10M records, critical infrastructure failure, ongoing attacks

**INSOLVENCY & CREDIT EVENTS:**
- 0-20: Strong financial position, no solvency concerns (HEALTHY COMPANIES)
- 21-40: Stock volatility, analyst concerns, but fundamentals solid
- 41-60: Credit rating downgrade (but still investment grade), liquidity concerns
- 61-80: Downgrade to junk status, covenant violations, restructuring needed
- 81-100: Bankruptcy filing, debt default, going concern warnings

**ESG VIOLATIONS:**
- 0-20: Minor complaints, routine ESG disclosures (MOST COMPANIES)
- 21-40: ESG controversies reported, protests, negative press
- 41-60: EPA/OSHA violations, fines <$1M, labor disputes
- 61-80: Major environmental incidents, fines $1M-$25M, systemic issues
- 81-100: Environmental disasters, fines >$25M, criminal environmental charges

=== REALITY CHECKS ===

1. **Routine business news should score 0-20**
   - "Company sued by customer" = 10-15 (happens constantly)
   - "Regulatory examination opened" = 15-25 (standard oversight)
   - "Negative analyst report" = 10-20 (opinions, not violations)

2. **Only proven violations score 60+**
   - Need: Fines issued, charges filed, settlements admitted
   - NOT: Allegations alone, investigations opened, speculation

3. **For major companies (Fortune 500, public companies):**
   - Expect some lawsuits/complaints = NORMAL
   - Regulatory scrutiny = NORMAL
   - Negative press = NORMAL
   - Don't over-react to routine business friction

4. **Positive/neutral news should score 0-10 across all categories**

=== OUTPUT REQUIREMENTS ===

Score each category 0-100 based on CONCRETE EVIDENCE.
Identify PRIMARY risk (highest score).
Calculate OVERALL severity (max of all categories).
Provide CONFIDENCE (0-100) in your assessment.
Extract 2-3 KEY SENTENCES that support your scores.
Write 2-3 sentence EXPLANATION citing specific facts.

BE CONSERVATIVE. When in doubt, score LOWER. False positives are worse than false negatives."""

        try:
            assessment = self.client.chat.completions.create(
                model=self.model,
                response_model=RiskAssessment,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a highly experienced, skeptical banking compliance analyst. You require strong evidence before flagging high risks. Most news is routine and should score low."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.2  # Lower temperature = more consistent, conservative
            )
            
            # Apply post-processing dampening for major entities
            assessment_dict = assessment.model_dump()
            assessment_dict = self._apply_reality_check(assessment_dict, entity_name)
            
            # Convert back to RiskAssessment
            return RiskAssessment(**assessment_dict)
        
        except Exception as e:
            print(f"❌ Error: {e}")
            
            error_msg = f"AI screening temporarily unavailable. Error: {str(e)[:100]}. Please verify your OpenRouter API key and model availability."
            
            return RiskAssessment(
                fraud=0, sanctions=0, money_laundering=0, bribery_corruption=0,
                cyber_incident=0, insolvency=0, esg_violation=0,
                primary_risk="error",
                overall_severity=0,
                confidence=0,
                key_sentences=[],
                explanation=error_msg
            )
    
    def _apply_reality_check(self, assessment: Dict, entity_name: str) -> Dict:
        """
        Apply reality check dampening for major companies
        Major public companies rarely have genuinely critical (80+) risk scores
        """
        
        # List of major entities that should have dampened scores
        major_entities = [
            'bank of america', 'jp morgan', 'wells fargo', 'citigroup', 'goldman sachs',
            'tesla', 'apple', 'microsoft', 'amazon', 'google', 'meta', 'netflix',
            'boeing', 'ge', 'ford', 'gm', 'walmart', 'target', 'costco',
            'exxon', 'chevron', 'bp', 'shell', 'conocophillips',
            'pfizer', 'merck', 'johnson', 'unitedhealth', 'cvs'
        ]
        
        entity_lower = entity_name.lower()
        is_major = any(name in entity_lower for name in major_entities)
        
        if is_major:
            # For major companies, apply 25% dampening unless truly exceptional
            risk_categories = [
                'fraud', 'sanctions', 'money_laundering', 'bribery_corruption',
                'cyber_incident', 'insolvency', 'esg_violation'
            ]
            
            for category in risk_categories:
                if category in assessment:
                    original = assessment[category]
                    
                    # Strong dampening for major companies
                    # Unless score is based on truly critical evidence (95+), reduce it
                    if original < 95:
                        # Apply 25% reduction
                        dampened = int(original * 0.75)
                        assessment[category] = dampened
            
            # Recalculate overall severity
            category_scores = [assessment.get(cat, 0) for cat in risk_categories]
            assessment['overall_severity'] = max(category_scores) if category_scores else 0
        
        return assessment
    
    def screen_entity(self, articles: List[Dict], entity_name: str) -> Dict:
        """Screen all articles for an entity"""
        if not articles:
            return {
                "entity_name": entity_name,
                "screening_date": datetime.now().isoformat(),
                "articles_analyzed": 0,
                "overall_severity": 0,
                "error": "No articles found"
            }
        
        assessments = []
        print(f"\n🤖 AI Screening: {len(articles)} articles for {entity_name}")
        print(f"📡 Using model: {self.model}")
        print(f"⚙️  Conservative calibration enabled")
        print("=" * 60)
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'Untitled')[:60]
            print(f"  [{i}/{len(articles)}] {title}...")
            
            article_text = f"{article.get('title', '')}\n\n{article.get('content', '')}"
            assessment = self.screen_article(article_text, entity_name)
            
            assessment_dict = assessment.model_dump()
            assessment_dict.update({
                'article_url': article.get('url', ''),
                'article_title': article.get('title', ''),
                'publish_date': article.get('publish_date', ''),
                'source': article.get('source', '')
            })
            
            assessments.append(assessment_dict)
        
        print("\n✅ Screening complete with conservative scoring!")
        return self._aggregate_assessments(assessments, entity_name)
    
    def _aggregate_assessments(self, assessments: List[Dict], entity_name: str) -> Dict:
        """Aggregate with conservative approach"""
        if not assessments:
            return {}
        
        risk_categories = [
            'fraud', 'sanctions', 'money_laundering', 'bribery_corruption',
            'cyber_incident', 'insolvency', 'esg_violation'
        ]
        
        # Take max score per category (worst-case)
        aggregated_scores = {}
        for category in risk_categories:
            scores = [a.get(category, 0) for a in assessments if a.get(category, 0) > 0]
            aggregated_scores[category] = max(scores) if scores else 0
        
        overall_severity = max(aggregated_scores.values())
        high_risk_articles = [a for a in assessments if a.get('overall_severity', 0) > 50]
        high_risk_articles = sorted(high_risk_articles, key=lambda x: x.get('overall_severity', 0), reverse=True)
        primary_risk = max(aggregated_scores, key=aggregated_scores.get)
        
        return {
            "entity_name": entity_name,
            "screening_date": datetime.now().isoformat(),
            "articles_analyzed": len(assessments),
            "overall_severity": overall_severity,
            "primary_risk": primary_risk,
            "risk_scores": aggregated_scores,
            "high_risk_articles": high_risk_articles,
            "all_assessments": assessments
        }

if __name__ == "__main__":
    print("Testing Recalibrated Adverse Media Screener...")
    print("=" * 60)
    
    screener = AdverseMediaScreener()
    
    # Test with routine news
    test_article = """
    Tesla Reports Strong Q3 Earnings, Beats Expectations
    
    Tesla announced quarterly results today that exceeded analyst expectations.
    The company also faces a routine class action lawsuit from customers regarding
    service fee disclosures, which Tesla says it will defend against. The lawsuit
    is in early stages with no findings yet.
    """
    
    result = screener.screen_article(test_article, "Tesla")
    print(f"\n✅ Screening Results:")
    print(f"   Primary Risk: {result.primary_risk.upper()}")
    print(f"   Fraud Score: {result.fraud}/100")
    print(f"   Overall Severity: {result.overall_severity}/100")
    print(f"   Confidence: {result.confidence}%")
    print(f"\n   Explanation: {result.explanation[:200]}...")
