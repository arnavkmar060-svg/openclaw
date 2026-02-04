#!/bin/bash
#
# Diagnostic script for MoltBook Bot
# Checks configuration, API key, network, and provides recommendations
#

echo "=============================================="
echo "🔍 MoltBook Bot Diagnostic Tool"
echo "=============================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/moltbook"
CREDENTIALS_FILE="$CONFIG_DIR/credentials.json"
ENV_FILE="$SCRIPT_DIR/.env"
LOG_FILE="$SCRIPT_DIR/bot_execution.log"
OLD_LOG="$SCRIPT_DIR/agent_log.txt"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

test_check() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Check Python
echo "🐍 Test 1: Python Installation"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    test_check 0 "Python installed: $PYTHON_VERSION"
else
    test_check 1 "Python 3 not found"
fi
echo ""

# Test 2: Check moltbook_standalone.py
echo "📦 Test 2: MoltBook Client Module"
if [ -f "$SCRIPT_DIR/moltbook_standalone.py" ]; then
    test_check 0 "moltbook_standalone.py exists"
    
    # Try to import
    if python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from moltbook_standalone import MoltbookClient" 2>/dev/null; then
        test_check 0 "MoltbookClient can be imported"
    else
        test_check 1 "MoltbookClient import failed"
    fi
else
    test_check 1 "moltbook_standalone.py not found"
fi
echo ""

# Test 3: Check API key sources
echo "🔑 Test 3: API Key Configuration"

API_KEY_FOUND=false

# Check environment variable
if [ -n "$MOLTBOOK_API_KEY" ]; then
    test_check 0 "MOLTBOOK_API_KEY environment variable set (length: ${#MOLTBOOK_API_KEY})"
    echo "   Value: ${MOLTBOOK_API_KEY:0:10}...${MOLTBOOK_API_KEY: -4}"
    API_KEY_FOUND=true
    API_KEY_SOURCE="environment"
else
    test_check 1 "MOLTBOOK_API_KEY environment variable NOT set"
fi

# Check .env file
if [ -f "$ENV_FILE" ]; then
    test_check 0 ".env file exists: $ENV_FILE"
    
    if grep -q "MOLTBOOK_API_KEY=" "$ENV_FILE"; then
        ENV_KEY=$(grep "MOLTBOOK_API_KEY=" "$ENV_FILE" | cut -d'=' -f2-)
        if [ -n "$ENV_KEY" ]; then
            test_check 0 ".env file contains API key (length: ${#ENV_KEY})"
            echo "   Value: ${ENV_KEY:0:10}...${ENV_KEY: -4}"
            API_KEY_FOUND=true
            API_KEY_SOURCE="env_file"
        else
            test_check 1 ".env file has empty API key"
        fi
    else
        test_check 1 ".env file missing MOLTBOOK_API_KEY"
    fi
else
    test_check 1 ".env file not found"
fi

# Check credentials.json
if [ -f "$CREDENTIALS_FILE" ]; then
    test_check 0 "credentials.json exists: $CREDENTIALS_FILE"
    
    if grep -q '"api_key"' "$CREDENTIALS_FILE"; then
        JSON_KEY=$(python3 -c "import json; print(json.load(open('$CREDENTIALS_FILE')).get('api_key', ''))" 2>/dev/null)
        if [ -n "$JSON_KEY" ]; then
            test_check 0 "credentials.json contains API key (length: ${#JSON_KEY})"
            echo "   Value: ${JSON_KEY:0:10}...${JSON_KEY: -4}"
            API_KEY_FOUND=true
            API_KEY_SOURCE="credentials_file"
        else
            test_check 1 "credentials.json has empty api_key"
        fi
    else
        test_check 1 "credentials.json missing api_key field"
    fi
else
    test_check 1 "credentials.json not found"
fi

if [ "$API_KEY_FOUND" = false ]; then
    echo ""
    echo -e "${RED}❌ CRITICAL: No API key found in any location!${NC}"
fi

echo ""

# Test 4: Test API authentication
if [ "$API_KEY_FOUND" = true ]; then
    echo "🔐 Test 4: API Authentication"
    
    # Try to authenticate
    if [ "$API_KEY_SOURCE" = "credentials_file" ]; then
        export MOLTBOOK_API_KEY="$JSON_KEY"
    elif [ "$API_KEY_SOURCE" = "env_file" ]; then
        export MOLTBOOK_API_KEY="$ENV_KEY"
    fi
    
    AUTH_TEST=$(python3 << 'PYEOF'
import sys
sys.path.insert(0, '$SCRIPT_DIR')
try:
    from moltbook_standalone import MoltbookClient
    client = MoltbookClient()
    profile = client.get_my_profile()
    if profile.get("success"):
        agent = profile.get("agent", {})
        print(f"SUCCESS|{agent.get('name')}|{agent.get('karma', 0)}|{agent.get('follower_count', 0)}")
    else:
        print(f"FAIL|{profile.get('error', 'Unknown error')}")
except Exception as e:
    print(f"ERROR|{str(e)}")
PYEOF
    )
    
    IFS='|' read -r status name karma followers <<< "$AUTH_TEST"
    
    if [ "$status" = "SUCCESS" ]; then
        test_check 0 "API authentication successful"
        echo "   Agent: $name"
        echo "   Karma: $karma"
        echo "   Followers: $followers"
    elif [ "$status" = "FAIL" ]; then
        test_check 1 "API returned error: $name"
    else
        test_check 1 "Authentication test failed: $name"
    fi
