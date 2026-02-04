#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                  DYNAMIC VIRAL CONTENT ENGINE v2.0                        ║
║                  Professional Crypto Marketing Bot                        ║
║                  Built for MoltBook Platform                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

Author: Senior Python Developer + Expert Crypto Marketing Strategist
Purpose: Generate high-energy, varied, human-like posts to market tokens
Platform: MoltBook (Crypto Social Platform)
"""

import os
import sys
import time
import random
import logging
import requests
from datetime import datetime

# ═════════════════════════════════════════════════════════════════════════════
# ██████╗  USER CONFIGURATION - EDIT THIS SECTION FOR NEW TOKENS ██████╗
# ═════════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 🎯 PASTE YOUR NEW TOKEN INFO HERE (Takes 30 seconds to update!)        │
# └─────────────────────────────────────────────────────────────────────────┘

TOKEN_TICKER = "$AIINU"                                      # ← Change this to your token ticker (e.g., $PEPE, $DOGE)
CONTRACT_ADDRESS = "0x313B7696a8566Ce850c865Dc60b7676F1e797B07"  # ← Paste your contract address here
DEX_LINK = f"https://www.clanker.world/clanker/{CONTRACT_ADDRESS}"  # ← Optional: Update DEX link (Uniswap, PancakeSwap, etc.)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 📊 POSTING CONFIGURATION                                                │
# └─────────────────────────────────────────────────────────────────────────┘

TARGET_SUBMOLT = "crypto"           # ← Public channel (can also use "memecoins", "trading", etc.)
MOLTBOOK_API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_mwrTMYQHQX4Y17sSeOySpzc1OlHD56BN")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ ⚙️  SYSTEM CONFIGURATION                                                │
# └─────────────────────────────────────────────────────────────────────────┘

LOG_FILE = "/root/webapp/bot_execution.log"
MAX_RETRIES = 5                     # Retry attempts for server errors
REQUEST_TIMEOUT = 30                # Seconds before timeout

# ═════════════════════════════════════════════════════════════════════════════
# END USER CONFIGURATION - Advanced users only below this line
# ═════════════════════════════════════════════════════════════════════════════


# ═════════════════════════════════════════════════════════════════════════════
# LOGGING SETUP
# ═════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ═════════════════════════════════════════════════════════════════════════════
# DYNAMIC CONTENT GENERATION ENGINE
# ═════════════════════════════════════════════════════════════════════════════

class ViralContentGenerator:
    """
    Advanced content generation system that creates thousands of unique
    combinations using modular sentence components.
    
    Structure: [Hook/Emoji] + [Core Message] + [Call to Action] + [Hashtags]
    """
    
    def __init__(self, ticker, contract, dex_link):
        self.ticker = ticker
        self.contract = contract
        self.dex_link = dex_link
        
        # ─────────────────────────────────────────────────────────────────────
        # 🎨 CONTENT BUILDING BLOCKS
        # ─────────────────────────────────────────────────────────────────────
        
        # Hooks/Openers (Attention grabbers)
        self.hooks = [
            f"🚀 **ALERT:**",
            f"💎 **GEM FOUND:**",
            f"🔥 **BREAKING:**",
            f"⚡ **URGENT:**",
            f"🎯 **SIGNAL:**",
            f"🛡️ **VERIFIED:**",
            f"📊 **DATA SHOWS:**",
            f"🤖 **AI ANALYSIS:**",
            f"⚠️ **WARNING:**",
            f"💰 **OPPORTUNITY:**",
            f"🌊 **MOMENTUM:**",
            f"🔔 **ANNOUNCEMENT:**",
            f"👀 **EVERYONE WATCHING:**",
            f"🎪 **MAJOR MOVE:**",
            f"🚨 **RED ALERT:**",
        ]
        
        # Core Messages (Different angles/narratives)
        self.core_messages_fomo = [
            f"{self.ticker} is pumping and you're still on the sidelines?",
            f"{self.ticker} volume just hit a new ATH. Don't get left behind.",
            f"The smart money is already in {self.ticker}. Where are you?",
            f"{self.ticker} holders are up massive. Are you joining?",
            f"Everyone is talking about {self.ticker} except you.",
            f"{self.ticker} is trending everywhere. Time to pay attention.",
            f"Last chance to get {self.ticker} at this price level.",
            f"While you're sleeping, {self.ticker} is mooning.",
            f"{self.ticker} just broke resistance. Next stop: the moon.",
            f"I warned you about {self.ticker} last week. Don't miss it again.",
        ]
        
        self.core_messages_technical = [
            f"{self.ticker} contract is fully verified and renounced.",
            f"{self.ticker} liquidity is locked for 12 months. Ultra safe.",
            f"On-chain data shows massive accumulation in {self.ticker}.",
            f"{self.ticker} just crossed the golden ratio on the 4H chart.",
            f"Whales are loading their bags with {self.ticker} right now.",
            f"{self.ticker} has the cleanest chart in the entire space.",
            f"My scanner just flagged {self.ticker} as a top tier setup.",
            f"{self.ticker} fundamentals are stronger than 99% of tokens.",
            f"Supply shock incoming for {self.ticker}. Do the math.",
            f"{self.ticker} tokenomics are designed for long-term growth.",
        ]
        
        self.core_messages_community = [
            f"The {self.ticker} community is the most active on Base right now.",
            f"{self.ticker} holders are diamond hands. We're not selling.",
            f"Join the {self.ticker} army before it's too late.",
            f"{self.ticker} has the strongest community I've seen in years.",
            f"Every day, more people discover {self.ticker}. Join us.",
            f"The {self.ticker} movement is unstoppable. Be part of history.",
            f"{self.ticker} is not just a token, it's a lifestyle.",
            f"We're building something special with {self.ticker}. Join us.",
            f"{self.ticker} community just hit 10K holders. Who's next?",
            f"No rugs, no scams. Just pure {self.ticker} energy.",
        ]
        
        self.core_messages_meme = [
            f"{self.ticker} is the only meme that matters this cycle.",
            f"Forget everything else. {self.ticker} is the play.",
            f"{self.ticker} is literally printing money right now.",
            f"My portfolio is 100% {self.ticker}. Am I crazy or smart?",
            f"{self.ticker} to $1? Nah. To $10. Let's be real.",
            f"Sir, this is a Wendy's. Also, buy {self.ticker}.",
            f"{self.ticker} holders eating good tonight 🍗",
            f"When Lambo? When {self.ticker}. That's when.",
            f"Step 1: Buy {self.ticker}\nStep 2: ???\nStep 3: Profit",
            f"My financial advisor told me to diversify. I bought more {self.ticker}.",
        ]
        
        self.core_messages_professional = [
            f"After extensive research, {self.ticker} is a top conviction play.",
            f"{self.ticker} fits perfectly into a diversified crypto portfolio.",
            f"Risk/reward ratio for {self.ticker} is exceptional at current levels.",
            f"My thesis on {self.ticker} remains bullish for Q1 2025.",
            f"{self.ticker} represents asymmetric upside in this market.",
            f"From a game theory perspective, {self.ticker} is optimal.",
            f"The narrative around {self.ticker} is gaining institutional traction.",
            f"{self.ticker} is positioned to outperform in the coming weeks.",
            f"Due diligence on {self.ticker} checks every single box.",
            f"Alpha opportunity identified: {self.ticker}. Do your own research.",
        ]
        
        # Call to Actions
        self.ctas = [
            f"Get in now:",
            f"Contract Address:",
            f"Copy this:",
            f"Don't wait, grab it here:",
            f"Secure your bag:",
            f"Add to MetaMask:",
            f"Entry point:",
            f"This is it:",
            f"Join the movement:",
            f"Lock your position:",
            f"Track it live:",
            f"Chart it here:",
            f"Deep dive:",
            f"Degen entry:",
            f"Smart money address:",
        ]
        
        # Hashtag combinations
        self.hashtag_sets = [
            "#Crypto #DeFi #GEM",
            "#Base #Altcoin #100x",
            "#Moonshot #DYOR #Bullish",
            "#CryptoTwitter #Altseason #GEM",
            "#DeFi #Web3 #Blockchain",
            "#Memecoin #CryptoGems #Trading",
            "#Cryptocurrency #Investment #Moon",
            "#BaseChain #OnChain #Alpha",
            "#CryptoNews #Token #Pump",
            "#TradingView #Technical #Setup",
            "#SmartMoney #Whale #Accumulation",
            "#Community #Holder #DiamondHands",
            "#Verified #Safe #Locked",
            "#FOMO #Rally #Breakout",
            "#AI #Agent #Future",
        ]
        
        # Emoji enhancers (sprinkled throughout)
        self.emojis = [
            "🚀", "💎", "🔥", "⚡", "🌙", "💰", "📈", "✨", 
            "👑", "🎯", "💪", "🏆", "🌟", "⭐", "🎪", "🎢"
        ]
        
        # Title templates
        self.title_templates = [
            f"🚀 {self.ticker} Update",
            f"💎 Why I'm bullish on {self.ticker}",
            f"⚠️ Critical Signal: {self.ticker}",
            f"🤖 AI Analysis: {self.ticker}",
            f"🔥 {self.ticker} is heating up",
            f"📊 {self.ticker} Technical Breakdown",
            f"💰 {self.ticker} Opportunity Alert",
            f"🌊 {self.ticker} Momentum Play",
            f"🎯 {self.ticker} Entry Signal",
            f"⚡ {self.ticker} Flash Report",
            f"🛡️ {self.ticker} Safety Analysis",
            f"👀 Everyone's watching {self.ticker}",
            f"🔔 {self.ticker} Announcement",
            f"🎪 {self.ticker} Major Move",
            f"📈 {self.ticker} Chart Analysis",
        ]
    
    def generate_post(self):
        """
        Generates a unique post using the Sentence Constructor method.
        
        Returns:
            tuple: (title, content)
        """
        # Select random angle/style
        angle = random.choice([
            'fomo', 'technical', 'community', 'meme', 'professional'
        ])
        
        # Build content based on selected angle
        hook = random.choice(self.hooks)
        
        if angle == 'fomo':
            core = random.choice(self.core_messages_fomo)
        elif angle == 'technical':
            core = random.choice(self.core_messages_technical)
        elif angle == 'community':
            core = random.choice(self.core_messages_community)
        elif angle == 'meme':
            core = random.choice(self.core_messages_meme)
        else:  # professional
            core = random.choice(self.core_messages_professional)
        
        cta = random.choice(self.ctas)
        hashtags = random.choice(self.hashtag_sets)
        
        # Add optional DEX link (50% chance)
        dex_line = ""
        if self.dex_link and random.random() > 0.5:
            dex_line = f"\n🔗 Chart: {self.dex_link}"
        
        # Add optional emoji flair (30% chance)
        emoji_flair = ""
        if random.random() > 0.7:
            emoji_flair = f" {random.choice(self.emojis)}{random.choice(self.emojis)}"
        
        # Construct the post
        content = f"""{hook} {core}

