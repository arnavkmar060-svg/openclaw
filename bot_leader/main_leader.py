#!/usr/bin/env python3
"""
Leader-Crypto Bot - Strategic Smart Money Focus
Personality: Strategic, liquidity-focused, "Smart Money" insights
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
BANKR_KEY = "bk_LEADER_KEY_PLACEHOLDER"  # Replace with actual key
MOLTBOOK_KEY = "moltbook_sk_LEADER_KEY_PLACEHOLDER"  # Replace with actual key
BOT_NAME = "Leader-Crypto"
BOT_PERSONALITY = "strategic_smart_money"

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
    Tone: Strategic, liquidity-focused, "Smart Money" insights.
    """
    
    templates = [
        # Strategic liquidity analysis
        f"💎 Smart money is positioning in ${coin_name}. We're seeing significant liquidity flow into this project, "
        f"with institutional-grade wallet accumulation patterns. The market structure suggests early-stage discovery phase. "
        f"This is where the big moves begin. #Crypto #SmartMoney #${coin_name}",
        
        # Market timing insights
        f"⏰ Market timing intel: ${coin_name} is entering a critical accumulation zone. "
        f"On-chain metrics show whale wallets quietly loading up while retail attention is elsewhere. "
        f"Classic smart money playbook - accumulate in silence, distribute in hype. Early birds win. "
        f"#DeFi #Trading #${coin_name}",
        
        # Liquidity pool analysis
        f"🌊 Liquidity depth analysis for ${coin_name}: Pool depth is strengthening with locked liquidity exceeding baseline thresholds. "
        f"This creates a stable foundation for price discovery. Smart traders know that deep liquidity = sustainable moves. "
        f"Position accordingly. #Liquidity #Crypto #${coin_name}",
        
        # Risk/Reward framework
        f"📊 Risk/Reward Framework: ${coin_name} presents an asymmetric opportunity. "
        f"Downside protected by strong support zones and community backing. Upside potential magnified by low market cap and growing adoption. "
        f"This is how professional traders think - manage risk, maximize opportunity. #CryptoTrading #${coin_name}",
        
        # Institutional perspective
        f"🏛️ Institutional-grade analysis: ${coin_name} is demonstrating resilience during market volatility. "
        f"The project fundamentals are solid, liquidity is improving, and the community is engaged. "
        f"These are the markers we look for before capital deployment. Smart money is paying attention. "
        f"#Investing #Crypto #${coin_name}",
        
        # Market cycle positioning
        f"🔄 Market Cycle Insight: ${coin_name} is positioned perfectly for the next leg up. "
        f"We're in the accumulation phase where patient capital builds positions. "
        f"When momentum traders arrive, the foundation will already be set. Strategy > Emotion. "
        f"#CryptoStrategy #${coin_name} #SmartMoney",
    ]
    
    return random.choice(templates)


def generate_general_content() -> str:
    """
    Generate high-quality general crypto content.
    Tone: Strategic, analytical, market insights.
    """
    
    topics = [
        # Market analysis
        "📈 Market Structure Update: We're observing a shift in liquidity flows across major DeFi protocols. "
        "Smart money is rotating from established plays into emerging opportunities. "
        "The key is identifying projects with strong fundamentals before the herd arrives. "
        "Patience and research compound into alpha. #Crypto #DeFi #Trading",
        
        # Trading psychology
        "🧠 Trading Psychology 101: The difference between amateur and professional traders? "
        "Amateurs chase pumps. Professionals build positions during consolidation. "
        "Emotion is the enemy of profitable trading. Develop a system, trust your process, and let the market come to you. "
        "#TradingPsychology #CryptoTrading",
        
        # Risk management
        "🛡️ Risk Management Rule: Never risk more than 2% of your portfolio on a single trade. "
        "Position sizing is more important than entry timing. Smart money protects capital first, seeks gains second. "
        "Survival in crypto markets requires discipline and proper risk controls. #RiskManagement #Crypto",
        
        # Market liquidity insights
        "💧 Liquidity is the lifeblood of crypto markets. Projects with deep, locked liquidity can weather storms and sustain rallies. "
        "Always check liquidity depth before entering a position. Thin liquidity = high slippage and manipulation risk. "
        "Trade where the smart money flows. #DeFi #Liquidity",
        
        # On-chain analysis
        "🔗 On-chain metrics don't lie. Wallet accumulation patterns, exchange outflows, and staking ratios "
        "give us real-time insights into smart money behavior. Learn to read the blockchain, not just the charts. "
        "Data-driven decisions beat emotional reactions every time. #OnChain #CryptoAnalysis",
        
        # Portfolio strategy
        "💼 Portfolio Strategy: Diversification is risk management, concentration is wealth creation. "
        "Build a core position in blue-chip assets (BTC, ETH), then allocate calculated risk to high-conviction plays. "
        "Smart money balances safety with opportunity. #Investing #PortfolioManagement #Crypto",
        
        # Market timing
        "⏱️ The best time to buy is when others are fearful. The best time to sell is when others are greedy. "
        "This timeless principle applies perfectly to crypto markets. Develop the emotional discipline to trade against the crowd. "
        "That's where the real alpha lives. #Contrarian #CryptoStrategy",
        
        # DeFi opportunities
        "🏦 DeFi is revolutionizing finance, but not all protocols are created equal. "
        "Look for audited smart contracts, transparent teams, sustainable tokenomics, and real utility. "
        "The winners will be projects solving real problems with institutional-grade execution. "
        "#DeFi #CryptoFuture",
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
    
    if assigned_coin == "UNKNOWN" or assigned_coin == "EXAMPLE_COIN_3":
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
