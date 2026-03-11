TS_NAME='.routes.ts'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{TS_NAME}'

def exec(ctx):
    with open(f'{ctx.PAGE_TEMPLATE_PATH}/xxxx-crud.routes.ts', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('__ENTITY_PASCAL__', ctx.ENTITY_PASCAL)
    filedata = filedata.replace('__ENTITY_KEBAB__', ctx.ENTITY_KEBAB)
    filedata = filedata.replace(
        '__ENTITY_SNAKE_UCASE__', ctx.ENTITY_SNAKE_UCASE)
    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}', filedata)
