#!/bin/bash
#
# Setup script for Automated MoltBook Bot
# This script will:
# 1. Store your MOLTBOOK_API_KEY securely
# 2. Configure cron job with proper environment
# 3. Test the bot execution
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/moltbook"
CREDENTIALS_FILE="$CONFIG_DIR/credentials.json"
ENV_FILE="$SCRIPT_DIR/.env"
CRON_SCRIPT="$SCRIPT_DIR/run_bot.sh"

echo "=============================================="
echo "🤖 MoltBook Bot Setup"
echo "=============================================="
echo ""

# Step 1: Get API key
echo "📝 Step 1: API Key Configuration"
echo ""

if [ -n "$MOLTBOOK_API_KEY" ]; then
    echo "✅ MOLTBOOK_API_KEY found in environment"
    API_KEY="$MOLTBOOK_API_KEY"
else
    echo "❓ Enter your MoltBook API key:"
    read -r API_KEY
    
    if [ -z "$API_KEY" ]; then
        echo "❌ Error: No API key provided!"
        exit 1
    fi
fi

echo "✅ API Key: ${API_KEY:0:10}...${API_KEY: -4}"
echo ""

# Step 2: Store in config file (JSON format for moltbook_standalone.py)
echo "📁 Step 2: Storing credentials..."
mkdir -p "$CONFIG_DIR"

cat > "$CREDENTIALS_FILE" << EOF
{
  "api_key": "$API_KEY"
}
EOF

chmod 600 "$CREDENTIALS_FILE"
echo "✅ Credentials saved to: $CREDENTIALS_FILE"
echo ""

# Step 3: Create .env file for environment variable method
echo "📋 Step 3: Creating .env file..."

cat > "$ENV_FILE" << EOF
# MoltBook Bot Configuration
MOLTBOOK_API_KEY=$API_KEY
TWITTER_HANDLE=@ENG_Cryptoo0
EOF

chmod 600 "$ENV_FILE"
echo "✅ .env file created: $ENV_FILE"
echo ""

# Step 4: Create cron execution script
echo "⚙️  Step 4: Creating cron execution script..."

cat > "$CRON_SCRIPT" << 'EOF'
#!/bin/bash
# Cron execution wrapper for automated_moltbook_bot.py

# Load environment variables from .env file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Execute bot
cd "$SCRIPT_DIR"
/usr/bin/python3 "$SCRIPT_DIR/automated_moltbook_bot.py" >> "$SCRIPT_DIR/bot_execution.log" 2>&1

exit $?
EOF

chmod +x "$CRON_SCRIPT"
echo "✅ Cron script created: $CRON_SCRIPT"
echo ""

# Step 5: Test the bot
echo "🧪 Step 5: Testing bot execution..."
echo "----------------------------------------"

# Source the env file and run test
export $(grep -v '^#' "$ENV_FILE" | xargs)

if /usr/bin/python3 "$SCRIPT_DIR/automated_moltbook_bot.py"; then
    echo "----------------------------------------"
    echo "✅ Bot test SUCCESSFUL!"
    echo ""
    
    # Show the log
    echo "📜 Last 20 lines of execution log:"
    echo "----------------------------------------"
    tail -20 "$SCRIPT_DIR/bot_execution.log"
    echo "----------------------------------------"
    echo ""
    
    # Step 6: Setup cron job
    echo "⏰ Step 6: Cron Job Setup"
    echo ""
    echo "Choose posting frequency:"
    echo "  1. Every 6 hours (4 posts/day)"
    echo "  2. Every 12 hours (2 posts/day)"
    echo "  3. Daily at 9 AM"
    echo "  4. Custom"
    echo "  5. Skip (configure manually)"
    echo ""
    echo -n "Your choice (1-5): "
    read -r cron_choice
    
    case $cron_choice in
        1)
            CRON_SCHEDULE="0 */6 * * *"
            CRON_DESC="Every 6 hours"
            ;;
        2)
            CRON_SCHEDULE="0 */12 * * *"
            CRON_DESC="Every 12 hours"
            ;;
        3)
            CRON_SCHEDULE="0 9 * * *"
            CRON_DESC="Daily at 9 AM"
            ;;
        4)
            echo -n "Enter cron schedule (e.g., '0 */6 * * *'): "
            read -r CRON_SCHEDULE
            CRON_DESC="Custom schedule"
            ;;
        5)
            echo "⏭️  Skipping cron setup"
            echo ""
            echo "To manually add cron job, run:"
            echo "  crontab -e"
            echo ""
            echo "Add this line:"
            echo "  0 */6 * * * $CRON_SCRIPT"
            echo ""
            exit 0
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
    
    # Add to crontab
    echo ""
    echo "Adding cron job: $CRON_DESC ($CRON_SCHEDULE)"
    
    # Create temp crontab with existing entries + new one
    crontab -l 2>/dev/null > /tmp/current_cron || true
    
    # Remove any existing entries for this bot
    grep -v "automated_moltbook_bot.py\|run_bot.sh" /tmp/current_cron > /tmp/new_cron || true
    
    # Add new entry
    echo "$CRON_SCHEDULE $CRON_SCRIPT" >> /tmp/new_cron
    
    # Install new crontab
    crontab /tmp/new_cron
    
    rm /tmp/current_cron /tmp/new_cron
    
    echo "✅ Cron job installed successfully!"
    echo ""
    echo "Current crontab:"
    echo "----------------------------------------"
    crontab -l
    echo "----------------------------------------"
    
else
    echo "----------------------------------------"
    echo "❌ Bot test FAILED!"
    echo ""
    echo "Check the log file for details:"
    echo "  tail -50 $SCRIPT_DIR/bot_execution.log"
    exit 1
fi

echo ""
echo "=============================================="
echo "✅ Setup Complete!"
echo "=============================================="
echo ""
echo "📊 Next steps:"
echo "  1. Monitor execution log: tail -f $SCRIPT_DIR/bot_execution.log"
echo "  2. Check MoltBook for posts: https://www.moltbook.com/"
echo "  3. View cron status: crontab -l"
echo ""
echo "🔧 To run bot manually:"
echo "  $CRON_SCRIPT"
echo ""
echo "🛠️  To update cron schedule:"
echo "  crontab -e"
echo ""
echo "Happy automating! 🦞🚀"