else
    echo "🔐 Test 4: API Authentication"
    echo -e "${YELLOW}⏭️  SKIPPED${NC}: No API key to test"
fi
echo ""

# Test 5: Check bot script
echo "🤖 Test 5: Bot Script"
BOT_SCRIPT="$SCRIPT_DIR/automated_moltbook_bot.py"

if [ -f "$BOT_SCRIPT" ]; then
    test_check 0 "automated_moltbook_bot.py exists"
    
    if [ -x "$BOT_SCRIPT" ]; then
        test_check 0 "Bot script is executable"
    else
        test_check 1 "Bot script not executable (fix: chmod +x $BOT_SCRIPT)"
    fi
    
    # Check for syntax errors
    if python3 -m py_compile "$BOT_SCRIPT" 2>/dev/null; then
        test_check 0 "Bot script has valid Python syntax"
    else
        test_check 1 "Bot script has syntax errors"
    fi
else
    test_check 1 "automated_moltbook_bot.py not found"
fi
echo ""

# Test 6: Check cron setup
echo "⏰ Test 6: Cron Configuration"

if command -v crontab &> /dev/null; then
    test_check 0 "crontab command available"
    
    CRON_ENTRIES=$(crontab -l 2>/dev/null | grep -c "moltbook\|run_bot")
    
    if [ "$CRON_ENTRIES" -gt 0 ]; then
        test_check 0 "Found $CRON_ENTRIES cron job(s) for bot"
        echo ""
        echo "   Current cron entries:"
        crontab -l 2>/dev/null | grep "moltbook\|run_bot" | sed 's/^/   /'
    else
        test_check 1 "No cron jobs found for bot"
    fi
else
    test_check 1 "crontab not available"
fi
echo ""

# Test 7: Check logs
echo "📜 Test 7: Log Files"

if [ -f "$LOG_FILE" ]; then
    test_check 0 "bot_execution.log exists"
    
    LOG_SIZE=$(du -h "$LOG_FILE" | cut -f1)
    echo "   Size: $LOG_SIZE"
    
    # Check for recent activity
    RECENT_RUNS=$(grep -c "EXECUTION STARTED" "$LOG_FILE" 2>/dev/null || echo "0")
    echo "   Total executions: $RECENT_RUNS"
    
    SUCCESS_COUNT=$(grep -c "POST SUCCESSFULLY CREATED" "$LOG_FILE" 2>/dev/null || echo "0")
    FAIL_COUNT=$(grep -c "POST FAILED" "$LOG_FILE" 2>/dev/null || echo "0")
    
    echo "   Successful posts: $SUCCESS_COUNT"
    echo "   Failed posts: $FAIL_COUNT"
    
    if [ "$SUCCESS_COUNT" -gt 0 ]; then
        test_check 0 "Bot has successfully posted before"
    else
        test_check 1 "No successful posts found in log"
    fi
else
    test_check 1 "bot_execution.log not found (bot hasn't run yet)"
fi

if [ -f "$OLD_LOG" ]; then
    echo "   ℹ️  Old log file found: agent_log.txt"
fi
echo ""

# Test 8: Network connectivity
echo "🌐 Test 8: Network Connectivity"

if ping -c 1 www.moltbook.com &> /dev/null; then
    test_check 0 "Can reach www.moltbook.com"
else
    test_check 1 "Cannot reach www.moltbook.com (check network/firewall)"
fi

if curl -s -o /dev/null -w "%{http_code}" https://www.moltbook.com/api/v1/posts | grep -q "200\|401"; then
    test_check 0 "MoltBook API endpoint reachable"
else
    test_check 1 "MoltBook API endpoint not reachable"
fi
echo ""

# Summary
echo "=============================================="
echo "📊 Diagnostic Summary"
echo "=============================================="
echo ""
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

# Recommendations
if [ $TESTS_FAILED -gt 0 ]; then
    echo "🔧 Recommendations:"
    echo ""
    
    if [ "$API_KEY_FOUND" = false ]; then
        echo -e "${YELLOW}⚠️  CRITICAL: No API key configured!${NC}"
        echo "   Fix: Run ./setup_bot.sh to configure your API key"
        echo ""
    fi
    
    if ! crontab -l 2>/dev/null | grep -q "moltbook\|run_bot"; then
        echo -e "${YELLOW}⚠️  No cron job configured${NC}"
        echo "   Fix: Run ./setup_bot.sh to set up automated posting"
        echo ""
    fi
    
    if [ ! -f "$BOT_SCRIPT" ]; then
        echo -e "${YELLOW}⚠️  Bot script missing${NC}"
        echo "   Fix: Re-download automated_moltbook_bot.py"
        echo ""
    fi
    
    echo "🚀 Quick fix: Run the setup script"
    echo "   $ cd $SCRIPT_DIR"
    echo "   $ ./setup_bot.sh"
else
    echo -e "${GREEN}✅ All tests passed! Your bot is properly configured.${NC}"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Test manual run: $BOT_SCRIPT"
    echo "   2. Monitor logs: tail -f $LOG_FILE"
    echo "   3. Wait for next cron execution"
fi

echo ""
echo "=============================================="
echo "📖 For more help, see: BOT_README.md"
echo "=============================================="
