#!/usr/bin/env bash
# pass_gen.sh
# Hacker-style launcher for Password Generator (GUI or CLI)
# Author: Sudo-xdk (Dhanush)
# GitHub: https://github.com/Sudo-xdk

set -euo pipefail

# --- banner (figlet) ---
if ! command -v figlet >/dev/null 2>&1; then
  echo "figlet not found. Attempting to install (requires sudo/apt)..."
  if command -v apt >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1; then
    sudo apt update -y && sudo apt install -y figlet
  else
    echo "Warning: cannot auto-install figlet. Install it for the fancy banner: sudo apt install figlet"
  fi
fi

# Use figlet if available, otherwise simple ASCII
if command -v figlet >/dev/null 2>&1; then
  figlet -f slant "Pass_Gen"
else
  echo "  ____            _            _     _    _ _    "
  echo " / ___| _   _  __| | ___  _ __| | __| |  | | | __"
  echo " \___ \| | | |/ _\` |/ _ \| '__| |/ _\` |  | | |/ /"
  echo "  ___) | |_| | (_| | (_) | |  | | (_| |  | |   < "
  echo " |____/ \__,_|\__,_|\___/|_|  |_|\__,_|  |_|_|\_\\"
  echo "                                                 "
  echo "              Sudo_xdk"
fi

# Colored author/info lines
BLUE="\033[1;34m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RESET="\033[0m"

echo -e "${BLUE}Author:${RESET} Sudo-xdk (Dhanush)  ${BLUE}|${RESET} GitHub: https://github.com/Sudo-xdk"
echo -e "${GREEN}🔐 Secure Password Generator${RESET}"
echo ""

# Check for python3
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  echo -e "${YELLOW}Error:${RESET} No python3 or python found in PATH. Install Python 3.8+ and retry."
  exit 1
fi

# Ensure script exists
PYTHON_SCRIPT="password_generator.py"
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo -e "${YELLOW}Error:${RESET} ${PYTHON_SCRIPT} not found in current directory ($(pwd))."
  exit 1
fi

# If Streamlit available, run GUI. else fallback to running the script directly.
if "$PYTHON_CMD" -c "import importlib, sys, json
try:
    importlib.import_module('streamlit')
    sys.stdout.write('yes')
except Exception:
    sys.stdout.write('no')
" 2>/dev/null | grep -q "yes"; then
  echo "Streamlit detected — launching GUI..."
  # Use python -m streamlit to avoid missing streamlit executable on PATH
  exec "$PYTHON_CMD" -m streamlit run "$PYTHON_SCRIPT" "$@"
else
  echo "Streamlit not found — running script directly with Python (CLI mode)."
  exec "$PYTHON_CMD" "$PYTHON_SCRIPT" "$@"
fi
