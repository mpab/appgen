import os
import sys
from pathlib import Path

project_stack_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_stack_dir))
import project.project_context


class FrontendContext:
    def description(ctx):
        return "create frontend context"

    def exec(ctx):
        ctx.read_opts()

        ctx.TEMPLATE_PATH = f'{os.environ["__APPGEN_PROFILE_FE_PATH__"]}/components'
        ctx.APP_TEMPLATE_PATH = f"{ctx.TEMPLATE_PATH}/app"
        ctx.PAGE_TEMPLATE_PATH = f"{ctx.TEMPLATE_PATH}/page"
        ctx.PAGE_BE4FE_PAGED_TEMPLATE_PATH = f"{ctx.TEMPLATE_PATH}/page-be4fe-paged"

        FRONTEND_PATH = ctx.match_opt_prefix_or_default(
            "--frontend-path=", "./frontend"
        )
        ctx.ensure_folder(FRONTEND_PATH)

        ctx.APP_APP_PATH = f"{FRONTEND_PATH}"
        ctx.APP_COMPONENT_PATH = f"{ctx.APP_APP_PATH}/src/app"
        ctx.APP_COMPONENTS_PATH = f"{ctx.APP_APP_PATH}/src/components"
        ctx.APP_PAGES_PATH = f"{ctx.APP_APP_PATH}/src/pages"

        # ensure paths, barf if error
        ctx.ensure_folder(ctx.APP_COMPONENT_PATH)
        ctx.ensure_folder(ctx.APP_COMPONENTS_PATH)
        ctx.ensure_folder(ctx.APP_PAGES_PATH)


def create(job):
    ctx = project.project_context.Context
    ctx.set_job(job)
    ctx.exec(FrontendContext)
    return ctx
