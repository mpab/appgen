import shutil


def description(ctx):
    return f"copy common app files"


def exec(ctx):

    shutil.copytree(
        f"{ctx.COMPONENTS_APP_PATH}/app",
        f"{ctx.APP_APP_PATH}",
        dirs_exist_ok=True,
    )
