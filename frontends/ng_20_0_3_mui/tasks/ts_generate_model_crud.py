TS_NAME='.model.ts'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{TS_NAME}'

def exec(ctx):
    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    dto = f'export interface {ctx.ENTITY_PASCAL}Model ' + '{\n'
    for idx in range(len(entity_fields) + 1):
        if (idx >= len(entity_fields)):  # terminal actions
            dto = dto + '};'
            break  # prevent out-of-bounds access
        field = entity_fields[idx]
        field_name = field.name
        dto = dto + f'{ctx.TAB04}{field_name}: {field.js_type},' + '\n'

    ctx.save_data(f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}', dto)
