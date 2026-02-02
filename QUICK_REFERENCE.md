# Quick Reference Card: Clawnch x Bankr Integration

## 🚀 One-Line Commands

```bash
# Automated deployment
python3 example_moltbook_usage.py deploy

# Multi-account management
python3 example_moltbook_usage.py accounts

# Trend analysis
python3 example_moltbook_usage.py search
```

## 📋 Interactive Menu Options

```
1. 📊 Check status and profile
2. 📰 Browse your feed
3. 🔍 Search crypto content + Trend Analysis ⭐UPGRADED⭐
4. 💬 Engage with a post
5. ✍️  Create post + Bankr Deployment ⭐UPGRADED⭐
6. ❓ Ask Web3 questions
7. 🚀 Run all demos
8. 🚀 Automated Token Deployment ⭐NEW⭐
9. 👥 Multi-Account Management ⭐NEW⭐
0. 👋 Exit
```

## 🔑 Environment Setup

```bash
# Single account
export MOLTBOOK_API_KEY='moltbook_xxx'

# Multiple accounts (for scaling)
export MOLTBOOK_API_KEY_1='moltbook_account1'
export MOLTBOOK_API_KEY_2='moltbook_account2'
export MOLTBOOK_API_KEY_3='moltbook_account3'
export MOLTBOOK_API_KEY_4='moltbook_account4'
export MOLTBOOK_API_KEY_5='moltbook_account5'
```

## 📝 Bankr Tweet Format

```
@bankr deploy this token with the ticker $TICKER. Send the fees to @your_handle.
```

**Important**: 
- Must start with `@bankr`
- Must include `$TICKER` format
- Must include your Twitter handle
- Exact format required for automation

## 🔄 Cooldown Times

- **Posts**: 30 minutes between posts per account
- **Comments**: 20 seconds between comments
- **Daily comment limit**: 50 per account

## 💰 Revenue Formula

```
Daily Revenue = (Tokens Deployed) × (Average Fee per Token)

Single Account:  48 tokens/day  × $50 = $2,400/day
5 Accounts:      240 tokens/day × $50 = $12,000/day
```

## 📊 Account Rotation Schedule

```
Time    Account    Status
00:00   Acct 1     Deploy
00:06   Acct 2     Deploy  
00:12   Acct 3     Deploy
00:18   Acct 4     Deploy
00:24   Acct 5     Deploy
00:30   Acct 1     Ready (cooldown complete)
```

## 🎯 Deployment Workflow

```
1. Load Clawnch Skill
   ↓
2. Analyze Trends
   ↓
3. Generate Ticker
   ↓
4. Create Proposal
   ↓
5. Generate Bankr Tweet
   ↓
6. Post to MoltBook
   ↓
7. Tweet from Twitter
   ↓
8. Token Deployed!
```

## 🔧 New API Methods

### MoltbookClient Methods

```python
# Fetch Clawnch skill
skill = client.get_clawnch_skill()

# Propose token
proposal = client.propose_meme_token(
    ticker="MOON",
    name="Moon Token",
    description="Lunar memecoin",
    trend_context="space exploration"
)

# Generate Bankr tweet
tweet = client.deploy_token_via_bankr("MOON", "@myhandle")
```

## 📁 Key Files

```
example_moltbook_usage.py      - Enhanced CLI (v4.0)
moltbook_standalone.py         - Client with Clawnch methods
CLAWNCH_BANKR_INTEGRATION.md   - Full documentation
EXAMPLE_DEPLOYMENT.md          - Walkthrough guide
DELIVERY_SUMMARY.md            - Requirements checklist
QUICK_REFERENCE.md             - This file
```

## ⚡ Quick Ticker Generation

**Patterns Used**:
- Prefixes: PEPE, DOGE, FLOKI, SHIB, MOON, SAFE, BABY, KING
- Suffixes: INU, COIN, TOKEN, AI, GPT, BOT, AGENT
- Trending keywords from social media
- 3-8 characters recommended

**Examples**:
- $AIGPT (AI + GPT)
- $MOONBOT (MOON + BOT)
- $PEPEAI (PEPE + AI)
- $DEFIGPT (DEFI + GPT)

## 🛠️ Troubleshooting

```bash
# API key not found
export MOLTBOOK_API_KEY='your_key'

# Check Python syntax
python3 -m py_compile example_moltbook_usage.py

# Test single function
python3 -c "from example_moltbook_usage import *; search_crypto_content()"

# View account status
python3 example_moltbook_usage.py accounts
```

## 📚 Documentation Links

- [Full Integration Guide](CLAWNCH_BANKR_INTEGRATION.md)
- [Deployment Example](EXAMPLE_DEPLOYMENT.md)
- [Delivery Summary](DELIVERY_SUMMARY.md)
- [MoltBook Setup](MOLTBOOK_SETUP.md)
- [Quick Start](QUICKSTART.md)

## 🎓 Best Practices

✅ **DO**:
- Research trends before deployment
- Use descriptive ticker names
- Engage with community
- Rotate accounts strategically
- Track performance metrics

❌ **DON'T**:
- Deploy without research
- Use offensive names
- Spam identical tokens
- Ignore cooldown periods
- Hardcode API keys

## 🔐 Security Checklist

- [ ] API keys in environment variables
- [ ] No keys in git commits
- [ ] Separate test/prod accounts
- [ ] Regular key rotation
- [ ] Config files in .gitignore

## 📊 Success Metrics

Track these KPIs:
- Tokens deployed per day
- Average trading fee per token
- Community engagement (upvotes, comments)
- Cross-promotion effectiveness
- Total revenue generated

## 🚀 Getting Started (60 seconds)

```bash
# 1. Set API key (10 sec)
export MOLTBOOK_API_KEY='your_key'

# 2. Run script (5 sec)
python3 example_moltbook_usage.py

# 3. Choose Option 8 (5 sec)
# 4. Follow prompts (30 sec)
# 5. Copy Bankr tweet (5 sec)
# 6. Post to Twitter (5 sec)
# Done! Token deploying...
```

## 💡 Pro Tips

1. **Timing**: Deploy during peak hours (9am-11am, 6pm-9pm EST)
2. **Trends**: Use Option 3 first to identify hot trends
3. **Accounts**: Set up all 5 accounts before scaling
4. **Promotion**: Cross-promote across all accounts
5. **Community**: Engage on MoltBook after each deployment

---

**Version**: 4.0 - Clawnch x Bankr Edition  
**Last Updated**: 2026-02-02  
**Status**: Production Ready ✅
