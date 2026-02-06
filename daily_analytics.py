#!/usr/bin/env python3
"""
Daily Analytics Script - Trend Hunter
Analyzes market trends using Banker's Market Intelligence API with fallback to simulation mode.
"""

import requests
import json
import logging
import random
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Banker API Configuration
BANKER_API_BASE = "https://api.bankr.bot"
BANKER_API_KEY = "bk_XE6SA2BLVX5U37LET5KMLYRGJMRMEPG8"  # Default key, can be overridden

class TrendHunter:
    """
    Main class for hunting trending coins and generating similar coin suggestions.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Trend Hunter with API key."""
        self.api_key = api_key or BANKER_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.simulation_mode = False
        
    def query_market_intelligence(self, query_type: str = "trending") -> Optional[Dict]:
        """
        Query Banker's market_intelligence endpoint.
        
        Args:
            query_type: Type of query ("trending", "category", etc.)
            
        Returns:
            API response data or None if failed
        """
        endpoint = f"{BANKER_API_BASE}/market_intelligence"
        
        payload = {
            "query_type": query_type,
            "limit": 10
        }
        
        try:
            logger.info(f"🔍 Querying Banker's Market Intelligence ({query_type})...")
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Market Intelligence data received: {len(data.get('trends', []))} trends found")
                return data
            elif response.status_code == 402:
                logger.warning("⚠️ Payment Required (402) - Switching to Simulation Mode")
                self.simulation_mode = True
                return None
            else:
                logger.error(f"❌ API Error {response.status_code}: {response.text}")
                self.simulation_mode = True
                return None
                
        except Exception as e:
            logger.error(f"❌ Exception during API call: {e}")
            self.simulation_mode = True
            return None
    
    def perform_technical_analysis(self, coin_symbol: str) -> Optional[Dict]:
        """
        Perform technical analysis on a specific coin.
        
        Args:
            coin_symbol: The coin symbol to analyze
            
        Returns:
            Technical analysis data or None
        """
        endpoint = f"{BANKER_API_BASE}/technical_analysis"
        
        payload = {
            "symbol": coin_symbol,
            "timeframe": "1h"
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Technical analysis failed for {coin_symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Technical analysis exception: {e}")
            return None
    
    def get_social_sentiment(self, coin_name: str) -> Optional[Dict]:
        """
        Get social sentiment for a coin.
        
        Args:
            coin_name: The coin name or symbol
            
        Returns:
            Social sentiment data or None
        """
        endpoint = f"{BANKER_API_BASE}/social_sentiment"
        
        payload = {
            "query": coin_name
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Social sentiment failed for {coin_name}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Social sentiment exception: {e}")
            return None
    
    def simulation_mode_trends(self) -> List[Dict]:
        """
        Fallback simulation mode using Google Trends/Twitter simulation.
        
        Returns:
            List of simulated trending topics
        """
        logger.info("🎭 Running in SIMULATION MODE - Using fallback trend detection")
        
        # Try pytrends if available
        try:
            from pytrends.request import TrendReq
            
            pytrends = TrendReq(hl='en-US', tz=360)
            trending = pytrends.trending_searches(pn='united_states')
            
            trends = []
            for i, trend in enumerate(trending.head(5).values):
                trend_name = trend[0]
                trends.append({
                    'name': trend_name,
                    'volume': random.randint(10000, 100000),
                    'sentiment': random.choice(['Very Positive', 'Positive', 'Neutral']),
                    'source': 'Google Trends'
                })
                
            logger.info(f"✅ Google Trends: Found {len(trends)} trending topics")
            return trends
            
        except ImportError:
            logger.warning("⚠️ pytrends not installed, using mock trends")
            
        except Exception as e:
            logger.warning(f"⚠️ Google Trends failed: {e}, using mock trends")
        
        # Fallback to mock trends based on current crypto themes
        mock_trends = [
            {'name': 'AI Agent', 'volume': 85000, 'sentiment': 'Very Positive', 'source': 'Mock'},
            {'name': 'DeFi Protocol', 'volume': 72000, 'sentiment': 'Positive', 'source': 'Mock'},
            {'name': 'Pepe', 'volume': 68000, 'sentiment': 'Very Positive', 'source': 'Mock'},
            {'name': 'Base Chain', 'volume': 55000, 'sentiment': 'Positive', 'source': 'Mock'},
            {'name': 'Memecoin', 'volume': 50000, 'sentiment': 'Neutral', 'source': 'Mock'},
        ]
        
        logger.info(f"✅ Mock Trends: Generated {len(mock_trends)} trending topics")
        return mock_trends
    
    def generate_similar_names(self, trend_name: str, count: int = 3) -> List[str]:
        """
        Generate similar coin names based on a trend.
        
        Args:
            trend_name: The base trend name
            count: Number of similar names to generate
            
        Returns:
            List of generated coin names
        """
        # Clean the trend name
        clean_name = ''.join(e for e in trend_name if e.isalnum())
        
        # Suffixes and prefixes that work well for memecoins
        suffixes = ['AI', 'Bot', 'Coin', 'Token', 'Inu', 'Moon', 'Doge', 'Protocol', 'Finance', 'Swap']
        prefixes = ['Meta', 'Super', 'Ultra', 'Mega', 'Giga', 'Hyper', 'Cyber', 'Smart', 'Turbo', 'Alpha']
        
        similar_names = []
        
        # Strategy 1: Add AI/Bot/Coin suffix
        if len(clean_name) <= 10:
            for suffix in random.sample(suffixes, min(3, len(suffixes))):
                if len(similar_names) >= count:
                    break
                name = f"{clean_name}{suffix}"
                if name not in similar_names:
                    similar_names.append(name)
        
        # Strategy 2: Add prefix
        if len(similar_names) < count:
            for prefix in random.sample(prefixes, min(3, len(prefixes))):
                if len(similar_names) >= count:
                    break
                name = f"{prefix}{clean_name}"
                if name not in similar_names:
                    similar_names.append(name)
        
        # Strategy 3: Combine with popular memecoin patterns
        if len(similar_names) < count:
            patterns = [
                f"{clean_name}2.0",
                f"x{clean_name}",
                f"{clean_name}Verse",
            ]
            for pattern in patterns:
                if len(similar_names) >= count:
                    break
                if pattern not in similar_names:
                    similar_names.append(pattern)
        
        return similar_names[:count]
    
    def analyze_and_suggest(self) -> List[Dict[str, str]]:
        """
        Main analysis function: Get trends and suggest 3 coin names.
        
        Returns:
            List of dictionaries with trend info and suggested names
        """
        logger.info("=" * 60)
        logger.info("🚀 STARTING DAILY TREND ANALYSIS")
        logger.info("=" * 60)
        
        # Step 1: Get market intelligence
        trends_data = self.query_market_intelligence("trending")
        
        if trends_data and not self.simulation_mode:
            # Parse real API data
            trends = trends_data.get('trends', [])[:3]
            logger.info(f"📊 Using real market data: {len(trends)} trends")
        else:
            # Use simulation mode
            trends = self.simulation_mode_trends()[:3]
        
        suggestions = []
        
        for i, trend in enumerate(trends, 1):
            trend_name = trend.get('name', f"Trend{i}")
            
            logger.info(f"\n{'=' * 60}")
            logger.info(f"📈 TREND #{i}: {trend_name}")
            logger.info(f"{'=' * 60}")
            logger.info(f"   Volume/Mentions: {trend.get('volume', 'N/A')}")
            logger.info(f"   Sentiment: {trend.get('sentiment', 'N/A')}")
            logger.info(f"   Source: {trend.get('source', 'API')}")
            
            # Validate with technical analysis (if API available)
            if not self.simulation_mode:
                tech_analysis = self.perform_technical_analysis(trend_name)
                if tech_analysis:
                    logger.info(f"   Technical Score: {tech_analysis.get('score', 'N/A')}")
                
                sentiment = self.get_social_sentiment(trend_name)
                if sentiment:
                    logger.info(f"   Social Score: {sentiment.get('score', 'N/A')}")
            
            # Generate similar names
            similar_names = self.generate_similar_names(trend_name, count=3)
            
            logger.info(f"\n   💡 SUGGESTED COIN NAMES:")
            for idx, name in enumerate(similar_names, 1):
                logger.info(f"      {idx}. {name}")
            
            suggestions.append({
                'trend': trend_name,
                'volume': trend.get('volume', 0),
                'sentiment': trend.get('sentiment', 'Unknown'),
                'suggested_names': similar_names
            })
        
        return suggestions
    
    def print_final_suggestions(self, suggestions: List[Dict]) -> Tuple[str, str, str]:
        """
        Print final 3 coin suggestions clearly for manual launch.
        
        Args:
            suggestions: List of suggestion dictionaries
            
        Returns:
            Tuple of 3 coin names to launch
        """
        logger.info("\n" + "=" * 60)
        logger.info("🎯 FINAL 3 COIN SUGGESTIONS FOR LAUNCH")
        logger.info("=" * 60)
        
        # Pick the best name from each trend
        final_three = []
        
        for i, suggestion in enumerate(suggestions[:3], 1):
            # Pick the first suggested name (usually the best)
            coin_name = suggestion['suggested_names'][0]
            final_three.append(coin_name)
            
            logger.info(f"\n{i}. 🚀 {coin_name}")
            logger.info(f"   Based on trend: {suggestion['trend']}")
            logger.info(f"   Volume: {suggestion['volume']}")
            logger.info(f"   Sentiment: {suggestion['sentiment']}")
        
        logger.info("\n" + "=" * 60)
        logger.info("📋 COPY THESE NAMES TO LAUNCH:")
        logger.info("=" * 60)
        for i, name in enumerate(final_three, 1):
            logger.info(f"{i}. {name}")
        
        logger.info("\n" + "=" * 60)
        logger.info("💾 Update 'active_campaigns.json' with these names!")
        logger.info("=" * 60)
        
        # Ensure we have exactly 3 names
        while len(final_three) < 3:
            final_three.append(f"DefaultCoin{len(final_three) + 1}")
        
        return tuple(final_three[:3])


def main():
    """Main execution function."""
    try:
        # Initialize the Trend Hunter
        hunter = TrendHunter()
        
        # Run analysis
        suggestions = hunter.analyze_and_suggest()
        
        # Print final suggestions
        coin1, coin2, coin3 = hunter.print_final_suggestions(suggestions)
        
        # Save to a file for easy reference
        output_file = "suggested_coins.json"
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "simulation_mode": hunter.simulation_mode,
            "suggestions": [
                {"bot": "Nemr_AI", "suggested_coin": coin1},
                {"bot": "Eng_Crypto", "suggested_coin": coin2},
                {"bot": "Leader-Crypto", "suggested_coin": coin3}
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        logger.info(f"\n✅ Suggestions saved to: {output_file}")
        logger.info("🎉 Analysis Complete!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Fatal error in main execution: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
