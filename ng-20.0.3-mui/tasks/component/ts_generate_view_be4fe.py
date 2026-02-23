TS_NAME='.view.ts'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{TS_NAME}'

def exec(ctx):
    dto = ''

    for reference_entity in ctx.REFERENCES:
        names = ctx.from_snake(reference_entity)
        dto = dto + 'import { ' + names.PASCAL + 'Model }' + f" from '../{names.KEBAB}/{names.KEBAB}.model';\n"
        
    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    dto = dto + f'\nexport interface {ctx.ENTITY_PASCAL}View ' + '{\n'
    for idx in range(len(entity_fields) + 1):
        if (idx >= len(entity_fields)):  # terminal actions
            dto = dto + '};'
            break  # prevent out-of-bounds access
        field = entity_fields[idx]
        field_name = field.name
        if field_name in ctx.ENTITY_REF_MAP.keys():
            reference_entity = ctx.ENTITY_REF_MAP[field_name]
            names = ctx.from_snake(reference_entity)
            dto = dto + f'{ctx.TAB04}{reference_entity}: {names.PASCAL}Model,' + '\n'
            continue
        dto = dto + f'{ctx.TAB04}{field_name}: {field.js_type},' + '\n'

    ctx.save_data(f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}', dto)
