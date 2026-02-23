HTML_NAME='-form.component.html'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{HTML_NAME}'

def exec(ctx):
    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    enum_key = entity_fields[1].name
    enum_names = ctx.from_snake(enum_key)

    form_template_fragments = []

    with open(f'{ctx.PAGE_TEMPLATE_PATH}/xxxx-crud-form-fragment-text.component.html', 'r') as file:
        text_fragment = file.read()
    
    for field_idx, field in enumerate(entity_fields):
        if field.data_type == 'entity_id':  continue # skip ID
        elif field.data_type == 'text': fragment = text_fragment
        else:
            ctx.error(str(field))
            ctx.fatal(f'unhandled data_type: {field.data_type}')

        fragment = fragment.replace('__KEY_IDX__', f'{field_idx}')
        fragment = fragment.replace('__KEY__', field.name)

        form_template_fragments.append(fragment)

    with open(f'{ctx.PAGE_TEMPLATE_PATH}/xxxx-crud-form.component.html', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(
        '__ENTITY_PASCAL_SPACED_NO_ENUM__', ctx.ENTITY_PASCAL_SPACED_NO_ENUM)
    filedata = filedata.replace(
        '__KEY_PASCAL_SPACED_NO_ENUM__', enum_names.PASCAL_SPACED_NO_ENUM)
    filedata = filedata.replace(
        '__FORM_TEMPLATE_FRAGMENTS__', '\n'.join(map(str, form_template_fragments)))
    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{HTML_NAME}', filedata)
