import os


def description(ctx):
    return f"copy initial database files"


def exec(ctx):
    ctx.copy_file(
        f"{ctx.TEMPLATE_DATABASE_PATH}/recreate-tables",
        f"{ctx.DATABASE_SCRIPTS_PATH}/recreate-tables",
    )
    ctx.copy_file(
        f"{ctx.TEMPLATE_DATABASE_PATH}/seed-tables",
        f"{ctx.DATABASE_SCRIPTS_PATH}/seed-tables",
    )
    ctx.copy_file(
        f"{ctx.TEMPLATE_DATABASE_PATH}/.gitignore",
        ".gitignore",
    )
    # ctx.copy_file(f'{ctx.TEMPLATE_DATABASE_PATH}/database-name', f'{ctx.DATABASE_SCRIPTS_PATH}/database-name')
