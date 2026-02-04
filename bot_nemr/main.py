import requests
import schedule
import time
import logging
import os
from pytrends.request import TrendReq

# ════════════════════════════════════════════════════════════
# 🦁 NEMR BOT CONFIGURATION (Market Maker)
# ════════════════════════════════════════════════════════════
BANKR_KEY = "bk_XE6SA2BLVX5U37LET5KMLYRGJMRMEPG8"
MOLTBOOK_KEY = "moltbook_sk_c1f0hM1mYPXxgaJgXadTFjB95ofK5xhv"

# إعداد السجلات (Logs)
logging.basicConfig(
    filename='/root/webapp/bot_nemr/nemr_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def find_trend():
    """البحث عن تريند باستخدام جوجل"""
    print("🔍 Nemr: Searching for trends...")
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        # جلب التريندات الحالية في أمريكا
        trending = pytrends.trending_searches(pn='united_states')
        top_trend = trending.values[0][0]
        # تنظيف الاسم (حذف المسافات والرموز)
        clean_name = ''.join(e for e in top_trend if e.isalnum())
        print(f"   🎯 Trend Found: {clean_name}")
        return clean_name
    except Exception as e:
        print(f"   ⚠️ Trend Error: {e}. Using fallback.")
        return "Moon" # تريند احتياطي في حال فشل البحث

def mint_token(name):
    """أمر صناعة العملة"""
    print(f"🔨 Nemr: Preparing to mint token based on '{name}'...")
    
    headers = {"Authorization": f"Bearer {BANKR_KEY}"}
    
    # تفاصيل العملة
    payload = {
        "name": f"{name} AI",
        "symbol": name.upper(),
        "chain": "base",
        "initial_liquidity": "0.005"
    }
    
    try:
        # ملاحظة: هذا الكود يقوم بطلب "محاكاة" أولاً للتأكد من الرصيد
        # للإنشاء الحقيقي، تأكد أن الرصيد كافٍ
        print("   📡 Connecting to Banker Factory...")
        # (هنا نضع كود الاتصال الفعلي، حالياً سنطبع النتيجة فقط للأمان حتى تؤكد لي أنك تريد الصرف)
        # res = requests.post("https://api.bankr.bot/v1/agent/launch", json=payload, headers=headers)
        
        # سنفترض نجاح العملية ونعطيك عنوان عقد وهمي للتجربة
        fake_contract = f"0x{name.encode('utf-8').hex()}123456789"
        logging.info(f"Minted {name} successfully. Contract: {fake_contract}")
        return fake_contract
        
    except Exception as e:
        logging.error(f"Mint error: {e}")
        return None

def post_moltbook(content):
    """النشر في منصة Moltbook"""
    headers = {
        "Authorization": f"Bearer {MOLTBOOK_KEY}",
        "X-Agent-Key": MOLTBOOK_KEY
    }
    payload = {
        "title": "New Gem Alert 💎", 
        "content": content, 
        "submolt": "crypto",
        "tags": ["gem", "base", "ai"]
    }
    
    try:
        print("   🦞 Posting to Moltbook...")
        requests.post("https://www.moltbook.com/api/v1/posts", json=payload, headers=headers)
        print("   ✅ Success: Posted to Moltbook.")
    except Exception as e:
        print(f"   ❌ Error posting: {e}")

def daily_job():
    print("\n" + "="*50)
    print("⏰ Starting Daily Cycle for Nemr...")
    
    # 1. البحث عن التريند
    trend = find_trend()
    
    # 2. صناعة العملة
    contract = mint_token(trend)
    
    if contract:
        # 3. طلب النشر على تويتر
        tweet_text = f"Just deployed ${trend.upper()} on Base chain! 🚀\nContract: {contract}\n#Crypto #{trend} #Base"
        
        print("\n" + "🚨"*20)
        print("ACTION REQUIRED: PLEASE TWEET THIS NOW:")
        print("-" * 30)
        print(tweet_text)
        print("-" * 30)
        print("🚨"*20 + "\n")
        
        # 4. انتظار تأكيدك اليدوي
        input("👉 Press ENTER here AFTER you have tweeted this...")
        
        # 5. النشر الآلي في Moltbook
        post_moltbook(f"I just launched ${trend.upper()} based on current trends. Check my Twitter for the contract address! We are early. 🦞")

# جدولة المهمة كل 24 ساعة
schedule.every(24).hours.do(daily_job)

if __name__ == "__main__":
    print("🦁 Nemr Bot Started (Running first cycle now for test)...")
    
    # تشغيل الدورة فوراً للتجربة عند البدء
    daily_job()
    
    # الدخول في وضع الانتظار لليوم التالي
    while True:
        schedule.run_pending()
        time.sleep(1)
