TS_NAME='.viewmodel.ts'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{TS_NAME}'

def init_val(ctx, val):
    if val.endswith('_id'):
        return f"{val}: -1,\n"
    return f"{val}: '',\n"

def exec(ctx):

    model_view_mappers = []
    view_model_mappers = []

    for reference_entity in ctx.REFERENCES:
        model_view_mappers.append(
            f"""        x = apiModel.references.{reference_entity}.find((i) =>
            model.{reference_entity}_id === i.{reference_entity}_id);
            if (x) view.{reference_entity} = x;"""
        )

        view_model_mappers.append(
            f"""        x = apiModel.references.{reference_entity}.find((i) =>
            view.{reference_entity} === i);
            if (x) model.{reference_entity}_id = x.{reference_entity}_id;"""
        )

    create_view = ''
    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        field_name = field.name
        if field_name in ctx.ENTITY_REF_MAP.keys():
            reference_entity_name = ctx.ENTITY_REF_MAP[field_name]
            create_view = create_view + f'{ctx.TAB12}{reference_entity_name}: ' + '{\n'
            reference_entity = ctx.ENTITY_DEFINITIONS[reference_entity_name]
            for ref_entity_key in reference_entity:
                create_view = create_view + ctx.TAB16 + init_val(ctx, ref_entity_key.name)
            create_view = create_view + ctx.TAB12 + '},\n'
            continue
        create_view = create_view + ctx.TAB12 + init_val(ctx, field_name)
    create_view = create_view.removesuffix('\n'); 

    with open(f'{ctx.PAGE_TEMPLATE_PATH}/be4fe{TS_NAME}', 'r') as file:
            filedata = file.read()
    filedata = filedata.replace('__ENTITY_PASCAL__', ctx.ENTITY_PASCAL)
    filedata = filedata.replace('__ENTITY_CAMEL__', ctx.ENTITY_CAMEL)
    filedata = filedata.replace('__ENTITY_KEBAB__', ctx.ENTITY_KEBAB)
    filedata = filedata.replace('__ENTITY_SNAKE__', ctx.ENTITY_SNAKE)
    filedata = filedata.replace('__CREATE_VIEW__', create_view)

    filedata = filedata.replace(
        '__MODEL_VIEW_MAPPERS__', '\n'.join(map(str, model_view_mappers)))
    filedata = filedata.replace(
        '__VIEW_MODEL_MAPPERS__', '\n'.join(map(str, view_model_mappers)))

    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}', filedata)
