import os


def description(ctx):
    return f"copy database seed template files"


def exec(ctx):
    ctx.copy_file(
        f"{ctx.COMPONENTS_DB}/recreate-tables",
        f"{ctx.DATABASE_SCRIPTS_PATH}/recreate-tables",
    )
    ctx.copy_file(
        f"{ctx.COMPONENTS_DB}/seed-tables",
        f"{ctx.DATABASE_SCRIPTS_PATH}/seed-tables",
    )
