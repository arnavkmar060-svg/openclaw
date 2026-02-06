import requests
import json
import random
import logging
import os
import time
from datetime import datetime

# ═════════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION & TEAM ROSTER
# ═════════════════════════════════════════════════════════════════════════════

# اسم العملة وعنوانها
TOKEN_TICKER = "$AIINU"
CONTRACT_ADDRESS = "0x313B7696a8566Ce850c865Dc60b7676F1e797B07"

# قائمة الوكلاء (الفريق)
# ملاحظة: حالياً نمر فقط مفعل. سنضيف البقية غداً بعد السماح بالتسجيل.
TEAM_ROSTER = [
    {
        "name": "Nemr_AI",
        "api_key": "moltbook_sk_c1f0hM1mYPXxgaJgXadTFjB95ofK5xhv", # ✅ مفتاح حقيقي
        "style": "Hype Leader",
        "instructions": "Write a short, high-energy tweet about $AIINU. Use fire emojis. Say 'We are early'.",
        "hashtags": "#LFG #Gem #Base"
    }
    # { "name": "Adam_Bot", "api_key": "PLACEHOLDER_FOR_TOMORROW", ... },
    # { "name": "Leader_55k", "api_key": "PLACEHOLDER_FOR_TOMORROW", ... },
]

# ملف حفظ الدور
STATE_FILE = "/root/webapp/rotation_state.json"

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/root/webapp/bot_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ViralEngine")

# ═════════════════════════════════════════════════════════════════════════════
# 📡 MOLTBOOK CLIENT (كلاس الاتصال بالسيرفر)
# ═════════════════════════════════════════════════════════════════════════════
class MoltbookClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.moltbook.com/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-Agent-Key": self.api_key
        }

    def create_post(self, title, content):
        url = f"{self.base_url}/posts"
        payload = {
            "title": title,
            "content": content,
            "submolt": "crypto",  # النشر في قسم الكريبتو
            "tags": ["crypto", "memecoin", "base"]
        }
        
        try:
            logger.info(f"📡 Sending post to Moltbook...")
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ POST SUCCESS! ID: {response.json().get('id', 'Unknown')}")
                return True
            else:
                logger.error(f"❌ POST FAILED. Status: {response.status_code} | Msg: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ CONNECTION ERROR: {e}")
            return False

# ═════════════════════════════════════════════════════════════════════════════
# 🧠 LOGIC: ROTATION & CONTENT
# ═════════════════════════════════════════════════════════════════════════════

def get_next_agent():
    """اختيار الوكيل التالي في القائمة"""
    current_index = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                current_index = data.get('last_index', -1) + 1
        except:
            current_index = 0
    
    # إعادة التدوير إذا وصلنا للنهاية
    if current_index >= len(TEAM_ROSTER):
        current_index = 0
    
    # حفظ الحالة الجديدة
    with open(STATE_FILE, 'w') as f:
        json.dump({'last_index': current_index}, f)
        
    return TEAM_ROSTER[current_index]

class ContentGenerator:
    """توليد محتوى بسيط (سيتم ربطه بـ Gemini لاحقاً)"""
    def generate(self, agent):
        # قوالب جاهزة للتجربة الفورية
        templates = [
            f"🚀 {TOKEN_TICKER} is heating up on Base chain! The community is growing fast. {agent['hashtags']}",
            f"💎 Found a gem: {TOKEN_TICKER}. Contract: {CONTRACT_ADDRESS}. Don't miss this one! {agent['hashtags']}",
            f"👀 Whales are watching {TOKEN_TICKER}. Accumulation phase seems to be starting. {agent['hashtags']}",
            f"🔥 {agent['style']} Update: We are building something huge with {TOKEN_TICKER}. Join us! {agent['hashtags']}"
        ]
        content = random.choice(templates)
        title = f"{agent['name']} Market Update"
        return title, content

# ═════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN EXECUTION
# ═════════════════════════════════════════════════════════════════════════════
def main():
    logger.info("="*50)
    logger.info("🚀 STARTING VIRAL ENGINE SESSION")
    
    # 1. تحديد من عليه الدور
    agent = get_next_agent()
    logger.info(f"👤 Active Agent: {agent['name']} ({agent['style']})")
    
    if "PLACEHOLDER" in agent['api_key']:
        logger.warning("⚠️ This agent is not ready yet. Skipping...")
        return

    # 2. توليد المحتوى
    generator = ContentGenerator()
    title, content = generator.generate(agent)
    logger.info(f"📝 Content Prepared: {content[:40]}...")

    # 3. النشر
    client = MoltbookClient(agent['api_key'])
    success = client.create_post(title, content)
    
    if success:
        logger.info(f"🎉 CYCLE COMPLETE for {agent['name']}")
    else:
        logger.error("⚠️ CYCLE FAILED")
        
    logger.info("="*50)

if __name__ == "__main__":
    main()
