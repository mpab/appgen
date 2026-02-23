HTML_NAME='.component.html'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{HTML_NAME}'

def exec(ctx):
    table_template_fragments = []

    with open(f'{ctx.PAGE_TEMPLATE_PATH}/be4fe-crud-fragment.component.html', 'r') as file:
        template_fragment = file.read()

    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        field_name = field.name
        fragment = template_fragment.replace('__KEY_IDX__', f'{field_idx}')
        # TODO: this is a hack
        # the solution is to determine all of the
        # reference tuples and insert them dynamically
        if field.data_type == 'reference':
            field_name = field_name.removesuffix('_id')
            field_name = field_name + '.' + field_name
        fragment = fragment.replace('__ENTITY_FIELD__', field_name)
        table_template_fragments.append(fragment)

    with open(f'{ctx.PAGE_BE4FE_PAGED_TEMPLATE_PATH}/_.component.html', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(
        '__XXXX_TEMPLATE_FRAGMENTS__', ''.join(map(str, table_template_fragments)))
    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}.component.html', filedata)
