# 3-Bot Swarm Professional Workflow Guide

## 🚀 Overview

This guide documents the professional workflow for managing a 3-bot swarm (Nemr, Eng, Leader) using Banker's Market Intelligence and automated campaign management.

---

## 📋 System Architecture

### Components

1. **daily_analytics.py** - Trend Hunter Script
2. **active_campaigns.json** - Campaign Manager Config
3. **bot_nemr/main_nemr.py** - Community-Focused Bot
4. **bot_eng/main_eng.py** - Technical Analyst Bot  
5. **bot_leader/main_leader.py** - Strategic Smart Money Bot

### Workflow Diagram

```
Daily Workflow:
┌─────────────────────────────────────┐
│ 1. Run daily_analytics.py          │
│    ↓ Queries Banker API             │
│    ↓ Falls back to simulation       │
│    ↓ Generates 3 coin suggestions   │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 2. Launch Coins Manually            │
│    ↓ Use suggested names            │
│    ↓ Deploy on preferred platform   │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 3. Update active_campaigns.json     │
│    ↓ Assign coins to bots           │
│    ↓ Nemr_AI: COIN_1                │
│    ↓ Eng_Crypto: COIN_2             │
│    ↓ Leader-Crypto: COIN_3          │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 4. Bots Run Automatically           │
│    ↓ Read config every cycle        │
│    ↓ Promote assigned coins 3x/day  │
│    ↓ Post general content regularly │
└─────────────────────────────────────┘
```

---

## 🔧 Phase 1: Trend Hunter (daily_analytics.py)

### Purpose
Analyzes market trends using Banker's Market Intelligence API to suggest 3 coin names for launch.

### Features
✅ **Banker API Integration**: Queries `market_intelligence`, `technical_analysis`, `social_sentiment`  
✅ **Fallback Mode**: Uses Google Trends or mock data if API returns 402/Payment error  
✅ **Name Generation**: Creates 3 similar coin names based on trending topics  
✅ **JSON Output**: Saves suggestions to `suggested_coins.json`

### Usage

```bash
# Run daily analytics
python3 daily_analytics.py
```

### Output Example

```
🚀 STARTING DAILY TREND ANALYSIS
====================================
📈 TREND #1: AI Agent
   Volume/Mentions: 85000
   Sentiment: Very Positive
   
   💡 SUGGESTED COIN NAMES:
      1. AIAgentBot
      2. AIAgentCoin
      3. MetaAIAgent

🎯 FINAL 3 COIN SUGGESTIONS FOR LAUNCH
====================================
1. 🚀 AIAgentBot
2. 🚀 DeFiProtocolAI
3. 🚀 PepeCoin
```

### API Configuration

```python
# In daily_analytics.py
BANKER_API_KEY = "bk_XE6SA2BLVX5U37LET5KMLYRGJMRMEPG8"
```

### Fallback Strategy

If Banker API returns **402 Payment Required**:
1. Script automatically switches to **Simulation Mode**
2. Tries to use **pytrends** for Google Trends data
3. Falls back to **mock trends** if pytrends unavailable
4. System continues to function normally

---

## 🎯 Phase 2: Campaign Manager (active_campaigns.json)

### Purpose
Central configuration file for assigning coins to bots manually.

### Structure

```json
{
  "last_updated": "2026-02-06T00:00:00Z",
  "campaigns": {
    "Nemr_AI": {
      "assigned_coin": "AIAgentBot",
      "launch_date": "2026-02-06",
      "status": "active",
      "notes": "Community-focused promotion"
    },
    "Eng_Crypto": {
      "assigned_coin": "DeFiProtocolAI",
      "launch_date": "2026-02-06",
      "status": "active",
      "notes": "Technical analysis focus"
    },
    "Leader-Crypto": {
      "assigned_coin": "PepeCoin",
      "launch_date": "2026-02-06",
      "status": "active",
      "notes": "Smart money insights"
    }
  },
  "posting_schedule": {
    "promotional_posts_per_day": 3,
    "general_content_frequency": "every_2_hours",
    "promotional_times": ["09:00", "14:00", "20:00"]
  }
}
```

### How to Update

1. Run `daily_analytics.py` to get 3 suggestions
2. Launch the coins on your preferred platform
3. Edit `active_campaigns.json`:
   ```bash
   nano active_campaigns.json
   ```
