#!/usr/bin/env python3
"""
Backward compatibility wrapper for lego_mosaic.py

This file maintains backward compatibility for users who run:
    python lego_mosaic.py [args]

The actual implementation is now in styles/lego_mosaic.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the actual implementation
from styles.lego_mosaic import main

if __name__ == '__main__':
    main()
