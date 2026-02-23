import os
import os.path
import sys
from pathlib import Path

project_stack_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_stack_dir))
import project.project_context


class BackendContext:
    def description(ctx):
        return "create backend context"

    def exec(ctx):
        ctx.read_opts()

        ctx.TEMPLATE_PATH = f'{os.environ["__APPGEN_PROFILE_BE_PATH__"]}/components'
        ctx.TEMPLATE_API_PATH = f"{ctx.TEMPLATE_PATH}/api"
        ctx.TEMPLATE_ENDPOINTS_PATH = f"{ctx.TEMPLATE_PATH}/api-endpoints"
        ctx.TEMPLATE_DATABASE_PATH = f"{ctx.TEMPLATE_PATH}/database"

        BACKEND_PATH = ctx.match_opt_prefix_or_default("--backend-path=", "./backend")
        ctx.ensure_folder(BACKEND_PATH)

        CONFIGURE_PATH = ctx.match_opt_prefix_or_default(
            "--configure-path=", "./configure"
        )
        ctx.ensure_folder(CONFIGURE_PATH)
        ctx.JSON_SCHEMA_PATH = f"{CONFIGURE_PATH}/schema"
        ctx.ensure_folder(ctx.JSON_SCHEMA_PATH)

        ctx.API_APP_PATH = f"{BACKEND_PATH}/api"
        ctx.API_PATH = f"{ctx.API_APP_PATH}/src"
        ctx.API_ENDPOINTS_PATH = f"{ctx.API_PATH}/endpoints"
        ctx.API_DOCS_PATH = f"{ctx.API_APP_PATH}/docs"
        ctx.DATABASE_PATH = f"{BACKEND_PATH}/database"
        ctx.DATABASE_SCRIPTS_PATH = f"{ctx.DATABASE_PATH}/scripts"
        ctx.DATABASE_SQL_PATH = f"{ctx.DATABASE_PATH}/sql"

        ctx.DATABASE_CSV_SEED_PATH = f"{ctx.DATABASE_PATH}/csv_seed"

        # ensure paths, barf if error
        ctx.ensure_folder(ctx.API_APP_PATH)
        ctx.ensure_folder(ctx.API_PATH)
        ctx.ensure_folder(ctx.API_ENDPOINTS_PATH)
        ctx.ensure_folder(ctx.API_DOCS_PATH)

        ctx.ensure_folder(ctx.DATABASE_PATH)
        ctx.ensure_folder(ctx.DATABASE_SCRIPTS_PATH)
        ctx.ensure_folder(ctx.DATABASE_SQL_PATH)

        ctx.ensure_folder(ctx.DATABASE_CSV_SEED_PATH)

        # docker barfs on MacOS if not present
        ctx.POSTGRES_VOLUME = f"./pgdata"
        ctx.ensure_folder(ctx.POSTGRES_VOLUME)


def create_for_init(job):
    ctx = project.project_context.Context
    ctx.set_job(job)
    ctx.exec(BackendContext)
    return ctx


def create(job):
    ctx = create_for_init(job)
    if not (ctx.read_opts()):
        ctx.fatal("arguments required")
    if not hasattr(ctx, "ENTITY_ARG"):
        ctx.fatal("file required")

    if not os.path.isfile(ctx.ENTITY_ARG):
        ctx.fatal(f"file {ctx.ENTITY_ARG} not found")

    ctx.ENTITY_FIELDS_STEM = "--entity-fields="

    ctx.TAB04 = "    "
    ctx.TAB08 = "        "
    ctx.TAB12 = "            "
    ctx.TAB16 = "                "

    ctx.TABLES_SQL = {}

    return ctx
