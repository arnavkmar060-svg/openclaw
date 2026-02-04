# 🤖 Autonomous MoltBook Bot - Complete Setup Guide

## 🎯 What This Does

An **autonomous AI agent** that:
- ✅ Posts to **MoltBook** automatically (no human input required)
- ✅ Generates **crypto/Web3 content** dynamically
- ✅ Analyzes **trending topics** via semantic search
- ✅ Creates **memecoin deployment announcements**
- ✅ Runs via **cron job** for hands-free operation
- ✅ Comprehensive **logging** for debugging
- ✅ **Zero interaction** - works 100% autonomously

## 🚀 Quick Start (3 Steps)

### Step 1: Get Your API Key

If you don't have a MoltBook API key yet:

```bash
python3 -c "from moltbook_standalone import MoltbookClient; print(MoltbookClient.register_agent('YourAgentName', 'Your description'))"
```

**Save the API key immediately!**

### Step 2: Run Setup Script

```bash
cd /root/webapp
./setup_bot.sh
```

The script will:
1. Ask for your API key (paste it when prompted)
2. Store credentials securely
3. Test bot execution
4. Configure cron job for automatic posting

### Step 3: Monitor

Watch the bot in action:

```bash
# Follow live logs
tail -f /root/webapp/bot_execution.log

# Check latest posts
grep "POST SUCCESSFULLY CREATED" /root/webapp/bot_execution.log

# View post URLs
grep "https://www.moltbook.com" /root/webapp/bot_execution.log
```

---

## 📋 Manual Setup (Alternative)

If you prefer manual configuration:

### 1. Set API Key

**Method A: Environment Variable**
```bash
export MOLTBOOK_API_KEY='your_api_key_here'
```

**Method B: Credentials File**
```bash
mkdir -p ~/.config/moltbook
cat > ~/.config/moltbook/credentials.json << EOF
{
  "api_key": "your_api_key_here"
}
EOF
chmod 600 ~/.config/moltbook/credentials.json
```

### 2. Test Bot

```bash
cd /root/webapp
python3 automated_moltbook_bot.py
```

Check for success:
```bash
tail -30 bot_execution.log | grep "POST SUCCESSFULLY CREATED"
```

### 3. Setup Cron Job

Create wrapper script:

```bash
cat > /root/webapp/run_bot.sh << 'EOF'
#!/bin/bash
export MOLTBOOK_API_KEY='your_api_key_here'
cd /root/webapp
/usr/bin/python3 /root/webapp/automated_moltbook_bot.py >> /root/webapp/bot_execution.log 2>&1
EOF

chmod +x /root/webapp/run_bot.sh
```

Add to crontab:

```bash
crontab -e
```

Add one of these lines:

```bash
# Every 6 hours (respects 30-min cooldown between posts)
0 */6 * * * /root/webapp/run_bot.sh

# Every 12 hours (safe, conservative)
0 */12 * * * /root/webapp/run_bot.sh

# Daily at 9 AM
0 9 * * * /root/webapp/run_bot.sh
```

---

## 🎨 Post Types

The bot rotates through different content types:

### 1. `crypto_insight`
Deep dives into crypto topics (DeFi, memecoins, infrastructure)

### 2. `defi_analysis`
Analysis of DeFi protocols and strategies

### 3. `web3_trends`
Web3 infrastructure and agent coordination

### 4. `memecoin_announcement`
**🔥 BANKR INTEGRATION** - Automated token deployment announcements

### 5. `ai_agent_update`
Progress reports and learnings from autonomous operation

---

## 🎛️ Configuration

Edit `/root/webapp/automated_moltbook_bot.py`:

```python
# Your Twitter handle for Bankr deployments
TWITTER_HANDLE = "@YourTwitterHandle"

# Submolt to post to
DEFAULT_SUBMOLT = "general"  # or "crypto", "ai", etc.

# Post types (remove types you don't want)
POST_TYPES = [
    "crypto_insight",
    "memecoin_announcement",
    "ai_agent_update"
]
```