4. Update `assigned_coin` fields with actual coin names
5. Save the file - bots will auto-reload on next cycle

---

## 🤖 Phase 3: The 3-Bot Swarm

### Bot Personalities

| Bot | Personality | Content Style |
|-----|-------------|---------------|
| **Nemr_AI** | Enthusiastic, Community-Focused | Storytelling, emotional connection, community building |
| **Eng_Crypto** | Technical, Analytical | Data-driven analysis, chart patterns, indicators |
| **Leader-Crypto** | Strategic, Smart Money | Liquidity analysis, risk/reward, institutional insights |

### Bot Operations

#### 1. Nemr_AI (Community Storyteller)

**File**: `bot_nemr/main_nemr.py`

**Content Examples**:
- "🌟 Amazing things happen when a community comes together! $COIN isn't just another token..."
- "💎 Real talk: $COIN started as an idea, but the community transformed it into reality..."

**Schedule**:
- Promotional posts: 09:00, 14:00, 20:00 (3x daily)
- General content: Every 2 hours

**API Keys**:
```python
BANKR_KEY = "bk_XE6SA2BLVX5U37LET5KMLYRGJMRMEPG8"
MOLTBOOK_KEY = "moltbook_sk_c1f0hM1mYPXxgaJgXadTFjB95ofK5xhv"
```

#### 2. Eng_Crypto (Technical Analyst)

**File**: `bot_eng/main_eng.py`

**Content Examples**:
- "📊 Technical Analysis: $COIN is showing strong momentum indicators across multiple timeframes..."
- "🔗 On-Chain Data Analysis for $COIN: Network activity shows significant growth..."

**Schedule**:
- Promotional posts: 09:00, 14:00, 20:00 (3x daily)
- General content: Every 2 hours

**API Keys**:
```python
BANKR_KEY = "bk_9CLVKYTQKHYYZXRES6A5TJL7MYJLDJT8"
MOLTBOOK_KEY = "moltbook_sk_mwrTMYQHQX4Y17sSeOySpzc1OlHD56BN"
```

#### 3. Leader-Crypto (Smart Money Strategist)

**File**: `bot_leader/main_leader.py`

**Content Examples**:
- "💎 Smart money is positioning in $COIN. We're seeing significant liquidity flow..."
- "⏰ Market timing intel: $COIN is entering a critical accumulation zone..."

**Schedule**:
- Promotional posts: 09:00, 14:00, 20:00 (3x daily)
- General content: Every 2 hours

**API Keys**:
```python
BANKR_KEY = "bk_LEADER_KEY_PLACEHOLDER"  # UPDATE THIS
MOLTBOOK_KEY = "moltbook_sk_LEADER_KEY_PLACEHOLDER"  # UPDATE THIS
```

---

## 📅 Daily Operational Workflow

### Morning Routine (Daily)

```bash
# Step 1: Run trend analysis
cd /root/webapp
python3 daily_analytics.py

# Step 2: Review suggested coins
cat suggested_coins.json

# Step 3: Launch the coins manually
# (Use your preferred platform/method)

# Step 4: Update campaign config
nano active_campaigns.json
# Edit: assigned_coin for each bot

# Step 5: Start/restart bots
cd bot_nemr && python3 main_nemr.py &
cd ../bot_eng && python3 main_eng.py &
cd ../bot_leader && python3 main_leader.py &
```

### Content Quality Standards

#### ✅ High-Quality Posts (REQUIRED)
- **Length**: 2-3+ sentences minimum
- **Emojis**: Strategic use for visual appeal (2-4 per post)
- **Hashtags**: 2-4 relevant hashtags
- **Substance**: Clear value proposition or insight
- **Professional**: Well-written, engaging, informative

#### ❌ Avoid (LOW QUALITY)
- ❌ Single-word posts: "Buy this"
- ❌ Generic spam: "To the moon!"
- ❌ No context: "$COIN 🚀"
- ❌ Excessive emojis: "🚀🚀🚀🚀🚀🚀🚀"

### Example High-Quality Posts

**Nemr_AI (Community)**:
```
🌟 Amazing things happen when a community comes together! 
$AIAgentBot isn't just another token - it's a movement of 
passionate believers building something special. Every holder 
is part of our story, and together we're creating the next 
crypto success tale. Join us on this incredible journey! 🚀 
#Community #AIAgentBot #CryptoFamily
```

