"""
Enhanced News Fetcher with Balanced Coverage
- Fetches ALL news (not just negative)
- Caching support for faster results
- Better error handling
- Supports unlimited articles
"""
import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
from urllib.parse import quote
import random
import hashlib
import json
import os

class NewsFetcher:
    def __init__(self):
        self.base_url = "https://news.google.com/rss/search"
        self.timeout = 10
        self.cache_dir = "data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_key(self, entity_name: str, days_back: int) -> str:
        """Generate cache key for entity + date"""
        key_string = f"{entity_name}_{days_back}_{datetime.now().strftime('%Y-%m-%d')}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _load_from_cache(self, cache_key: str) -> List[Dict]:
        """Load cached results if available"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                # Check if cache is from today
                cache_time = os.path.getmtime(cache_file)
                cache_date = datetime.fromtimestamp(cache_time).date()
                if cache_date == datetime.now().date():
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        print(f"💾 Loaded {len(data)} articles from cache")
                        return data
            except Exception as e:
                print(f"⚠️  Cache read error: {e}")
        return None
    
    def _save_to_cache(self, cache_key: str, data: List[Dict]):
        """Save results to cache"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Cache write error: {e}")
    
    def fetch_google_news_rss(self, entity_name: str, days_back: int = 30, max_results: int = 100) -> List[Dict]:
        """
        Fetch BALANCED news coverage from Google News RSS
        - Gets ALL news (positive, negative, neutral)
        - No keyword bias toward negative news
        - Supports caching for faster results
        """
        
        # Check cache first
        cache_key = self._get_cache_key(entity_name, days_back)
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            return cached_data[:max_results]
        
        try:
            # BALANCED QUERY - just the entity name, no negative keyword bias
            query = f'"{entity_name}"'
            
            # Calculate date range
            after_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            # Build RSS URL
            query_encoded = quote(query, safe='')
            rss_url = f"{self.base_url}?q={query_encoded}+after:{after_date}&hl=en-US&gl=US&ceid=US:en"
            
            print(f"🔍 Fetching balanced news coverage for '{entity_name}'...")
            
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                print("⚠️  No articles found in Google RSS, using demo data")
                return self._get_demo_data(entity_name)
            
            articles = []
            for entry in feed.entries:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                link = entry.get('link', '')
                
                # Extract source
                source = 'Unknown'
                if hasattr(entry, 'source') and hasattr(entry.source, 'title'):
                    source = entry.source.title
                
                pub_date = entry.get('published', '')
                
                # Skip very short articles (likely duplicates or stubs)
                if len(summary) < 50:
                    continue
                
                articles.append({
                    "title": title,
                    "content": summary,
                    "url": link,
                    "source": source,
                    "publish_date": pub_date
                })
            
            if articles:
                print(f"✅ Found {len(articles)} articles from Google News RSS")
                # Save to cache
                self._save_to_cache(cache_key, articles)
                return articles[:max_results]
            else:
                print("⚠️  No valid articles found, using demo data")
                return self._get_demo_data(entity_name)
        
        except Exception as e:
            print(f"⚠️  Error fetching Google RSS: {e}")
            print("📝 Using demo data")
            return self._get_demo_data(entity_name)
    
    def _get_demo_data(self, entity_name: str) -> List[Dict]:
        """
        Generate realistic demo data with BALANCED coverage
        (positive, negative, and neutral news)
        """
        
        # Mix of risk articles AND positive/neutral articles
        articles = []
        
        # Some negative/risk articles (realistic for any company)
        risk_articles = [
            {
                "title": f"{entity_name} Faces Class Action Lawsuit Over Service Fees",
                "content": f"A group of customers has filed a class action lawsuit against {entity_name} alleging improper service fees. The lawsuit, filed in federal court, claims fees were not properly disclosed. {entity_name} stated it will vigorously defend against the claims and believes they are without merit. The case is in early stages and no findings have been made.",
                "source": "Reuters",
                "severity_hint": "low"  # Just a lawsuit, common for large companies
            },
            {
                "title": f"{entity_name} Under Regulatory Review for Compliance Practices",
                "content": f"Financial regulators have opened a routine examination of {entity_name}'s compliance procedures as part of periodic oversight. The company is cooperating fully with the review. Industry experts note such examinations are standard practice and do not indicate wrongdoing. {entity_name} maintains it follows all applicable regulations.",
                "source": "Wall Street Journal",
                "severity_hint": "low"  # Routine examination
            },
        ]
        
        # Positive articles (balance the negative)
        positive_articles = [
            {
                "title": f"{entity_name} Reports Strong Quarterly Earnings, Beats Estimates",
                "content": f"{entity_name} today announced quarterly results that exceeded analyst expectations, with revenue up 12% year-over-year. The company raised its full-year guidance and announced plans to expand operations. CEO stated the results demonstrate strong execution and customer demand. Shares rose 5% on the news.",
                "source": "CNBC",
                "severity_hint": "positive"
            },
            {
                "title": f"{entity_name} Announces $500M Investment in Sustainability Initiatives",
                "content": f"{entity_name} unveiled plans to invest $500 million in environmental sustainability over the next five years. The initiative includes renewable energy adoption, carbon footprint reduction, and sustainable supply chain programs. Environmental groups praised the commitment. The company aims for net-zero emissions by 2040.",
                "source": "Bloomberg",
                "severity_hint": "positive"
            },
            {
                "title": f"{entity_name} Named One of Best Places to Work in 2025",
                "content": f"Fortune magazine included {entity_name} in its 2025 list of 100 Best Companies to Work For, citing strong employee benefits, career development programs, and workplace culture. The company received high marks for diversity initiatives and work-life balance. {entity_name} has been on the list for five consecutive years.",
                "source": "Fortune",
                "severity_hint": "positive"
            },
        ]
        
        # Neutral articles (standard business news)
        neutral_articles = [
            {
                "title": f"{entity_name} Announces New Product Launch for Fall 2025",
                "content": f"{entity_name} today previewed its upcoming product line scheduled for release in Fall 2025. The company showcased features and pricing at an industry conference. Analysts expect moderate market reception. The products will compete in a crowded market segment.",
                "source": "TechCrunch",
                "severity_hint": "neutral"
            },
            {
                "title": f"{entity_name} Opens New Regional Office, Plans to Hire 200 Employees",
                "content": f"{entity_name} celebrated the opening of a new regional office today, with plans to hire 200 employees over the next 18 months. Local officials attended the ribbon-cutting ceremony. The expansion is part of the company's strategy to increase geographic presence. Hiring will begin immediately.",
                "source": "Local Business Journal",
                "severity_hint": "neutral"
            },
            {
                "title": f"{entity_name} CEO Speaks at Industry Conference on Digital Transformation",
                "content": f"The CEO of {entity_name} delivered a keynote address at the annual industry conference, discussing digital transformation strategies and market trends. The executive emphasized the importance of innovation and customer-centric approaches. Attendees praised the insights shared during the presentation.",
                "source": "Industry Today",
                "severity_hint": "neutral"
            },
        ]
        
        # Combine all article types for balanced coverage
        all_demo_articles = risk_articles + positive_articles + neutral_articles
        
        # Add timestamps and format
        for i, article_data in enumerate(all_demo_articles):
            days_ago = random.randint(1, 30)
            pub_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            articles.append({
                "title": article_data["title"],
                "content": article_data["content"],
                "url": f"https://example.com/{entity_name.lower().replace(' ', '-')}-article-{i+1}",
                "source": article_data["source"],
                "publish_date": pub_date
            })
        
        print(f"📝 Generated {len(articles)} balanced demo articles (positive + negative + neutral)")
        return articles
    
    def fetch_all_news(self, entity_name: str, days_back: int = 30, max_articles: int = 100) -> List[Dict]:
        """
        Main method to fetch news
        - Tries Google News RSS first
        - Falls back to demo data if needed
        - Returns deduplicated results
        """
        
        # Fetch from Google News RSS
        articles = self.fetch_google_news_rss(entity_name, days_back, max_articles)
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_articles = []
        for article in articles:
            url = article.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        # Limit to max_articles
        final_articles = unique_articles[:max_articles]
        
        print(f"📊 Returning {len(final_articles)} unique articles for analysis")
        return final_articles

# Test function
if __name__ == "__main__":
    print("Testing Enhanced News Fetcher...")
    print("=" * 70)
    
    fetcher = NewsFetcher()
    
    # Test with a well-known company
    test_entity = "Tesla"
    print(f"\n🔍 Fetching balanced news for: {test_entity}")
    print("-" * 70)
    
    articles = fetcher.fetch_all_news(test_entity, days_back=30, max_articles=20)
    
    print(f"\n✅ Retrieved {len(articles)} articles")
    print("\n📰 Sample articles:")
    print("=" * 70)
    
    for i, article in enumerate(articles[:5], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   📰 Source: {article['source']}")
        print(f"   📅 Date: {article['publish_date'][:10]}")
        print(f"   📝 Content: {article['content'][:100]}...")
        print(f"   🔗 URL: {article['url'][:60]}...")
    
    print("\n" + "=" * 70)
    print("✅ News fetcher test complete!")
