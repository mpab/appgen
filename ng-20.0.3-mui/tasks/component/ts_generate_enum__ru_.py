TS_NAME='enum-_ru_.component.ts'

def description(ctx):
    return f'generate: {TS_NAME}=>{ctx.ENTITY_KEBAB}.component.ts'


def exec(ctx):
    entity_initializer = []
    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        entity_init = ctx.TAB16 + f"{field.name}: {field.js_init},"
        entity_initializer.append(entity_init)

    enum_key = entity_fields[1].name
    with open(f'{ctx.PAGE_TEMPLATE_PATH}/{TS_NAME}', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('__ENTITY_PASCAL__', ctx.ENTITY_PASCAL)
    filedata = filedata.replace('__ENTITY_CAMEL__', ctx.ENTITY_CAMEL)
    filedata = filedata.replace('__ENTITY_KEBAB__', ctx.ENTITY_KEBAB)
    filedata = filedata.replace('__ENTITY_SNAKE__', ctx.ENTITY_SNAKE)
    filedata = filedata.replace('__ENTITY_ID__', ctx.ENTITY_ID)
    filedata = filedata.replace('__KEY__', enum_key)
    filedata = filedata.replace(
        '__ENTITY_INITIALIZER__', '\n'.join(map(str, entity_initializer)))
    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}.component.ts', filedata)
