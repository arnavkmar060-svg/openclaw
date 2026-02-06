#!/bin/bash
# Update cron job to use new autonomous bot

API_KEY="moltbook_sk_mwrTMYQHQX4Y17sSeOySpzc1OlHD56BN"

echo "🔄 Updating cron job to use autonomous bot..."

# Remove old cron entries
crontab -l 2>/dev/null | grep -v "example_moltbook_usage.py\|run_bot.sh" > /tmp/new_cron || true

# Add new autonomous bot (every 6 hours to respect cooldown)
echo "0 */6 * * * cd /root/webapp && MOLTBOOK_API_KEY='$API_KEY' /usr/bin/python3 /root/webapp/automated_moltbook_bot.py >> /root/webapp/bot_execution.log 2>&1" >> /tmp/new_cron

# Install new crontab
crontab /tmp/new_cron
rm /tmp/new_cron

echo "✅ Cron job updated!"
echo ""
echo "New schedule:"
crontab -l
