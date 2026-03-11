import os
import sys
from pathlib import Path

project_stack_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_stack_dir))
import common.project_context


class FrontendContext:
    def description(ctx):
        return "create frontend context"

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
        ctx.ensure_folder(ctx.APP_APP_PATH)

        ctx.APP_COMPONENTS_PATH = f"{ctx.FRONTEND_PATH}/src/components"
        ctx.ensure_folder(ctx.APP_COMPONENTS_PATH)

        ctx.APP_PAGES_PATH = f"{ctx.FRONTEND_PATH}/src/pages"
        ctx.ensure_folder(ctx.APP_PAGES_PATH)


def create(job):
    ctx = common.project_context.Context
    ctx.set_job(job)
    ctx.exec(FrontendContext)
    return ctx
