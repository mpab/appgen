import os
import os.path
import sys
from pathlib import Path

# set global context
appgen_dir = f'{os.environ["__APPGEN_HOME__"]}'
# print(f"appgen_dir {appgen_dir}")
sys.path.append(appgen_dir)
import app.context


class ng_20_0_3_muiContext:
    def description(ctx):
        return "create frontend context for ng_20_0_3_mui"

    def exec(ctx):
        ctx.read_opts()

        ctx.COMPONENTS_STACK_PATH = f'{os.environ["__APPGEN_FE_PATH__"]}/components'
        ctx.FRONTEND_TEMPLATE_PATH = f"{ctx.COMPONENTS_STACK_PATH}/frontend"
        ctx.APP_TEMPLATE_PATH = f"{ctx.COMPONENTS_STACK_PATH}/app"
        ctx.PAGE_TEMPLATE_PATH = f"{ctx.COMPONENTS_STACK_PATH}/page"
        ctx.PAGE_BE4FE_PAGED_TEMPLATE_PATH = (
            f"{ctx.COMPONENTS_STACK_PATH}/page-be4fe-paged"
        )

        ctx.FRONTEND_PATH = ctx.match_opt_prefix_or_default(
            "--frontend-path=", "./frontend"
        )
        ctx.ensure_folder(ctx.FRONTEND_PATH)

        ctx.APP_APP_PATH = f"{ctx.FRONTEND_PATH}/src/app"
        ctx.ensure_folders(ctx.APP_APP_PATH)

        ctx.APP_COMPONENTS_PATH = f"{ctx.FRONTEND_PATH}/src/components"
        ctx.ensure_folders(ctx.APP_COMPONENTS_PATH)

        ctx.APP_PAGES_PATH = f"{ctx.FRONTEND_PATH}/src/pages"
        ctx.ensure_folders(ctx.APP_PAGES_PATH)


def create(job):
    ctx = app.context.Context
    ctx.set_job(job)
    ctx.exec(ng_20_0_3_muiContext)
    return ctx
