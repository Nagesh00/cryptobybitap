import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

try:
    import pandas as pd
    print("✓ Pandas imported successfully")
except ImportError as e:
    print(f"✗ Pandas import failed: {e}")

try:
    import numpy as np
    print("✓ NumPy imported successfully")
except ImportError as e:
    print(f"✗ NumPy import failed: {e}")

try:
    from pybit.unified_trading import HTTP
    print("✓ PyBit imported successfully")
except ImportError as e:
    print(f"✗ PyBit import failed: {e}")

try:
    from utils.logger import setup_logger
    print("✓ Local logger imported successfully")
except ImportError as e:
    print(f"✗ Local logger import failed: {e}")
