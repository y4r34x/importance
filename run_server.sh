#!/bin/bash
# Run Flask server using venv's Python directly
cd "$(dirname "$0")"
./venv/bin/python3 app.py
