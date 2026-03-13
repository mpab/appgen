import os
import os.path
import sys
from pathlib import Path

# redirect to api context
api_dir = f'{os.environ["__APPGEN_API_PATH__"]}'
# print(f"api_dir {api_dir}")
sys.path.append(api_dir)
import context


def create(job):
    return context.create(job)
