#!/usr/bin/env python

import os
import os.path
import sys
from pathlib import Path

appgen_dir = Path(__file__).resolve().parent.parent.parent
backends_stack_dir = os.path.join(appgen_dir, "backends")
# print(f"backends_stack_dir {backends_stack_dir}")
sys.path.append(str(backends_stack_dir))