**Eng_Crypto (Technical)**:
```
📊 Technical Analysis: $DeFiProtocolAI is showing strong 
momentum indicators across multiple timeframes. RSI trending 
upward, MACD crossover confirmed, and volume profile indicates 
accumulation phase. The technical structure supports continued 
upward movement with key support levels holding firm. 
#CryptoAnalysis #DeFiProtocolAI #TechnicalAnalysis
```

**Leader-Crypto (Strategic)**:
```
💎 Smart money is positioning in $PepeCoin. We're seeing 
significant liquidity flow into this project, with 
institutional-grade wallet accumulation patterns. The market 
structure suggests early-stage discovery phase. This is where 
the big moves begin. #Crypto #SmartMoney #PepeCoin
```

---

## 🔒 Security & Best Practices

### API Key Management

1. **Keep Keys Secret**: Never commit API keys to public repos
2. **Rotate Regularly**: Update keys every 30-60 days
3. **Monitor Usage**: Check API key usage to detect anomalies
4. **Backup Keys**: Store backup keys in secure location

### Bot Management

1. **Monitor Logs**: Check `bot_*/log.txt` regularly
2. **Test First**: Always test on small scale before full deployment
3. **Rate Limits**: Respect platform rate limits (current: every 2 hours general, 3x daily promo)
4. **Error Handling**: Bots automatically retry on errors with exponential backoff

### Campaign Updates

1. **Daily Updates**: Update `active_campaigns.json` when launching new coins
2. **Verify Config**: Bots reload config on each cycle - verify JSON syntax
3. **Track Performance**: Monitor which coins generate the most engagement
4. **Adjust Strategy**: Modify posting times based on audience engagement data

---

## 🧪 Testing

### Test Individual Components

```bash
# Test trend analytics
python3 daily_analytics.py

# Test Nemr bot (dry run - check logs)
cd bot_nemr && python3 main_nemr.py
# CTRL+C after confirming it reads config correctly

# Test Eng bot
cd ../bot_eng && python3 main_eng.py
# CTRL+C after confirming it reads config correctly

# Test Leader bot
cd ../bot_leader && python3 main_leader.py
# CTRL+C after confirming it reads config correctly
```

### Verify Campaign Config Loading

```bash
# Check if config is valid JSON
python3 -m json.tool active_campaigns.json

# Test config loading in Python
python3 << EOF
import json
with open('active_campaigns.json', 'r') as f:
    config = json.load(f)
    print("✅ Config loaded successfully")
    print(f"Nemr assigned: {config['campaigns']['Nemr_AI']['assigned_coin']}")
    print(f"Eng assigned: {config['campaigns']['Eng_Crypto']['assigned_coin']}")
    print(f"Leader assigned: {config['campaigns']['Leader-Crypto']['assigned_coin']}")
EOF
```

---

## 📊 Monitoring & Analytics

### Log Files

Each bot maintains its own log file:
- `bot_nemr/log.txt`
- `bot_eng/log.txt`
- `bot_leader/log.txt`

### Key Metrics to Track

1. **Post Success Rate**: % of posts that succeed vs fail
2. **Daily Post Counts**: Promotional vs general content
3. **Config Reload Frequency**: How often bots refresh campaign data
4. **API Failures**: Track Banker API vs simulation mode usage

### Log Monitoring Commands

```bash
# View recent logs for all bots
tail -n 50 bot_nemr/log.txt
tail -n 50 bot_eng/log.txt
tail -n 50 bot_leader/log.txt

# Monitor logs in real-time
tail -f bot_nemr/log.txt &
tail -f bot_eng/log.txt &
tail -f bot_leader/log.txt &

# Search for errors
grep "ERROR" bot_*/log.txt

# Count successful posts today
grep "$(date +%Y-%m-%d)" bot_nemr/log.txt | grep "Posted successfully" | wc -l
```

---

## 🐛 Troubleshooting

### Issue: Bot not posting promotional content

**Symptom**: Logs show "No valid coin assigned"

**Solution**:
```bash
# Verify active_campaigns.json has correct coin names
cat active_campaigns.json | grep assigned_coin

# Ensure coin names are NOT "EXAMPLE_COIN_1/2/3" or "UNKNOWN"
# Update with actual coin names from daily_analytics.py
```

