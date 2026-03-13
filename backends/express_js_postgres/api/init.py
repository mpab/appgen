import shutil


def description(ctx):
    return f"copy common api files"


def exec(ctx):

    shutil.copytree(
        f"{ctx.COMPONENTS_API_PATH}/app", f"{ctx.APP_API_PATH}", dirs_exist_ok=True
    )
