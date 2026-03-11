def description(ctx):
    return f"copy initial api files"


def exec(ctx):
    copy_api_src_file(ctx, "index.js")
    copy_api_src_file(ctx, "endpoints.js")
    copy_api_src_file(ctx, "response.js")
    copy_api_src_file(ctx, "database.js")
    copy_api_src_file(ctx, "swagger-autogen.js")
    copy_endpoint_file(ctx, "info.js")
    ctx.copy_file(
        f"{ctx.COMPONENTS_API_PATH}/swagger.json", f"{ctx.API_DOCS_PATH}/swagger.json"
    )

    copy_app_file(ctx, ".dockerignore")
    copy_app_file(ctx, ".env")
    copy_app_file(ctx, ".gitignore")
    copy_app_file(ctx, "Dockerfile")
    copy_app_file(ctx, "mise.toml")


def copy_app_file(ctx, fname):
    ctx.copy_file(f"{ctx.COMPONENTS_APP_PATH}/{fname}", f"{ctx.API_APP_PATH}/{fname}")


def copy_api_src_file(ctx, fname):
    ctx.copy_file(
        f"{ctx.COMPONENTS_API_PATH}/{fname}", f"{ctx.API_APP_SRC_PATH}/{fname}"
    )


def copy_endpoint_file(ctx, fname):
    ctx.copy_file(
        f"{ctx.COMPONENTS_API_ENDPOINTS_PATH}/{fname}",
        f"{ctx.API_APP_SRC_ENDPOINTS_PATH}/{fname}",
    )
