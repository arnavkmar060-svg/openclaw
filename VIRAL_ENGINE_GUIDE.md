# 🚀 Dynamic Viral Content Engine v2.0 - Complete Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Configuration Guide](#configuration-guide)
3. [Content Generation System](#content-generation-system)
4. [Running the Bot](#running-the-bot)
5. [Advanced Features](#advanced-features)
6. [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

### Step 1: Update Token Information (30 seconds)

Open `dynamic_viral_engine.py` and find the **USER CONFIGURATION** section at the top:

```python
# ═════════════════════════════════════════════════════════════════════════════
# ██████╗  USER CONFIGURATION - EDIT THIS SECTION FOR NEW TOKENS ██████╗
# ═════════════════════════════════════════════════════════════════════════════

TOKEN_TICKER = "$AIINU"                                      # ← Change this
CONTRACT_ADDRESS = "0x313B7696a8566Ce850c865Dc60b7676F1e797B07"  # ← Paste here
DEX_LINK = f"https://www.clanker.world/clanker/{CONTRACT_ADDRESS}"  # ← Update if needed
```

### Step 2: Run the Script

```bash
cd /root/webapp
python3 dynamic_viral_engine.py
```

That's it! The bot will generate and post unique content to MoltBook.

---

## 🎯 Configuration Guide

### Required Settings

| Variable | Description | Example |
|----------|-------------|---------|
| `TOKEN_TICKER` | Your token symbol (include $) | `$PEPE`, `$DOGE`, `$SHIB` |
| `CONTRACT_ADDRESS` | Full contract address | `0x123...abc` |
| `DEX_LINK` | Link to chart/DEX (optional) | Uniswap, PancakeSwap, Clanker |

### Optional Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `TARGET_SUBMOLT` | Public channel to post in | `crypto` |
| `MAX_RETRIES` | Server error retry attempts | `5` |
| `REQUEST_TIMEOUT` | HTTP timeout (seconds) | `30` |

### API Key

The bot uses the environment variable `MOLTBOOK_API_KEY` or falls back to the hardcoded key:

```python
MOLTBOOK_API_KEY = os.environ.get("MOLTBOOK_API_KEY", "your_key_here")
```

**Recommended:** Set as environment variable:
```bash
export MOLTBOOK_API_KEY="moltbook_sk_your_key_here"
```

---

## 🎨 Content Generation System

### The Sentence Constructor Method

The bot uses a **modular approach** to create thousands of unique combinations:

```
[Hook/Emoji] + [Core Message] + [Call to Action] + [Hashtags]
```

### Content Angles (Automatic Variation)

The bot randomly selects from 5 different marketing angles:

#### 1. 🔥 FOMO Angle (Urgency)
- Creates fear of missing out
- Emphasizes price action and momentum
- Example: *"$TOKEN is pumping and you're still on the sidelines?"*

#### 2. 📊 Technical Angle (Trust)
- Focuses on contract security
- Highlights verified audits
- Example: *"$TOKEN contract is fully verified and renounced."*

#### 3. 🤝 Community Angle (Social Proof)
- Emphasizes growing holder base
- Builds tribe mentality
- Example: *"The $TOKEN community is the most active on Base right now."*

#### 4. 😂 Meme Angle (Entertainment)
- Uses humor and crypto slang
- Relatable and shareable
- Example: *"My financial advisor told me to diversify. I bought more $TOKEN."*

#### 5. 💼 Professional Angle (Credibility)
- Sophisticated language
- Analytical approach
- Example: *"After extensive research, $TOKEN is a top conviction play."*

### Content Formats

**Full Format (75% of posts):**
- Detailed multi-line post
- Includes hook, core message, CTA, contract, hashtags
- Average length: 100-150 characters

**Short Format (25% of posts):**
- Ultra-punchy one-liner
- Minimal text, maximum impact
- Average length: 30-50 characters

### Content Library Size

**Total Unique Combinations:**
- **15 Hooks** × **50 Core Messages** × **15 CTAs** × **15 Hashtag Sets** = **~168,750 unique posts**
- Plus **10 short format templates** = **168,760 total variations**

**You can run this bot for MONTHS without repeating the same post!**

---

## 🤖 Running the Bot

### Manual Execution

```bash
cd /root/webapp
python3 dynamic_viral_engine.py
```

### Automated Scheduling (Recommended)

#### Option 1: Cron Job (Every 4 hours)

```bash
# Edit crontab
crontab -e

# Add this line (runs at 00:00, 04:00, 08:00, 12:00, 16:00, 20:00)
0 */4 * * * cd /root/webapp && python3 dynamic_viral_engine.py >> /root/webapp/cron.log 2>&1
```

#### Option 2: Systemd Timer (More reliable)

Create `/etc/systemd/system/viral-engine.service`:

```ini
[Unit]
Description=Dynamic Viral Content Engine
After=network.target

[Service]
Type=oneshot
User=root
WorkingDirectory=/root/webapp
ExecStart=/usr/bin/python3 /root/webapp/dynamic_viral_engine.py
StandardOutput=append:/root/webapp/bot_execution.log
StandardError=append:/root/webapp/bot_execution.log

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/viral-engine.timer`:

```ini
[Unit]
Description=Run Viral Engine every 4 hours

[Timer]
OnBootSec=5min
OnUnitActiveSec=4h

[Install]
WantedBy=timers.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable viral-engine.timer
sudo systemctl start viral-engine.timer
```

Check status:

```bash
sudo systemctl status viral-engine.timer
```

---

## 🎛️ Advanced Features

### Custom Content Pools

You can extend the content library by editing these lists in the `ViralContentGenerator` class:

```python
# Add your own hooks
self.hooks = [
    f"🚀 **ALERT:**",
    f"💎 **GEM FOUND:**",
    # Add more here...
]

# Add your own core messages
self.core_messages_fomo = [
    f"{self.ticker} is pumping...",
    # Add more here...
]
```

### Error Handling Features

The bot includes robust error handling:

- ✅ **Retry Logic**: Automatically retries failed requests 5 times
- ✅ **Exponential Backoff**: Waits longer between each retry (5s, 10s, 15s, 20s, 25s)
- ✅ **Timeout Protection**: 30-second timeout prevents hanging
- ✅ **Server Error Detection**: Handles 429, 500, 502, 503, 504 errors
- ✅ **Detailed Logging**: Every action is logged to `bot_execution.log`

### Logging

All activity is logged to `/root/webapp/bot_execution.log`:

```bash
# View recent activity
tail -n 50 /root/webapp/bot_execution.log

# Watch in real-time
tail -f /root/webapp/bot_execution.log

# Search for errors
grep "ERROR" /root/webapp/bot_execution.log
```

---

## 🛠️ Troubleshooting

### Problem: Script doesn't run

**Solution:**
```bash
# Make executable
chmod +x /root/webapp/dynamic_viral_engine.py

# Check Python version (requires 3.6+)
python3 --version

# Install dependencies
pip3 install requests
```

### Problem: API key errors

**Solution:**
```bash
# Set environment variable
export MOLTBOOK_API_KEY="your_key_here"

# Or edit the script directly:
MOLTBOOK_API_KEY = "your_key_here"
```

### Problem: Posts not publishing (429 errors)

**Explanation:** MoltBook server is rate-limiting or unstable. This is NORMAL.

**Solutions:**
1. The bot already has retry logic (waits and retries 5 times)
2. Run the bot less frequently (every 6-8 hours instead of 4)
3. Check MoltBook status/uptime

### Problem: Repetitive content

**This shouldn't happen**, but if it does:

1. Check that randomization is working: `import random; print(random.random())`
2. Add more content variations to the pools (see Advanced Features)
3. The bot has 168,760 unique combinations by default

### Problem: Need to target different channel

**Solution:**
Edit the `TARGET_SUBMOLT` variable:

```python
TARGET_SUBMOLT = "memecoins"  # or "trading", "defi", etc.
```

---

## 📊 Performance Metrics

### Expected Results

- **Uniqueness**: 99.9%+ unique posts across thousands of runs
- **Engagement**: Varied angles target different audience segments
- **Human-like**: No obvious patterns or repetition
- **Professional**: Clean formatting, proper grammar

### Comparison to Old Script

| Feature | Old Script | New Engine | Improvement |
|---------|-----------|------------|-------------|
| Unique Posts | 8 | 168,760 | **21,095x more** |
| Content Angles | 1 | 5 | **5x variety** |
| Formats | 1 | 2 | **2x flexibility** |
| Lines of Code | 98 | 500+ | Better structure |
| Error Handling | Basic | Advanced | Exponential backoff |

---

## 🎯 Marketing Strategy Tips

### Optimal Posting Frequency

**Recommended:** Every 4-6 hours

- **Too frequent** = Rate limits, spam detection
- **Too rare** = Lost visibility, missed opportunities

### Best Times to Post (UTC)

- 🌅 **06:00-08:00** - Europe waking up
- 🌞 **13:00-15:00** - US lunch time
- 🌙 **20:00-22:00** - Peak crypto hours

### Multi-Token Strategy

If you launch multiple tokens:

1. Create separate copies of the script for each token
2. Name them: `engine_token1.py`, `engine_token2.py`, etc.
3. Schedule at different times to avoid self-competition

---

## 🚀 Quick Token Swap Guide

**When you launch a new token (takes 30 seconds):**

1. Open `dynamic_viral_engine.py`
2. Find lines 27-29 (USER CONFIGURATION)
3. Replace:
   ```python
   TOKEN_TICKER = "$NEWTOKEN"
   CONTRACT_ADDRESS = "0xNEWADDRESS"
   DEX_LINK = f"https://dexscreener.com/base/0xNEWADDRESS"
   ```
4. Save and run: `python3 dynamic_viral_engine.py`

**Done!** The entire content library updates automatically.

---

## 📞 Support

- **Logs**: Check `/root/webapp/bot_execution.log`
- **Test Run**: `python3 dynamic_viral_engine.py`
- **Dry Run**: Comment out the `client.create_post()` line to test content generation

---

## 🎉 Success Checklist

- [ ] Updated `TOKEN_TICKER` with your token symbol
- [ ] Pasted `CONTRACT_ADDRESS` (verified on explorer)
- [ ] Set `DEX_LINK` (optional but recommended)
- [ ] Tested script manually: `python3 dynamic_viral_engine.py`
- [ ] Checked logs for success: `tail -n 20 bot_execution.log`
- [ ] Set up automated scheduling (cron or systemd)
- [ ] Monitored MoltBook for your posts

---

**Built by a Senior Python Developer + Expert Crypto Marketing Strategist**

*Generate thousands of unique, human-like marketing posts without external APIs.*

🚀 **Go viral. Make it rain.** 💰
