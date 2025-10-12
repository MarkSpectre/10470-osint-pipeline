#!/usr/bin/env bash
# Unix-like setup script for OSINT Pipeline
# Usage: bash setup_unix.sh
set -euo pipefail
VENV_DIR="osint_env"

if ! command -v python3 &> /dev/null; then
  echo "python3 not found. Please install Python 3.10+ and try again." >&2
  exit 1
fi

python3 -m venv "$VENV_DIR"
# shellcheck source=/dev/null
. "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# NLTK downloads (optional)
python - <<'PY'
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
PY

echo "Setup complete. To activate the venv: source $VENV_DIR/bin/activate"
echo "Run 'python main.py' to collect data and 'python app.py' to start the web server."