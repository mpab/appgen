import os
import os.path
import sys
from pathlib import Path

# redirect to db context
db_dir = f'{os.environ["__APPGEN_DB_PATH__"]}'
# print(f"db_dir {db_dir}")
sys.path.append(db_dir)
import context


def create(job):
    return context.create(job)
