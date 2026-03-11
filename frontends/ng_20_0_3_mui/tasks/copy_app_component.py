def description(ctx):
    return f"copy app component and associated files"


def exec(ctx):
    copy_file(ctx, "app.css")
    copy_file(ctx, "app.html")
    copy_file(ctx, "app.spec.ts")
    copy_file(ctx, "app.ts")
    copy_file(ctx, "app.config.ts")
    copy_file(ctx, "app.menu.ts")
    copy_file(ctx, "app.menu.json")
    copy_file(ctx, "app.routes.ts")


def copy_file(ctx, fname):
    ctx.copy_file(f"{ctx.APP_TEMPLATE_PATH}/{fname}", f"{ctx.APP_APP_PATH}/{fname}")
