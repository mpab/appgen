import os
import os.path
import sys
from pathlib import Path

# redirect to db context
ui_dir = f'{os.environ["__APPGEN_FE_PATH__"]}'
# print(f"ui_dir {ui_dir}")
sys.path.append(ui_dir)
import context


def create(job):
    return context.create(job)
