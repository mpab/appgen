COMPONENT_NAME = "home.component"


def description(ctx):
    return f"copy Dockerfile"


def exec(ctx):
    ctx.copy_file(
        f"{ctx.FRONTEND_TEMPLATE_PATH}/Dockerfile", f"{ctx.FRONTEND_PATH}/Dockerfile"
    )
    ctx.copy_file(
        f"{ctx.FRONTEND_TEMPLATE_PATH}/.dockerignore",
        f"{ctx.FRONTEND_PATH}/.dockerignore",
    )
