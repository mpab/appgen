TS_NAME = "app.routes.ts"


def description(ctx):
    return f"merge routes into: {TS_NAME}"


def exec(ctx):
    app_routes_fp = f"{ctx.APP_APP_PATH}/{TS_NAME}"
    with open(app_routes_fp, "r") as file:
        filedata = file.read()
    if f"{ctx.ENTITY_SNAKE_UCASE}_ROUTES" in filedata:
        ctx.info(f"found {ctx.ENTITY_SNAKE_UCASE}_ROUTES in {app_routes_fp}, skipping")
    else:
        ctx.info(f"inserting {ctx.ENTITY_SNAKE_UCASE}_ROUTES in {app_routes_fp}")
        cut_idx = filedata.rfind("];")
        if cut_idx:
            filedata = filedata[:cut_idx]
        route = (
            "    , {"
            + f" path: '{ctx.ENTITY_PASCAL_SPACED_NO_ENUM}', loadChildren: () => import('../pages/{ctx.ENTITY_KEBAB}/{ctx.ENTITY_KEBAB}.routes').then(m => m.{ctx.ENTITY_SNAKE_UCASE}_ROUTES)"
            + " }"
        )
        filedata = filedata + route + "\n];"
    ctx.save_data(app_routes_fp, filedata)
