import os
import os.path
import sys
from pathlib import Path

# set this context
context_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(context_dir))

# set global context
appgen_dir = Path(__file__).resolve().parent.parent.parent
stack_dir = str(appgen_dir)
print(f"appgen_dir {appgen_dir}")
sys.path.append(str(appgen_dir))
import common.project_context


class PostgresContext:
    def description(ctx):
        return "create postgres context"

    def exec(ctx):
        ctx.read_opts()


def create(job):
    ctx = common.project_context.Context
    ctx.set_job(job)
    ctx.exec(PostgresContext)
    return ctx
