import shutil


def description(ctx):
    return f"copy common database files"


def exec(ctx):

    shutil.copytree(
        f"{ctx.COMPONENTS_DB_PATH}/app",
        f"{ctx.APP_DATABASE_PATH}",
        dirs_exist_ok=True,
    )
