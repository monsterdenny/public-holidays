#!/bin/bash

# Script to run all Python holiday crawler scripts in src/
# Usage: ./run-all.sh [COUNTRY_CODE]
#   If COUNTRY_CODE is provided (3 characters), runs only that script
#   If no argument, runs all scripts

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${SCRIPT_DIR}/src"

# Check if src directory exists
if [ ! -d "$SRC_DIR" ]; then
  echo "Error: src/ directory not found at $SRC_DIR"
  exit 1
fi

# Change to src directory
cd "$SRC_DIR"

# If country code argument is provided
if [ $# -gt 0 ]; then
  country_code="$1"
  
  # Validate country code is 3 characters
  if [ ${#country_code} -ne 3 ]; then
    echo "Error: Country code must be exactly 3 characters (e.g., USA, GBR, CHN)"
    exit 1
  fi
  
  # Convert to lowercase and construct script filename
  script_name=$(echo "$country_code" | tr '[:upper:]' '[:lower:]').py
  
  # Check if script exists
  if [ ! -f "$script_name" ]; then
    echo "Error: Script '$script_name' not found in src/ directory"
    echo "Available scripts:"
    ls -1 *.py 2>/dev/null | grep -v "^test.py$" | grep -v "^functions.py$" | grep -v "\.disabled$" | sed 's/^/  - /' || echo "  (none found)"
    exit 1
  fi
  
  # Skip if it's test.py, functions.py, or disabled
  if [ "$script_name" = "test.py" ] || [ "$script_name" = "functions.py" ] || [[ "$script_name" == *.disabled ]]; then
    echo "Error: Cannot run '$script_name' (test/utility/disabled script)"
    exit 1
  fi
  
  # Run the specific script
  echo "Running $script_name..."
  echo "======================================"
  echo ""
  
  if python3 "$script_name"; then
    echo ""
    echo "✓ $script_name completed successfully"
    exit 0
  else
    echo ""
    echo "✗ $script_name failed with error"
    exit 1
  fi
fi

# No argument provided - run all scripts
echo "Running all holiday crawler scripts..."
echo "======================================"
echo ""

# Counter for tracking
success_count=0
error_count=0

# Find all Python scripts except test.py, functions.py, and disabled files
for script in *.py; do
  # Skip if file doesn't exist (e.g., if no .py files match)
  [ ! -f "$script" ] && continue
  
  # Skip test.py, functions.py, and any .disabled files
  if [ "$script" = "test.py" ] || [ "$script" = "functions.py" ] || [[ "$script" == *.disabled ]]; then
    continue
  fi
  
  echo "Running $script..."
  echo "--------------------------------------"
  
  if python3 "$script"; then
    echo "✓ $script completed successfully"
    ((success_count++))
  else
    echo "✗ $script failed with error"
    ((error_count++))
  fi
  
  echo ""
done

echo "======================================"
echo "Summary:"
echo "  Successful: $success_count"
echo "  Failed: $error_count"
echo ""

if [ $error_count -gt 0 ]; then
  exit 1
fi

