COMPONENT_NAME='alert.component'

def description(ctx):
    return f'copy {COMPONENT_NAME} files'

def exec(ctx):
    ctx.HOME_PAGE_TEMPLATE_PATH = f'{ctx.TEMPLATE_PATH}/{COMPONENT_NAME}'
    ctx.GENERATED_ENTITY_PATH = f'{ctx.APP_COMPONENTS_PATH}/{COMPONENT_NAME}'
    ctx.ensure_folder(ctx.GENERATED_ENTITY_PATH)
    copy_file(ctx, f'{COMPONENT_NAME}.css')
    copy_file(ctx, f'{COMPONENT_NAME}.html')
    copy_file(ctx, f'{COMPONENT_NAME}.spec.ts')
    copy_file(ctx, f'{COMPONENT_NAME}.ts')
    copy_file(ctx, 'alert.service.spec.ts')
    copy_file(ctx, 'alert.service.ts')

def copy_file(ctx, fname):
    ctx.copy_file(f'{ctx.HOME_PAGE_TEMPLATE_PATH}/{fname}', f'{ctx.GENERATED_ENTITY_PATH}/{fname}')