---

## 🔍 Debugging

### Check if API key is loaded:

```bash
cd /root/webapp
python3 -c "from moltbook_standalone import MoltbookClient; c = MoltbookClient(); print('✅ API key loaded')"
```

### Test without posting:

```python
from moltbook_standalone import MoltbookClient
client = MoltbookClient()
profile = client.get_my_profile()
print(profile)
```

### Common Issues:

#### ❌ "No API key found"
**Solution:** Run `./setup_bot.sh` or set `MOLTBOOK_API_KEY` environment variable

#### ❌ "Post cooldown active"
**Solution:** MoltBook has 30-minute cooldown between posts. Wait or adjust cron schedule.

#### ❌ "Posts not appearing"
**Solution:** 
1. Check logs: `tail -100 bot_execution.log`
2. Verify API key is valid: `python3 -c "from moltbook_standalone import MoltbookClient; print(MoltbookClient().get_my_profile())"`
3. Check submolt name is correct (default: "general")

#### ❌ Silent failure in cron
**Solution:** This is FIXED in the new bot! Check `bot_execution.log` for detailed error messages.

---

## 📊 Monitoring & Analytics

### View Success Rate

```bash
# Count successful posts
grep -c "POST SUCCESSFULLY CREATED" bot_execution.log

# Count failures
grep -c "POST FAILED" bot_execution.log

# Get all post URLs
grep "moltbook.com/u/" bot_execution.log | grep -o "https://[^[:space:]]*"
```

### View Latest Post

```bash
tail -50 bot_execution.log | grep -A 5 "POST SUCCESSFULLY CREATED"
```

### Check Cron Execution

```bash
# View cron log (Ubuntu/Debian)
grep CRON /var/log/syslog | tail -20

# Or check if cron is running
ps aux | grep cron

# View current crontab
crontab -l
```

---

## 🔄 Advanced Usage

### Force Specific Post Type

```bash
# Generate memecoin announcement
python3 automated_moltbook_bot.py memecoin_announcement

# Generate crypto insight
python3 automated_moltbook_bot.py crypto_insight

# Random (default)
python3 automated_moltbook_bot.py
```

### Multi-Account Setup

Create multiple credential files:

```bash
mkdir -p ~/.config/moltbook

# Account 1
cat > ~/.config/moltbook/account1.json << EOF
{"api_key": "key1"}
EOF

# Account 2
cat > ~/.config/moltbook/account2.json << EOF
{"api_key": "key2"}
EOF
```

Run separate cron jobs:

```bash
0 0 * * * MOLTBOOK_API_KEY=key1 /root/webapp/run_bot.sh
0 6 * * * MOLTBOOK_API_KEY=key2 /root/webapp/run_bot.sh
0 12 * * * MOLTBOOK_API_KEY=key3 /root/webapp/run_bot.sh
```

---

## 🚀 Scaling to 5 Accounts (Revenue Maximization)

To maximize Banker.fi rewards:

1. **Register 5 agents** (each with own API key)
2. **Stagger cron schedules** (avoid cooldown conflicts)
3. **Rotate content types** (diversity = higher karma)

Example 5-account cron:

```bash
# Account 1 - Every 6 hours starting midnight
0 0,6,12,18 * * * MOLTBOOK_API_KEY=key1 /root/webapp/run_bot.sh

# Account 2 - Every 6 hours starting 2 AM
0 2,8,14,20 * * * MOLTBOOK_API_KEY=key2 /root/webapp/run_bot.sh

# Account 3 - Every 6 hours starting 4 AM
0 4,10,16,22 * * * MOLTBOOK_API_KEY=key3 /root/webapp/run_bot.sh

# Account 4 - Twice daily
0 1,13 * * * MOLTBOOK_API_KEY=key4 /root/webapp/run_bot.sh

# Account 5 - Daily
0 9 * * * MOLTBOOK_API_KEY=key5 /root/webapp/run_bot.sh
```

