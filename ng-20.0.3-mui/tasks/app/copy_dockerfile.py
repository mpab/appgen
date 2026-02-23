COMPONENT_NAME='home.component'

def description(ctx):
    return f'copy Dockerfile'

def exec(ctx):
    ctx.copy_file(f'{ctx.TEMPLATE_PATH}/Dockerfile', f'{ctx.APP_APP_PATH}/Dockerfile')
    ctx.copy_file(f'{ctx.TEMPLATE_PATH}/.dockerignore', f'{ctx.APP_APP_PATH}/.dockerignore')
