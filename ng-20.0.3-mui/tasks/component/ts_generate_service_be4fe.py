TS_NAME='-api.service.ts'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{TS_NAME}'


def exec(ctx):
    entity_references_declarations = []

    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        field_name = field.name
        if field_name in ctx.ENTITY_REF_MAP.keys():
            reference_entity = ctx.ENTITY_REF_MAP[field_name]
            names = ctx.from_snake(reference_entity)
            entity_references_declarations.append(f'{ctx.TAB16}{reference_entity}: [],')

    with open(f'{ctx.PAGE_TEMPLATE_PATH}/be4fe-crud.service.ts', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('__API_UUID__', ctx.API_UUID)
    filedata = filedata.replace('__ENTITY_PASCAL__', ctx.ENTITY_PASCAL)
    filedata = filedata.replace('__ENTITY_SNAKE__', ctx.ENTITY_SNAKE)
    filedata = filedata.replace('__ENTITY_KEBAB__', ctx.ENTITY_KEBAB)
    filedata = filedata.replace('__ENTITY_ID__', ctx.ENTITY_ID)
    filedata = filedata.replace('__API_URL__', ctx.API_URL)

    filedata = filedata.replace(
        '__ENTITY_REFERENCES_DECLARATIONS__', '\n'.join(map(str, entity_references_declarations)))

    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}', filedata)
