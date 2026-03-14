import os
import os.path
import sys
from pathlib import Path

# redirect to db context
db_dir = f'{os.environ["__APPGEN_DB_PATH__"]}'
# print(f"db_dir {db_dir}")
sys.path.append(db_dir)
import context


class AppContext:
    def description(ctx):
        return "create app context for appgen"

    def exec(ctx):
        ctx.read_opts()


def create(job):
    ctx = context.Context
    ctx.set_job(job)
    ctx.exec(AppContext)
    return ctx