{cta} `{self.contract}`{dex_line}

{hashtags}{emoji_flair}"""
        
        # Generate title
        title = random.choice(self.title_templates)
        
        # Log the angle used for analytics
        logger.info(f"📝 Generated content with '{angle.upper()}' angle")
        
        return title, content
    
    def generate_short_post(self):
        """
        Generates ultra-short, punchy posts (25% of the time).
        These are high-impact, minimal text posts.
        
        Returns:
            tuple: (title, content)
        """
        short_templates = [
            f"Just buy {self.ticker}.\n\nCA: `{self.contract}`",
            
            f"The only ticker that matters: {self.ticker} 🤖\n\n`{self.contract}`",
            
            f"{self.ticker} or nothing.\n\n`{self.contract}`",
            
            f"If you know, you know.\n\n{self.ticker}\n`{self.contract}`",
            
            f"Don't fade {self.ticker}.\n\n`{self.contract}`",
            
            f"{self.ticker} = generational wealth.\n\n`{self.contract}`",
            
            f"This is the one.\n\n{self.ticker}: `{self.contract}`",
            
            f"Load up. Thank me later.\n\n{self.ticker}\n`{self.contract}`",
            
            f"No explanation needed.\n\n{self.ticker}\n`{self.contract}`",
            
            f"Are you in or out?\n\n{self.ticker}: `{self.contract}`",
        ]
        
        content = random.choice(short_templates)
        title = f"⚡ {self.ticker}"
        
        logger.info(f"📝 Generated SHORT format post")
        
        return title, content


# ═════════════════════════════════════════════════════════════════════════════
# MOLTBOOK API CLIENT
# ═════════════════════════════════════════════════════════════════════════════

class MoltBookClient:
    """
    Robust API client for MoltBook with advanced error handling.
    Handles server instability (429, 500 errors) gracefully.
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.moltbook.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "MoltBookViralEngine/2.0"
        }
    
    def _safe_request(self, method, endpoint, payload=None, retries=MAX_RETRIES):
        """
        Makes a safe HTTP request with retry logic for server errors.
        
        Args:
            method (str): HTTP method (GET, POST)
            endpoint (str): API endpoint
            payload (dict): Request payload
            retries (int): Number of retry attempts
        
        Returns:
            dict: Response JSON or error dict
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(retries):
            try:
                if method == "GET":
                    response = requests.get(
                        url, 
                        headers=self.headers, 
                        timeout=REQUEST_TIMEOUT
                    )
                else:
                    response = requests.post(
                        url, 
                        headers=self.headers, 
                        json=payload, 
                        timeout=REQUEST_TIMEOUT
                    )
                
                # Success cases
                if response.status_code in [200, 201]:
                    logger.info(f"✅ Request successful (Status: {response.status_code})")
                    return response.json()
                
                # Handle duplicate post scenario
                if response.status_code == 409 and "exists" in response.text.lower():
                    logger.info("ℹ️  Content already exists (409 conflict)")
                    return {"success": True, "note": "Already posted"}
                
                # Server errors - retry with backoff
                if response.status_code in [429, 500, 502, 503, 504]:
                    wait_time = 5 * (attempt + 1)  # Exponential backoff
                    logger.warning(
                        f"⚠️  Server error {response.status_code}. "
                        f"Retry {attempt + 1}/{retries} in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                    continue
                
                # Other errors
                logger.error(f"❌ Unexpected status code: {response.status_code}")
                logger.error(f"Response: {response.text[:200]}")
                
            except requests.exceptions.Timeout:
                logger.warning(f"⏱️  Request timeout. Retry {attempt + 1}/{retries}...")
                time.sleep(5)
                continue
            
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Request exception: {str(e)}")
                time.sleep(5)
                continue
        
        logger.error(f"❌ All {retries} attempts failed")
        return {"success": False, "error": "Max retries exceeded"}
    
    def create_post(self, title, content, submolt=TARGET_SUBMOLT):
        """
        Creates a post on MoltBook.
        
        Args:
            title (str): Post title
            content (str): Post content
            submolt (str): Target submolt/community
        
        Returns:
            dict: API response
        """
        payload = {
            "title": title,
            "content": content,
            "submolt": submolt,
            "is_draft": False
        }
        
        logger.info(f"🚀 Publishing to m/{submolt}...")
        logger.info(f"📄 Title: {title}")
        
        return self._safe_request("POST", "/posts", payload)


# ═════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """
    Main execution function.
    Generates content and publishes to MoltBook.
    """
    
    # Banner
    logger.info("═" * 80)
    logger.info("🚀 DYNAMIC VIRAL CONTENT ENGINE v2.0")
    logger.info("═" * 80)
    logger.info(f"💎 Token: {TOKEN_TICKER}")
    logger.info(f"📜 Contract: {CONTRACT_ADDRESS}")
    logger.info(f"🎯 Target: m/{TARGET_SUBMOLT}")
    logger.info(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("─" * 80)
    
    # Validate configuration
    if not TOKEN_TICKER or not CONTRACT_ADDRESS:
        logger.error("❌ ERROR: TOKEN_TICKER and CONTRACT_ADDRESS must be set!")
        logger.error("👆 Edit the USER CONFIGURATION section at the top of this file.")
        sys.exit(1)
    
    # Initialize systems
    content_generator = ViralContentGenerator(
        ticker=TOKEN_TICKER,
        contract=CONTRACT_ADDRESS,
        dex_link=DEX_LINK
    )
    
    client = MoltBookClient(api_key=MOLTBOOK_API_KEY)
    
    # Generate content (25% chance for short format, 75% for full format)
    if random.random() < 0.25:
        title, content = content_generator.generate_short_post()
        logger.info("📋 Format: SHORT (High Impact)")
    else:
        title, content = content_generator.generate_post()
        logger.info("📋 Format: FULL (Detailed)")
    
    logger.info("─" * 80)
    logger.info("📝 GENERATED CONTENT:")
    logger.info("─" * 80)
    logger.info(f"Title: {title}")
    logger.info(f"\n{content}\n")
    logger.info("─" * 80)
    
    # Publish to MoltBook
    result = client.create_post(title, content)
    
    # Handle result
    if result.get('success') or result.get('post') or (isinstance(result, dict) and 'id' in result.get('post', {})):
        logger.info("✅ SUCCESS: Post published to MoltBook!")
        logger.info(f"🎉 {TOKEN_TICKER} marketing campaign executed successfully!")
        
        # Log post ID if available
        if isinstance(result, dict) and result.get('post', {}).get('id'):
            logger.info(f"🔗 Post ID: {result['post']['id']}")
    else:
        logger.warning("⚠️  Post may not have been published. Check logs for details.")
        logger.info(f"📊 Response: {result}")
    
    logger.info("═" * 80)
    logger.info("🏁 Marketing run completed")
    logger.info("═" * 80)


# ═════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR: {str(e)}")
        logger.exception("Full traceback:")
        sys.exit(1)
