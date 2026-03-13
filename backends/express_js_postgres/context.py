import os
import os.path
import sys
from pathlib import Path

# set global context
appgen_dir = f'{os.environ["__APPGEN_HOME__"]}'
# print(f"appgen_dir {appgen_dir}")
sys.path.append(appgen_dir)
import app.context


class ExpressJsPostgresContext:
    def description(ctx):
        return "create api context for express_js_postgres"

    def exec(ctx):
        ctx.read_opts()

        # target paths
        ctx.APP_API_SRC_PATH = f"{ctx.APP_API_PATH}/src"
        ctx.APP_API_SRC_ENDPOINTS_PATH = f"{ctx.APP_API_SRC_PATH}/endpoints"
        ctx.API_DOCS_PATH = f"{ctx.APP_API_PATH}/docs"

        # components
        ctx.COMPONENTS_API_PATH = f'{os.environ["__APPGEN_API_PATH__"]}/components'
        ctx.COMPONENTS_API_ENDPOINTS_PATH = f"{ctx.COMPONENTS_API_PATH}/api-endpoints"


def create(job):
    ctx = app.context.Context
    ctx.set_job(job)
    ctx.exec(ExpressJsPostgresContext)
    return ctx
