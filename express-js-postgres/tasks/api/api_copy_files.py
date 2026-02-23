def description(ctx):
    return f"copy initial api files"


def exec(ctx):
    copy_api_file(ctx, "index.js")
    copy_api_file(ctx, "endpoints.js")
    copy_api_file(ctx, "response.js")
    copy_api_file(ctx, "database.js")
    copy_api_file(ctx, "swagger-autogen.js")
    copy_api_file(ctx, ".gitignore")
    copy_endpoint_file(ctx, "info.js")
    ctx.copy_file(
        f"{ctx.TEMPLATE_API_PATH}/swagger.json", f"{ctx.API_DOCS_PATH}/swagger.json"
    )
    ctx.copy_file(f"{ctx.TEMPLATE_PATH}/Dockerfile", f"{ctx.API_APP_PATH}/Dockerfile")
    ctx.copy_file(
        f"{ctx.TEMPLATE_PATH}/.dockerignore", f"{ctx.API_APP_PATH}/.dockerignore"
    )


def copy_api_file(ctx, fname):
    ctx.copy_file(f"{ctx.TEMPLATE_API_PATH}/{fname}", f"{ctx.API_PATH}/{fname}")


def copy_endpoint_file(ctx, fname):
    ctx.copy_file(
        f"{ctx.TEMPLATE_ENDPOINTS_PATH}/{fname}", f"{ctx.API_ENDPOINTS_PATH}/{fname}"
    )
