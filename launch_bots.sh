#!/bin/bash
################################################################################
# BOT LAUNCHER SCRIPT (uses venv python)
################################################################################

set -e
cd /root/webapp

VENV_PYTHON="/root/webapp/venv/bin/python3"
BOT_NEMR="/root/webapp/bot_nemr/main_nemr.py"
BOT_ENG="/root/webapp/bot_eng/main_eng.py"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           LAUNCHING CRYPTO BOTS                          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verify venv python exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${RED}✗ Virtual environment Python not found at: $VENV_PYTHON${NC}"
    echo -e "${YELLOW}Run fix_and_run.sh first to set up the environment${NC}"
    exit 1
fi

# Verify bot files exist
if [ ! -f "$BOT_NEMR" ]; then
    echo -e "${RED}✗ Bot file not found: $BOT_NEMR${NC}"
    exit 1
fi

if [ ! -f "$BOT_ENG" ]; then
    echo -e "${RED}✗ Bot file not found: $BOT_ENG${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Using Python from venv: $VENV_PYTHON${NC}"
echo -e "${GREEN}✓ Bot files verified${NC}"
echo ""

# Check if we want to run in background or foreground
MODE="${1:-foreground}"

if [ "$MODE" == "background" ]; then
    echo -e "${YELLOW}Starting bots in BACKGROUND mode...${NC}"
    echo ""
    
    # Start Nemr bot in background
    echo -e "${BLUE}→ Starting Nemr_AI bot...${NC}"
    nohup "$VENV_PYTHON" "$BOT_NEMR" > /root/webapp/bot_nemr.log 2>&1 &
    NEMR_PID=$!
    echo "  PID: $NEMR_PID"
    echo "  Log: /root/webapp/bot_nemr.log"
    echo ""
    
    # Start Eng bot in background
    echo -e "${BLUE}→ Starting Eng_Crypto bot...${NC}"
    nohup "$VENV_PYTHON" "$BOT_ENG" > /root/webapp/bot_eng.log 2>&1 &
    ENG_PID=$!
    echo "  PID: $ENG_PID"
    echo "  Log: /root/webapp/bot_eng.log"
    echo ""
    
    echo -e "${GREEN}✓ Both bots started in background${NC}"
    echo ""
    echo "To view logs:"
    echo "  tail -f /root/webapp/bot_nemr.log"
    echo "  tail -f /root/webapp/bot_eng.log"
    echo ""
    echo "To stop bots:"
    echo "  kill $NEMR_PID $ENG_PID"
    
else
    echo -e "${YELLOW}Starting bots in FOREGROUND mode...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop both bots${NC}"
    echo ""
    
    # Create a trap to kill both processes on Ctrl+C
    trap 'echo ""; echo "Stopping bots..."; kill $NEMR_PID $ENG_PID 2>/dev/null; exit' INT TERM
    
    # Start Nemr bot in background (but monitor in foreground)
    echo -e "${BLUE}→ Starting Nemr_AI bot...${NC}"
    "$VENV_PYTHON" "$BOT_NEMR" 2>&1 | sed 's/^/[NEMR] /' &
    NEMR_PID=$!
    
    # Start Eng bot in background (but monitor in foreground)
    echo -e "${BLUE}→ Starting Eng_Crypto bot...${NC}"
    "$VENV_PYTHON" "$BOT_ENG" 2>&1 | sed 's/^/[ENG] /' &
    ENG_PID=$!
    
    echo ""
    echo -e "${GREEN}✓ Both bots running (PIDs: Nemr=$NEMR_PID, Eng=$ENG_PID)${NC}"
    echo ""
    
    # Wait for both processes
    wait $NEMR_PID $ENG_PID
fi
