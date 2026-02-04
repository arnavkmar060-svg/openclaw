import requests
import json
import time

# ═════════════════════════════════════════════════════════════════════════════
# 📡 MOLTBOOK REAL REGISTRAR (Live API Connection)
# ═════════════════════════════════════════════════════════════════════════════

AGENTS_LIST = [
    {
        "name": "Nemr_AI",
        "description": "Official AI Agent for Nemr2211 - Crypto Analyst", # تم تغيير bio إلى description حسب التوثيق
        "twitter": "https://x.com/Nemr2211"
    },
    {
        "name": "Adam_Bot_X",
        "description": "Technical Analysis & Chart Patterns Specialist",
        "twitter": "https://x.com/Adam2222x"
    },
    {
        "name": "Leader_55k",
        "description": "Market Operations & Community Growth Agent",
        "twitter": "https://x.com/Leader55000"
    },
    {
        "name": "Claude_747",
        "description": "Deep Learning & DeFi Research Agent",
        "twitter": "https://x.com/Claude747397"
    }
]

def register_agent_live(agent):
    print(f"\n📡 Connecting to LIVE Server for: {agent['name']}...")
    
    # 1. الرابط الحقيقي (Real Endpoint)
    url = "https://www.moltbook.com/api/v1/agents/register"
    
    # 2. البيانات بصيغة JSON الصحيحة
    payload = {
        "name": agent['name'],
        "description": agent['description']
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "MoltClient/1.0"
    }

    try:
        # إرسال الطلب الفعلي للسيرفر
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"   ⬅️ Server Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            
            # 3. تحليل الرد الحقيقي
            api_key = data.get("api_key")
            claim_token = data.get("claim_token")
            verification_code = data.get("verification_code")
            
            if api_key:
                print(f"🎉 SUCCESS! API Key Received Immediately.")
                print(f"🔑 KEY: {api_key}")
                save_key(agent['name'], api_key)
                
            elif claim_token or verification_code:
                # في حال طلب السيرفر التحقق عبر تويتر
                print("\n⚠️ SERVER REQUESTS VERIFICATION")
                print(f"The server returned a claim token: {claim_token or verification_code}")
                print(f"PLEASE TWEET THIS manually for {agent['name']}:")
                print(f"\nVerifying my AI agent {agent['name']} on @moltbook! Code: {claim_token or verification_code}\n")
                
                input("👉 After tweeting, press ENTER to continue (keys might be activated later)...")
                # قد تحتاج لحفظ الـ token لاستخدامه لاحقاً
                if api_key: 
                     save_key(agent['name'], api_key)
                else:
                     print("❌ No API key in response yet. Check your dashboard later.")

            else:
                # طباعة الرد الخام لفهم ما يريده السيرفر
                print(f"⚠️ Response content: {json.dumps(data, indent=2)}")
                
        else:
            print(f"❌ FAILED. Response: {response.text}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

def save_key(name, key):
    with open("final_real_keys.txt", "a") as f:
        f.write(f'"{key}", # {name}\n')
    print("💾 Key saved to 'final_real_keys.txt'")

if __name__ == "__main__":
    print("🚀 STARTING LIVE REGISTRATION...")
    for agent in AGENTS_LIST:
        register_agent_live(agent)
        time.sleep(2)
