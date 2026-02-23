TS_NAME='.service.ts'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{TS_NAME}'


def exec(ctx):
    with open(f'{ctx.PAGE_TEMPLATE_PATH}/xxxx-crud{TS_NAME}', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('__ENTITY_PASCAL__', ctx.ENTITY_PASCAL)
    filedata = filedata.replace('__ENTITY_KEBAB__', ctx.ENTITY_KEBAB)
    filedata = filedata.replace('__ENTITY_ID__', ctx.ENTITY_ID)
    filedata = filedata.replace('__API_URL__', ctx.API_URL)
    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}', filedata)
