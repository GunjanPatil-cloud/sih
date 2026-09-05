import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(parent_dir, 'backend')

for path in [parent_dir, backend_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

from app import create_app

# Top-level application assignment for Vercel
app = create_app()
