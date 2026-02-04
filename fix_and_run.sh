#!/bin/bash
################################################################################
# PYTHON BOT ENVIRONMENT FIX & LAUNCH SCRIPT
# Purpose: Fix PEP 668 externally-managed-environment errors and venv issues
# Author: GenSpark AI
# Date: 2026-02-04
################################################################################

set -e  # Exit on any error
set -u  # Exit on undefined variables

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  PYTHON BOT ENVIRONMENT FIX & DEPLOYMENT SCRIPT          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Ensure we're in the correct directory
cd /root/webapp
PROJECT_DIR="/root/webapp"
VENV_DIR="${PROJECT_DIR}/venv"

################################################################################
# STEP 1: Update apt repositories
################################################################################
echo -e "${YELLOW}[STEP 1/7]${NC} Updating apt repositories..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq || {
    echo -e "${RED}✗ Failed to update apt repositories${NC}"
    exit 1
}
echo -e "${GREEN}✓ Apt repositories updated${NC}"
echo ""

################################################################################
# STEP 2: Install system dependencies
################################################################################
echo -e "${YELLOW}[STEP 2/7]${NC} Installing system dependencies..."
echo "  → python3-pip"
echo "  → python3-venv"
echo "  → python3-full"
echo "  → python3-dev"
echo "  → build-essential"

apt-get install -y -qq \
    python3-pip \
    python3-venv \
    python3-full \
    python3-dev \
    build-essential \
    curl \
    git || {
    echo -e "${RED}✗ Failed to install system dependencies${NC}"
    exit 1
}
echo -e "${GREEN}✓ System dependencies installed${NC}"
echo ""

################################################################################
# STEP 3: Remove broken venv if it exists
################################################################################
echo -e "${YELLOW}[STEP 3/7]${NC} Cleaning up broken virtual environment..."
if [ -d "$VENV_DIR" ]; then
    echo "  → Found existing venv at: $VENV_DIR"
    echo "  → Removing broken venv..."
    rm -rf "$VENV_DIR"
    echo -e "${GREEN}✓ Broken venv removed${NC}"
else
    echo "  → No existing venv found (this is fine)"
fi
echo ""

################################################################################
# STEP 4: Create new clean virtual environment
################################################################################
echo -e "${YELLOW}[STEP 4/7]${NC} Creating new virtual environment..."
python3 -m venv "$VENV_DIR" || {
    echo -e "${RED}✗ Failed to create virtual environment${NC}"
    echo "Debugging information:"
    python3 --version
    python3 -m venv --help
    exit 1
}
echo -e "${GREEN}✓ Virtual environment created at: $VENV_DIR${NC}"
echo ""

################################################################################
# STEP 5: Activate environment and upgrade pip
################################################################################
echo -e "${YELLOW}[STEP 5/7]${NC} Activating environment and upgrading pip..."
source "$VENV_DIR/bin/activate" || {
    echo -e "${RED}✗ Failed to activate virtual environment${NC}"
    exit 1
}

# Upgrade pip to latest version
pip install --upgrade pip setuptools wheel -q || {
    echo -e "${RED}✗ Failed to upgrade pip${NC}"
    exit 1
}
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo -e "${GREEN}✓ Pip upgraded to latest version${NC}"
echo ""

################################################################################
# STEP 6: Install Python dependencies
################################################################################
echo -e "${YELLOW}[STEP 6/7]${NC} Installing Python dependencies..."
echo "  → requests"
echo "  → schedule"
echo "  → pytrends"

pip install requests schedule pytrends -q || {
    echo -e "${RED}✗ Failed to install Python dependencies${NC}"
    exit 1
}
echo -e "${GREEN}✓ All Python dependencies installed${NC}"
echo ""

# Verify installations
echo "Verifying installed packages:"
pip list | grep -E "(requests|schedule|pytrends)" || true
echo ""

################################################################################
# STEP 7: Create launcher script
################################################################################
echo -e "${YELLOW}[STEP 7/7]${NC} Creating bot launcher script..."

cat > "${PROJECT_DIR}/launch_bots.sh" << 'LAUNCHER_EOF'
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
LAUNCHER_EOF

chmod +x "${PROJECT_DIR}/launch_bots.sh"
echo -e "${GREEN}✓ Launcher script created: ${PROJECT_DIR}/launch_bots.sh${NC}"
echo ""

################################################################################
# SUMMARY
################################################################################
echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║               SETUP COMPLETE!                            ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Environment Details:${NC}"
echo "  Python executable: ${VENV_DIR}/bin/python3"
echo "  Virtual environment: ${VENV_DIR}"
echo "  Launcher script: ${PROJECT_DIR}/launch_bots.sh"
echo ""
echo -e "${GREEN}Installed Packages:${NC}"
pip freeze | grep -E "(requests|schedule|pytrends)" || echo "  (package list unavailable)"
echo ""
echo -e "${YELLOW}To launch your bots:${NC}"
echo ""
echo "  ${GREEN}Foreground mode${NC} (see output, press Ctrl+C to stop):"
echo "    ./launch_bots.sh"
echo ""
echo "  ${GREEN}Background mode${NC} (runs in background):"
echo "    ./launch_bots.sh background"
echo ""
echo -e "${YELLOW}Quick test:${NC}"
echo "  ${VENV_DIR}/bin/python3 -c 'import requests, schedule; from pytrends.request import TrendReq; print(\"✓ All imports successful!\")'"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
