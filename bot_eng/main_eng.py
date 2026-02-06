#!/usr/bin/env python3
"""
Eng_Crypto Bot - Technical Analyst
Personality: Technical, analytical, data-driven
"""

import requests
import schedule
import time
import logging
import random
import json
import os
from datetime import datetime, timedelta

# Bot Configuration
BANKR_KEY = "bk_9CLVKYTQKHYYZXRES6A5TJL7MYJLDJT8"
MOLTBOOK_KEY = "moltbook_sk_mwrTMYQHQX4Y17sSeOySpzc1OlHD56BN"
BOT_NAME = "Eng_Crypto"
BOT_PERSONALITY = "technical_analytical"

# File paths
CAMPAIGNS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "active_campaigns.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "log.txt")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(BOT_NAME)

# Post tracking
daily_posts = {"promotional": 0, "general": 0, "last_reset": datetime.now().date()}


def reset_daily_counters():
    """Reset daily post counters at midnight."""
    global daily_posts
    if daily_posts["last_reset"] != datetime.now().date():
        daily_posts = {"promotional": 0, "general": 0, "last_reset": datetime.now().date()}
        logger.info("🔄 Daily counters reset")


def load_campaign_config():
    """Load the active campaigns configuration."""
    try:
        with open(CAMPAIGNS_FILE, 'r') as f:
            config = json.load(f)
        
        bot_campaign = config['campaigns'].get(BOT_NAME, {})
        assigned_coin = bot_campaign.get('assigned_coin', 'UNKNOWN')
        
        logger.info(f"📋 Loaded campaign: Assigned coin = {assigned_coin}")
        return assigned_coin, config
    
    except FileNotFoundError:
        logger.warning(f"⚠️ Campaign config not found: {CAMPAIGNS_FILE}")
        return "UNKNOWN", {}
    
    except Exception as e:
        logger.error(f"❌ Error loading campaign config: {e}")
        return "UNKNOWN", {}


def generate_promotional_content(coin_name: str) -> str:
    """
    Generate high-quality promotional content for the assigned coin.
    Tone: Technical, analytical, data-driven.
    """
    
    templates = [
        # Technical analysis focus
        f"📊 Technical Analysis: ${coin_name} is showing strong momentum indicators across multiple timeframes. "
        f"RSI trending upward, MACD crossover confirmed, and volume profile indicates accumulation phase. "
        f"The technical structure supports continued upward movement with key support levels holding firm. "
        f"Data suggests this is a technically sound entry point. #CryptoAnalysis #${coin_name} #TechnicalAnalysis",
        
        # On-chain metrics
        f"🔗 On-Chain Data Analysis for ${coin_name}: Network activity shows significant growth with increasing "
        f"unique addresses and transaction volume up 45% over the past 7 days. Active wallet count reached new highs, "
        f"indicating organic growth and adoption. The fundamentals are strengthening - this is what sustainable "
        f"growth looks like. #OnChain #${coin_name} #DataDriven",
        
        # Chart pattern identification
        f"📈 Chart Pattern Alert: ${coin_name} has formed a bullish ascending triangle on the 4H timeframe. "
        f"Historical data shows this pattern has an 80% probability of breakout continuation. "
        f"Key resistance at current levels, with volume increasing on upward moves. "
        f"Technical traders should monitor the breakout zone closely. #ChartAnalysis #${coin_name} #Trading",
        
        # Risk/reward calculation
        f"⚖️ Risk/Reward Analysis: ${coin_name} presents a favorable 1:4 risk-reward ratio at current levels. "
        f"Stop loss placement below recent support offers capital protection, while profit targets align with "
        f"Fibonacci extension levels. Probability-weighted outcomes favor long positions based on technical confluence. "
        f"Systematic approach yields positive expectancy. #RiskManagement #${coin_name}",
        
        # Volume analysis
        f"📊 Volume Analysis: ${coin_name} is experiencing above-average volume with strong buy-side pressure. "
        f"Order book depth shows increasing bid support and decreasing ask resistance. "
        f"Volume-price correlation is positive, confirming the legitimacy of the current move. "
        f"Technical indicators align with volume data for high-probability setup. #VolumeAnalysis #${coin_name}",
        
        # Indicator convergence
        f"🎯 Multi-Indicator Convergence: ${coin_name} displays alignment across key technical indicators. "
        f"Moving averages show bullish crossover (50 MA > 200 MA), momentum oscillators trending positive, "
        f"and price action respecting Fibonacci retracement levels. When multiple indicators confirm the same signal, "
        f"probability of success increases significantly. #TechnicalTrading #${coin_name}",
    ]
    
    return random.choice(templates)


