#!/usr/bin/env python3
"""
Nemr_AI Bot - Community-Focused Storyteller
Personality: Enthusiastic, community-focused, storytelling
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
BANKR_KEY = "bk_XE6SA2BLVX5U37LET5KMLYRGJMRMEPG8"
MOLTBOOK_KEY = "moltbook_sk_c1f0hM1mYPXxgaJgXadTFjB95ofK5xhv"
BOT_NAME = "Nemr_AI"
BOT_PERSONALITY = "enthusiastic_community"

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
    Tone: Enthusiastic, community-focused, storytelling.
    """
    
    templates = [
        # Community building story
        f"🌟 Amazing things happen when a community comes together! ${coin_name} isn't just another token - "
        f"it's a movement of passionate believers building something special. Every holder is part of our story, "
        f"and together we're creating the next crypto success tale. Join us on this incredible journey! "
        f"🚀 #Community #${coin_name} #CryptoFamily",
        
        # Success story narrative
        f"💎 Real talk: ${coin_name} started as an idea, but the community transformed it into reality. "
        f"We've watched holders go from curious observers to passionate advocates. That's the power of a "
        f"strong community-driven project. We're not just trading tokens, we're building a legacy together. "
        f"Who's ready for the next chapter? 🌙 #${coin_name} #ToTheMoon",
        
        # Emotional connection
        f"❤️ You know what makes ${coin_name} different? It's YOU. It's US. It's the amazing community that "
        f"believes in what we're building. Every comment, every share, every holder adds value to this project. "
        f"We're not just investors - we're pioneers creating the future of crypto together! "
        f"Let's make history! 🔥 #${coin_name} #CryptoCommunity",
        
        # Inspirational journey
        f"🎯 From zero to hero - that's the ${coin_name} story! Started by dreamers, supported by believers, "
        f"and powered by an unstoppable community. We're proving every day that when people unite around a vision, "
        f"magic happens. This isn't just about gains, it's about building something extraordinary together! "
        f"Are you ready to be part of greatness? 💪 #${coin_name} #CryptoRevolution",
        
        # Celebration of milestones
        f"🎉 The ${coin_name} community keeps growing stronger every single day! New holders joining, engagement "
        f"soaring, and the energy is absolutely electric! This is what happens when genuine people support a "
        f"genuine project. We're not just holding tokens, we're holding tickets to an amazing future. "
        f"Welcome to the family, everyone! 🌈 #${coin_name} #CryptoSuccess",
        
        # Vision and dreams
        f"✨ Imagine a crypto project where the community truly matters. Where every voice is heard, every holder "
        f"is valued, and dreams become reality. That's ${coin_name}! We're building more than a token - "
        f"we're creating a movement that will change lives. Join thousands of believers who see the vision and "
        f"are making it happen together! 🌟 #${coin_name} #DreamBig",
    ]
    
    return random.choice(templates)


def generate_general_content() -> str:
    """
    Generate high-quality general crypto content.
    Tone: Enthusiastic, educational, community-focused.
    """
    
    topics = [
        # Crypto education
        "📚 Crypto 101: The beauty of blockchain is that it gives power back to the people! "
        "No banks, no middlemen, just peer-to-peer transactions secured by mathematics. "
        "We're witnessing a financial revolution, and everyone can be part of it. "
        "Start learning, start growing, start winning! 🚀 #CryptoEducation #Blockchain",
        
        # Community wisdom
        "💡 Community Wisdom: The best investments aren't just about charts and numbers. "
        "They're about people, vision, and shared belief in a better future. "
        "Find projects with strong communities, genuine teams, and real utility. "
        "That's where the magic happens! 🌟 #CryptoCommunity #InvestSmart",
        
        # Motivational message
        "🔥 Remember: Every crypto giant started small. Bitcoin was pennies. Ethereum was undervalued. "
        "The projects changing the world today were once just ideas supported by passionate communities. "
        "Stay curious, stay engaged, and stay positive. Your journey in crypto is just beginning! "
        "#CryptoMotivation #WAGMI",
        
        # Success stories
        "🎊 Love hearing success stories from the crypto community! People who believed early, held through "
        "volatility, and supported their projects are now celebrating life-changing wins. "
        "The lesson? Find great communities, contribute value, and patience pays off. "
        "Your story could be next! 📈 #CryptoSuccess #BelieveInYourself",
        
        # Market positivity
        "☀️ The crypto market is full of opportunities for those who stay positive and informed! "
        "Bear markets build character, bull markets build wealth, but community builds everything. "
        "Stay connected with projects you believe in, support fellow crypto enthusiasts, and keep learning. "
        "We're all in this together! 💪 #CryptoMarket #TogetherWeGrow",
        
        # AI and crypto fusion
        "🤖 The fusion of AI and crypto is creating incredible opportunities! Autonomous agents, "
        "smart trading systems, and AI-powered communities are the future. "
        "We're not just investing in tokens - we're investing in the technology that will reshape the world! "
        "Exciting times ahead! 🌐 #AIandCrypto #FutureTech",
        
        # Community engagement
        "🤝 The best thing about crypto? The amazing people you meet! From developers to holders, "
        "everyone brings unique value to the ecosystem. Share knowledge, support each other, celebrate wins together. "
        "That's how we build a better crypto future for everyone! "
        "#CryptoCommunity #TogetherStronger",
        
        # Vision for future
        "🌈 Imagine a world where everyone has access to financial freedom. Where borders don't limit opportunity. "
        "Where communities can build wealth together. That's the crypto vision, and it's becoming reality! "
        "Every day we're one step closer. Keep believing, keep building! "
        "#CryptoVision #FinancialFreedom",
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
    
    if assigned_coin == "UNKNOWN" or assigned_coin == "EXAMPLE_COIN_1":
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
