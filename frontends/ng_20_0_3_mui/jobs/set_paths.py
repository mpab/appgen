#!/usr/bin/env python

import os
import os.path
import sys
from pathlib import Path

frontends_stack_dir = Path(__file__).resolve().parent.parent.parent
print(f"frontends_stack_dir {frontends_stack_dir}")
sys.path.append(str(frontends_stack_dir))
