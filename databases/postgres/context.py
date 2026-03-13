import os
import os.path
import sys
from pathlib import Path

# set global context
appgen_dir = f'{os.environ["__APPGEN_HOME__"]}'
# print(f"appgen_dir {appgen_dir}")
sys.path.append(appgen_dir)
import app.context


class PostgresContext:
    def description(ctx):
        return "create database context"

    # TODO: clone folder structure
    def exec(ctx):
        ctx.read_opts()

        # hack to support no schema, moved to main Context
        # target paths
        # ctx.APP_DATABASE_SCRIPTS_PATH = f"{ctx.APP_DATABASE_PATH}/scripts"
        # ctx.ensure_folder(ctx.APP_DATABASE_SCRIPTS_PATH)

        # ctx.APP_DATABASE_CSV_SEED_PATH = f"{ctx.APP_DATABASE_PATH}/csv_seed"
        # ctx.ensure_folder(ctx.APP_DATABASE_CSV_SEED_PATH)

        # ctx.APP_DATABASE_SQL_PATH = f"{ctx.APP_DATABASE_PATH}/sql"
        # ctx.ensure_folder(ctx.APP_DATABASE_SQL_PATH)

        # docker barfs on MacOS if not present?
        # ctx.POSTGRES_VOLUME = f"./pgdata"
        # ctx.ensure_folder(ctx.POSTGRES_VOLUME)


def create(job):
    ctx = app.context.Context
    ctx.set_job(job)
    ctx.exec(PostgresContext)
    return ctx
