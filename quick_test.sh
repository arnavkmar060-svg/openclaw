#!/bin/bash
#
# Quick Test Script for MoltBook Bot
# This sets the key and runs the bot ONCE immediately.

# 1. Define the Key (Using your restored key)
export MOLTBOOK_API_KEY='moltbook_sk_mwrTMYQHQX4Y17sSeOySpzc1OlHD56BN'

echo "=============================================="
echo "🧪 Running Quick Test for MoltBook Bot..."
echo "🔑 Using Key: $MOLTBOOK_API_KEY"
echo "=============================================="

# 2. Run the Python Script
/usr/bin/python3 /root/webapp/automated_moltbook_bot.py

# 3. Check the Result
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ TEST PASSED! The bot ran without errors."
    echo "📄 Check 'bot_execution.log' for details."
else
    echo ""
    echo "❌ TEST FAILED! The bot encountered an error."
fi

echo "=============================================="