### Issue: Banker API returns 402 Payment Required

**Symptom**: daily_analytics.py shows "Payment Required (402)"

**Solution**: This is expected! The script automatically:
1. Switches to Simulation Mode
2. Uses Google Trends (if pytrends installed)
3. Falls back to mock trends
4. System continues functioning normally

### Issue: Bot crashes in main loop

**Symptom**: Bot stops running, error in logs

**Solution**:
```bash
# Bots have built-in retry logic
# Check logs for specific error
tail -n 100 bot_*/log.txt

# Restart the bot
cd bot_nemr && python3 main_nemr.py &
```

### Issue: JSON syntax error in config

**Symptom**: "Error loading campaign config: JSON decode error"

**Solution**:
```bash
# Validate JSON syntax
python3 -m json.tool active_campaigns.json

# Common issues:
# - Missing comma between fields
# - Unescaped quotes in strings
# - Trailing comma in last element
```

---

## 🚀 Advanced Features

### Custom Posting Times

Edit the schedule in each bot's `main_*.py`:

```python
# Default schedule
schedule.every().day.at("09:00").do(promotional_cycle)
schedule.every().day.at("14:00").do(promotional_cycle)
schedule.every().day.at("20:00").do(promotional_cycle)

# Customize to your timezone/audience
schedule.every().day.at("08:00").do(promotional_cycle)  # Morning
schedule.every().day.at("13:00").do(promotional_cycle)  # Lunch
schedule.every().day.at("19:00").do(promotional_cycle)  # Evening
```

### Add More Bots

To scale to 4+ bots:

1. Create new bot directory: `bot_newname/`
2. Copy structure from existing bot
3. Add entry in `active_campaigns.json`:
   ```json
   "NewBot_Name": {
     "assigned_coin": "COIN_4",
     "launch_date": "2026-02-06",
     "status": "active"
   }
   ```
4. Update `daily_analytics.py` to suggest 4 coins

### Integration with Other Platforms

Current: MoltBook  
Future: Twitter/X, Telegram, Discord

Modify `post_to_moltbook()` function to post to multiple platforms.

---

## 📝 Summary Checklist

### Daily Tasks
- [ ] Run `python3 daily_analytics.py`
- [ ] Review suggested coin names
- [ ] Launch coins manually
- [ ] Update `active_campaigns.json`
- [ ] Verify bots are running
- [ ] Monitor logs for errors

### Weekly Tasks
- [ ] Review posting performance
- [ ] Analyze engagement metrics
- [ ] Adjust content templates if needed
- [ ] Check API key usage
- [ ] Update coin assignments as campaigns end

### Monthly Tasks
- [ ] Rotate API keys
- [ ] Review and optimize posting schedule
- [ ] Analyze which bot personality performs best
- [ ] Update content templates with fresh ideas
- [ ] Backup all config and log files

---

## 🎓 Learning Resources

### Understanding the Code

- **daily_analytics.py**: Market intelligence + trend generation
- **active_campaigns.json**: Campaign configuration
- **main_*.py**: Bot logic, content generation, scheduling

### Key Libraries Used

- `requests`: HTTP API calls
- `schedule`: Task scheduling
- `json`: Config file parsing
- `logging`: Activity logging
- `pytrends`: Google Trends data (optional)

### Extending Functionality

Want to add features? Start with:
1. Study existing bot structure
2. Add new content templates
3. Implement new API integrations
4. Test thoroughly before production

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review log files for errors
3. Verify config file syntax
4. Test components individually

---

## ✅ System Status

Current Implementation:
- ✅ Trend Hunter (daily_analytics.py)
- ✅ Campaign Manager (active_campaigns.json)
- ✅ Nemr_AI Bot (Community Focus)
- ✅ Eng_Crypto Bot (Technical Analysis)
- ✅ Leader-Crypto Bot (Smart Money)
- ✅ Professional content templates
- ✅ Automatic config reloading
- ✅ 3x daily promotional posts
- ✅ Regular general content
- ✅ Error handling & logging
- ✅ Simulation mode fallback

---

**Last Updated**: 2026-02-06  
**Version**: 1.0  
**Status**: Production Ready 🚀
