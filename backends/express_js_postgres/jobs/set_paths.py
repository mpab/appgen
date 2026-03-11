#!/usr/bin/env python

import os
import os.path
import sys
from pathlib import Path

backends_stack_dir = Path(__file__).resolve().parent.parent.parent
print(f"backends_stack_dir {backends_stack_dir}")
sys.path.append(str(backends_stack_dir))
