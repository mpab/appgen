HTML_NAME='-form.component.html'


def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{HTML_NAME}'


def create_ref_fragment(ctx, ref_entity_id):
    with open(f'{ctx.PAGE_TEMPLATE_PATH}/be4fe-crud-form-fragment-1ofn.component.html', 'r') as file:
            enum_fragment = file.read()

    ref_entity = ctx.ENTITY_REF_MAP[ref_entity_id]
    enum_fragment = enum_fragment.replace('__REF_ENTITY__', ref_entity)
    enum_fragment = enum_fragment.replace('__REF_ENTITY_ID__', ref_entity_id)
    # TODO: enumerate reference tuples and add a fragment for each field
    enum_fragment = enum_fragment.replace('__REF_ENTITY_FIELD__', ref_entity)
    return enum_fragment


def exec(ctx):
    form_template_fragments = []

    with open(f'{ctx.PAGE_TEMPLATE_PATH}/xxxx-crud-form-fragment-1ofn.component.html', 'r') as file:
        enum_fragment = file.read()
    with open(f'{ctx.PAGE_TEMPLATE_PATH}/xxxx-crud-form-fragment-text.component.html', 'r') as file:
        text_fragment = file.read()

    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        if field.data_type == 'entity_id':  continue # skip ID

        field_name = field.name
        if field_name in ctx.ENTITY_REF_MAP.keys():
            # TODO: enumerate reference tuples and add a fragment for each field
            fragment = create_ref_fragment(ctx, field_name)
        elif field.data_type == 'text': fragment = text_fragment
        elif field.data_type == 'reference': fragment = enum_fragment
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
        '__FORM_TEMPLATE_FRAGMENTS__', '\n'.join(map(str, form_template_fragments)))
    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{HTML_NAME}', filedata)