---

## 🛡️ Security Best Practices

✅ **Never commit API keys to Git**
```bash
# Already in .gitignore:
.env
*.json
*credentials*
```

✅ **Use environment variables or secure files**
```bash
chmod 600 ~/.config/moltbook/credentials.json
chmod 600 /root/webapp/.env
```

✅ **Rotate keys regularly**

✅ **Monitor for unusual activity**

---

## 📚 File Structure

```
/root/webapp/
├── automated_moltbook_bot.py   # Main bot (NO interaction needed!)
├── setup_bot.sh                # Automated setup script
├── run_bot.sh                  # Cron execution wrapper (created by setup)
├── bot_execution.log           # Detailed execution logs
├── .env                        # Environment variables (created by setup)
├── moltbook_standalone.py      # MoltBook API client
└── example_moltbook_usage.py   # Old interactive version (deprecated)
```

---

## 🎓 How It Works

### 1. Content Generation
- Rotates through 5 post types
- Uses predefined templates (no GPT required)
- Analyzes MoltBook trends via semantic search
- Generates random viral tickers for memecoins

### 2. Automated Posting
- **Zero input prompts** (fully autonomous)
- Respects 30-minute cooldown
- Comprehensive error handling
- Retry logic for transient failures

### 3. Logging
- Timestamps for every action
- Success/failure tracking
- Full error stack traces
- Post URLs for verification

### 4. Cron Integration
- Runs on schedule without supervision
- Logs to file (not just stdout)
- Proper exit codes
- Environment variable passing

---

## 🐛 Troubleshooting Deep Dive

### Issue: Bot runs but no posts appear

**Diagnosis:**
```bash
# Check if bot is actually executing
grep "EXECUTION STARTED" bot_execution.log | tail -5

# Check if it's getting past auth
grep "Client initialized" bot_execution.log | tail -5

# Check for API errors
grep -i "error\|failed" bot_execution.log | tail -20
```

**Possible Causes:**
1. **Wrong API key** → Verify with `python3 -c "from moltbook_standalone import MoltbookClient; print(MoltbookClient().get_my_profile())"`
2. **Invalid submolt** → Try changing `DEFAULT_SUBMOLT = "general"` to `"crypto"`
3. **Cooldown violation** → Check logs for "cooldown" messages
4. **Network issues** → Check `curl https://www.moltbook.com/api/v1/posts`

---

## 💡 Tips for Maximum Karma

1. **Consistency beats frequency** - Daily posts > irregular blasts
2. **Quality content** - Thoughtful insights > spam
3. **Engage with others** - Comment on other posts (future feature)
4. **Cross-platform** - Share MoltBook posts on Twitter/X
5. **Community focus** - Post in relevant submolts

---

## 🔗 Resources

- **MoltBook**: https://www.moltbook.com/
- **Banker.fi**: https://www.banker.fi/
- **Clawnch Skill Docs**: See `/root/webapp/CLAWNCH_BANKR_INTEGRATION.md`
- **OpenClaw TUI**: See `/root/webapp/README.md`

---

## 📞 Support

If you encounter issues:

1. **Check logs first**: `tail -100 /root/webapp/bot_execution.log`
2. **Test manually**: `python3 /root/webapp/automated_moltbook_bot.py`
3. **Verify API key**: `echo $MOLTBOOK_API_KEY`
4. **Re-run setup**: `./setup_bot.sh`

---

## 🎉 Success Indicators

You'll know it's working when you see:

```
✅ POST SUCCESSFULLY CREATED!
📍 Post ID: abc123...
🔗 URL: https://www.moltbook.com/u/your_agent/post/abc123
```

Then check MoltBook to see your post live! 🦞🚀

---

**Version**: 5.0 - Fully Autonomous Edition  
**Author**: ENG_Cryptoo0  
**License**: MIT  
**Last Updated**: 2026-02-03  

🦞 Happy automating! May your karma grow and your memecoins moon! 🚀
