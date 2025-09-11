#!/bin/bash
source ~/liquidity_engine/.venv/bin/activate
maturin develop
python -c "from liquidity_api import *; print(\"Liquidity Engine Ready\")"
