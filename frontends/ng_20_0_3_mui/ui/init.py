import shutil


def description(ctx):
    return f"copy common frontend files"


def exec(ctx):

    shutil.copytree(
        f"{ctx.COMPONENTS_UI_PATH}/app-init",
        f"{ctx.APP_FRONTEND_PATH}",
        dirs_exist_ok=True,
    )
