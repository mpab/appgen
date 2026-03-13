import shutil


def description(ctx):
    return f"customize frontend files"


def exec(ctx):

    shutil.copytree(
        f"{ctx.COMPONENTS_UI_PATH}/app-customize",
        f"{ctx.APP_FRONTEND_PATH}",
        dirs_exist_ok=True,
    )
