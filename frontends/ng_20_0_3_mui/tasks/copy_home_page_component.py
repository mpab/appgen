COMPONENT_NAME = "home.component"


def description(ctx):
    return f"copy {COMPONENT_NAME} files"


def exec(ctx):
    ctx.HOME_PAGE_TEMPLATE_PATH = f"{ctx.COMPONENTS_STACK_PATH}/{COMPONENT_NAME}"
    ctx.GENERATED_ENTITY_PATH = f"{ctx.APP_PAGES_PATH}/{COMPONENT_NAME}"
    ctx.ensure_folder(ctx.GENERATED_ENTITY_PATH)
    copy_file(ctx, f"{COMPONENT_NAME}.css")
    copy_file(ctx, f"{COMPONENT_NAME}.html")
    copy_file(ctx, f"{COMPONENT_NAME}.spec.ts")
    copy_file(ctx, f"{COMPONENT_NAME}.ts")


def copy_file(ctx, fname):
    ctx.copy_file(
        f"{ctx.HOME_PAGE_TEMPLATE_PATH}/{fname}", f"{ctx.GENERATED_ENTITY_PATH}/{fname}"
    )