def generate_general_content() -> str:
    """
    Generate high-quality general crypto content.
    Tone: Technical, educational, analytical.
    """
    
    topics = [
        # Technical trading education
        "📚 Technical Trading 101: Moving averages are lagging indicators, but they provide crucial trend confirmation. "
        "The 50-day and 200-day moving average crossover (Golden Cross) historically signals strong bullish momentum. "
        "Combine with volume analysis and support/resistance levels for higher probability trades. "
        "Understanding technical tools is essential for systematic trading. #TechnicalAnalysis #Education",
        
        # Risk management systems
        "🛡️ Professional Risk Management: Never risk more than 1-2% of portfolio on a single trade. "
        "Use stop-loss orders to automate risk control. Calculate position size based on account size and stop distance. "
        "Risk management isn't optional - it's the difference between surviving and thriving in crypto markets. "
        "#RiskManagement #Trading",
        
        # Data-driven approach
        "📊 Data > Emotions: Successful crypto trading requires systematic, data-driven decision making. "
        "Track your trades, analyze win rates, measure risk-reward ratios, and optimize based on statistics. "
        "Emotional trading loses money. Statistical trading builds wealth. "
        "Let the data guide your decisions. #DataDriven #CryptoTrading",
        
        # Chart pattern education
        "📈 Chart Patterns That Work: Head and Shoulders, Double Tops/Bottoms, Triangles, and Flags have "
        "statistically proven success rates when properly identified. Study pattern completion rates, measure targets, "
        "and wait for confirmation before entry. Pattern recognition is a skill that improves with practice and data. "
        "#ChartPatterns #TechnicalAnalysis",
        
        # Indicator optimization
        "⚙️ Indicator Optimization: RSI, MACD, Stochastic, and Bollinger Bands are powerful when used correctly. "
        "Avoid indicator overload - focus on 2-3 that complement each other. Test different parameters on historical data "
        "to find optimal settings for your trading timeframe. Quality over quantity in technical analysis. "
        "#Indicators #Trading",
        
        # Market structure analysis
        "🏗️ Market Structure Analysis: Understanding higher highs, higher lows (uptrend) vs lower highs, lower lows (downtrend) "
        "is fundamental to technical trading. Market structure reveals the underlying trend and guides trade direction. "
        "Combine with support/resistance zones for precise entry and exit points. "
        "#MarketStructure #TechnicalAnalysis",
        
        # Backtesting importance
        "🔬 The Power of Backtesting: Before risking real capital, test your strategy on historical data. "
        "Measure win rate, average profit/loss, maximum drawdown, and risk-adjusted returns. "
        "A strategy that worked in the past isn't guaranteed to work in the future, but it's better than guessing. "
        "Data-driven strategy development is professional trading. #Backtesting #SystematicTrading",
        
        # Volume profile analysis
        "📊 Volume Profile Analysis: Price moves on volume. High volume nodes indicate areas of strong buyer/seller interest. "
        "Low volume zones typically see rapid price movement. Understanding volume distribution helps identify "
        "support/resistance levels that actually matter. Volume speaks louder than price alone. "
        "#VolumeProfile #Trading",
    ]
    
    return random.choice(topics)


def post_to_moltbook(content: str) -> bool:
    """
    Post content to MoltBook platform.
    
    Args:
        content: The content to post
        
    Returns:
        True if successful, False otherwise
    """
    try:
        url = "https://api.moltbook.com/v1/posts"
        headers = {
            "Authorization": f"Bearer {MOLTBOOK_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "content": content,
            "visibility": "public"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            logger.info(f"✅ Posted successfully to MoltBook")
            return True
        else:
            logger.warning(f"⚠️ MoltBook post failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error posting to MoltBook: {e}")
        return False


def promotional_cycle():
    """Execute a promotional post cycle (3x per day)."""
    reset_daily_counters()
    
    if daily_posts["promotional"] >= 3:
        logger.info("⏭️ Daily promotional limit reached (3/3)")
        return
    
    assigned_coin, config = load_campaign_config()
    
    if assigned_coin == "UNKNOWN" or assigned_coin == "EXAMPLE_COIN_2":
        logger.warning("⚠️ No valid coin assigned. Skipping promotional post.")
        return
    
    content = generate_promotional_content(assigned_coin)
    
    logger.info(f"🚀 Posting promotional content for ${assigned_coin}")
    logger.info(f"📝 Content preview: {content[:100]}...")
    
    if post_to_moltbook(content):
        daily_posts["promotional"] += 1
        logger.info(f"✅ Promotional post {daily_posts['promotional']}/3 completed")


def general_content_cycle():
    """Execute a general content post cycle."""
    reset_daily_counters()
    
    content = generate_general_content()
    
    logger.info(f"📢 Posting general content")
    logger.info(f"📝 Content preview: {content[:100]}...")
    
    if post_to_moltbook(content):
        daily_posts["general"] += 1
        logger.info(f"✅ General post #{daily_posts['general']} completed")


def setup_schedule():
    """Set up the posting schedule."""
    # Promotional posts: 3x per day at specific times
    schedule.every().day.at("09:00").do(promotional_cycle)
    schedule.every().day.at("14:00").do(promotional_cycle)
    schedule.every().day.at("20:00").do(promotional_cycle)
    
    # General content: Every 2 hours
    schedule.every(2).hours.do(general_content_cycle)
    
    logger.info("📅 Schedule configured:")
    logger.info("   - Promotional posts: 09:00, 14:00, 20:00 (3x daily)")
    logger.info("   - General content: Every 2 hours")


def run_bot():
    """Main bot execution loop."""
    logger.info("=" * 60)
    logger.info(f"🤖 {BOT_NAME} - STARTING UP")
    logger.info(f"⚡ Personality: {BOT_PERSONALITY}")
    logger.info("=" * 60)
    
    # Setup schedule
    setup_schedule()
    
    # Run an immediate general post on startup
    logger.info("🚀 Running initial general content post...")
    general_content_cycle()
    
    logger.info("♻️ Entering scheduled loop...")
    
    # Main loop
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
        except KeyboardInterrupt:
            logger.info("\n🛑 Bot stopped by user")
            break
            
        except Exception as e:
            logger.error(f"❌ Error in main loop: {e}")
            time.sleep(300)  # Wait 5 minutes before retry


if __name__ == "__main__":
    run_bot()
