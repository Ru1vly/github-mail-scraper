#!/bin/bash
# Wrapper script to run the scraper CLI
cd "$(dirname "$0")"
export PYTHONPATH=src
exec python3 -m scraper.cli "$@"
