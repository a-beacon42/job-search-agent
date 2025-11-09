import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.db import init_db

if __name__ == "__main__":
    init_db()
