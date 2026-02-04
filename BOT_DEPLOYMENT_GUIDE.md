# 🤖 Python Crypto Bot Deployment Guide

## ✅ Environment Setup - COMPLETE!

Your Python bot environment has been **completely fixed** and is ready to use!

---

## 📁 Project Structure

```
/root/webapp/
├── fix_and_run.sh          # ⭐ Main setup script (ALREADY RUN)
├── launch_bots.sh          # 🚀 Bot launcher
├── bot_nemr/
│   └── main_nemr.py        # Nemr_AI bot
├── bot_eng/
│   └── main_eng.py         # Eng_Crypto bot
├── venv/                   # Virtual environment (CREATED)
│   └── bin/
│       └── python3         # Use THIS Python!
└── requirements.txt        # Dependencies (INSTALLED)
```

---

## 🎯 Quick Start

### Option 1: Run in Foreground (Recommended for Testing)
```bash
cd /root/webapp
./launch_bots.sh
```
- **Pros**: See live output from both bots
- **Cons**: Terminal stays occupied
- **Stop**: Press `Ctrl+C`

### Option 2: Run in Background (Recommended for Production)
```bash
cd /root/webapp
./launch_bots.sh background
```
- **Pros**: Runs independently, terminal free
- **Cons**: No direct output visibility
- **View logs**: `tail -f bot_nemr.log bot_eng.log`
- **Stop**: Use the PID numbers shown or `pkill -f "main_nemr.py|main_eng.py"`

---

## 🔧 What Was Fixed

### ❌ Problems Solved:
1. **PEP 668 Error**: `error: externally-managed-environment`
   - ✅ **Solution**: Installed `python3-venv` and created isolated venv

2. **Missing ensurepip**: `ensurepip is not available`
   - ✅ **Solution**: Installed `python3-full` and `python3-venv` system packages

3. **ModuleNotFoundError**: Missing `requests`, `schedule`, `pytrends`
   - ✅ **Solution**: Installed all dependencies in venv

### ✅ What's Now Installed:
```
System Packages:
  ✓ python3-pip
  ✓ python3-venv
  ✓ python3-full
  ✓ python3-dev
  ✓ build-essential

Python Packages (in venv):
  ✓ requests==2.32.5
  ✓ schedule==1.2.2
  ✓ pytrends==4.9.2
```

---

## 🛠️ Manual Bot Control

### Start Individual Bots:
```bash
# Nemr bot only
/root/webapp/venv/bin/python3 /root/webapp/bot_nemr/main_nemr.py

# Eng bot only
/root/webapp/venv/bin/python3 /root/webapp/bot_eng/main_eng.py
```

### Check Running Bots:
```bash
ps aux | grep -E "(main_nemr|main_eng)" | grep -v grep
```

### View Live Logs:
```bash
# Both bots
tail -f /root/webapp/bot_nemr.log /root/webapp/bot_eng.log

# Nemr only
tail -f /root/webapp/bot_nemr.log

# Eng only
tail -f /root/webapp/bot_eng.log
```

### Stop Bots:
```bash
# Stop all bot processes
pkill -f "main_nemr.py|main_eng.py"

# Or use specific PIDs (shown when starting in background)
kill <PID_NEMR> <PID_ENG>
```

---

## 🔄 Bot Behavior

### Nemr_AI Bot (`bot_nemr/main_nemr.py`):
- **Character**: Enthusiastic, hype-driven crypto personality
- **Schedule**:
  - Every 25 hours: Mint new token based on Google Trends
  - Every 12 hours: Promote current token
  - Every 3 hours: Post general crypto content
- **API Keys**:
  - Bankr: `bk_XE6SA2BLVX5U37LET5KMLYRGJMRMEPG8`
  - Moltbook: `moltbook_sk_c1f0hM1mYPXxgaJgXadTFjB95ofK5xhv`

### Eng_Crypto Bot (`bot_eng/main_eng.py`):
- **Character**: Technical, analytical crypto expert
- **Schedule**:
  - Every 25 hours: Mint new token based on Google Trends
  - Every 12 hours: Promote current token
  - Every 3 hours: Post general crypto analysis
- **API Keys**:
  - Bankr: `bk_9CLVKYTQKHYYZXRES6A5TJL7MYJLDJT8`
  - Moltbook: `moltbook_sk_mwrTMYQHQX4Y17sSeOySpzc1OlHD56BN`

---

## 🔐 Production Deployment on VPS

### Using systemd (Recommended):

1. **Create systemd service file** (`/etc/systemd/system/crypto-bots.service`):
```ini
[Unit]
Description=Crypto Trading Bots (Nemr + Eng)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/webapp
ExecStart=/root/webapp/launch_bots.sh foreground
Restart=always
RestartSec=10
StandardOutput=append:/root/webapp/bots_system.log
StandardError=append:/root/webapp/bots_system.log

[Install]
WantedBy=multi-user.target
```

2. **Enable and start**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable crypto-bots.service
sudo systemctl start crypto-bots.service
sudo systemctl status crypto-bots.service
```

3. **View logs**:
```bash
sudo journalctl -u crypto-bots.service -f
```

### Using Supervisor (Alternative):

1. **Install supervisor**:
```bash
pip install supervisor
```

2. **Create config** (`/root/webapp/supervisor_bots.conf`):
```ini
[supervisord]
nodaemon=false
logfile=/root/webapp/supervisor.log
pidfile=/root/webapp/supervisor.pid

[unix_http_server]
file=/root/webapp/supervisor.sock

[supervisorctl]
serverurl=unix:///root/webapp/supervisor.sock

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[program:nemr_bot]
command=/root/webapp/venv/bin/python3 /root/webapp/bot_nemr/main_nemr.py
directory=/root/webapp
autostart=true
autorestart=true
stdout_logfile=/root/webapp/nemr_supervisor.log
stderr_logfile=/root/webapp/nemr_supervisor_error.log

[program:eng_bot]
command=/root/webapp/venv/bin/python3 /root/webapp/bot_eng/main_eng.py
directory=/root/webapp
autostart=true
autorestart=true
stdout_logfile=/root/webapp/eng_supervisor.log
stderr_logfile=/root/webapp/eng_supervisor_error.log
```

3. **Run supervisor**:
```bash
supervisord -c /root/webapp/supervisor_bots.conf
supervisorctl -c /root/webapp/supervisor_bots.conf status
```

---

## 🧪 Testing & Verification

### Test Virtual Environment:
```bash
/root/webapp/venv/bin/python3 -c 'import requests, schedule; from pytrends.request import TrendReq; print("✓ All imports successful!")'
```

### Test Single Bot (10 seconds):
```bash
timeout 10s /root/webapp/venv/bin/python3 /root/webapp/bot_nemr/main_nemr.py
```

### Verify Dependencies:
```bash
/root/webapp/venv/bin/pip freeze | grep -E "(requests|schedule|pytrends)"
```

---

## 🆘 Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution**: You're using system Python instead of venv Python
```bash
# ❌ Wrong:
python3 bot_nemr/main_nemr.py

# ✅ Correct:
/root/webapp/venv/bin/python3 bot_nemr/main_nemr.py
```

### Problem: "ensurepip is not available"
**Solution**: Re-run the fix script:
```bash
cd /root/webapp
./fix_and_run.sh
```

### Problem: Bots not posting
**Check**:
1. Verify API keys are correct
2. Check network connectivity
3. View error logs: `tail -f bot_nemr.log bot_eng.log`

### Problem: "externally-managed-environment"
**Solution**: Always use the venv Python:
```bash
/root/webapp/venv/bin/python3 <script>
```

---

## 📊 Monitoring

### Check Bot Status:
```bash
# Are they running?
ps aux | grep python3 | grep -E "(main_nemr|main_eng)"

# How long have they been running?
ps -p $(pgrep -f main_nemr.py) -o etime=
```

### View Recent Activity:
```bash
# Last 50 lines from each log
tail -50 bot_nemr.log
tail -50 bot_eng.log
```

### Check Resource Usage:
```bash
top -p $(pgrep -f "main_nemr.py|main_eng.py")
```

---

## 🚀 Next Steps

1. **Test the bots**: Run `./launch_bots.sh` to see them in action
2. **Monitor logs**: Watch `bot_nemr.log` and `bot_eng.log`
3. **Enable real minting**: Uncomment the API calls in the `mint_token()` functions
4. **Set up systemd**: For production deployment with auto-restart
5. **Configure monitoring**: Set up alerts for bot failures

---

## 📝 Important Notes

- **Virtual Environment**: Always use `/root/webapp/venv/bin/python3`
- **Token Minting**: Currently in DRY-RUN mode (change in code to enable spending)
- **Scheduling**: Bots use `schedule` library for timing (runs continuously)
- **Persistence**: Bots store current token in `token.json` files

---

## 🎉 Success Indicators

✅ No `externally-managed-environment` errors  
✅ Virtual environment created successfully  
✅ All dependencies installed  
✅ Bots start without ModuleNotFoundError  
✅ Scripts are executable and ready to use  

**Your environment is now fully operational!** 🚀

---

## 📞 Quick Reference Commands

```bash
# Start bots (foreground)
./launch_bots.sh

# Start bots (background)
./launch_bots.sh background

# Check status
ps aux | grep "main_.*\.py"

# View logs
tail -f bot_*.log

# Stop all
pkill -f "main_nemr.py|main_eng.py"

# Re-fix environment if needed
./fix_and_run.sh
```

---

**Last Updated**: 2026-02-04  
**Environment**: Debian/Ubuntu VPS  
**Python Version**: 3.12  
**Status**: ✅ FULLY OPERATIONAL
