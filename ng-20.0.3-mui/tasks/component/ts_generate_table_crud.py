TS_NAME='.component.ts'

def description(ctx):
    return f'generate: {ctx.ENTITY_KEBAB}{TS_NAME}'


def exec(ctx):
    table_template_imports = []
    collections_declarations = []
    injected_services = []
    collections_init = []
    services_read = []
    displayed_columns = []
    be4fe_constraints = []
    entity_initializer = []
    keys_pascal_spaced_quoted = []

    with open(f'{ctx.PAGE_TEMPLATE_PATH}/table-crud-fragment-service-read.component.ts', 'r') as file:
        collection_init = file.read()

    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        entity_init = ctx.TAB16 + f"{field.name}: {field.js_init},"
        entity_initializer.append(entity_init)
        key_names = ctx.from_snake(field.name)

        if field.data_type != 'entity_id':
            displayed_columns.append(f'"{field_idx}", ')
            keys_pascal_spaced_quoted.append(f'"{key_names.PASCAL_SPACED}"')

        if field.data_type == 'reference':
            collection_name = f'{key_names.CAMEL}Collection'
            collection = f'{collection_name}: {key_names.PASCAL}Model[] = [];'
            collections_declarations.append(ctx.TAB04 + collection)

            table_template_imports.append(
                'import { ' + key_names.PASCAL + 'Model } from ' + f"'../{key_names.KEBAB}/{key_names.KEBAB}.model';")
            table_template_imports.append(
                'import { ' + key_names.PASCAL + 'Service } from ' + f"'../{key_names.KEBAB}/{key_names.KEBAB}.service';")

            service_inject = f'public {key_names.CAMEL}Service: {key_names.PASCAL}Service,'
            injected_services.append(ctx.TAB08 + service_inject)

            collections_init.append(
                collection_init.replace('__KEY_CAMEL__', key_names.CAMEL))

            be4fe_constraint = ctx.TAB16 + \
                f'{key}: this.{key_names.CAMEL}Collection,'
            be4fe_constraints.append(be4fe_constraint)

    with open(f'{ctx.PAGE_TEMPLATE_PATH}/table-crud.component.ts', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('__ENTITY_PASCAL__', ctx.ENTITY_PASCAL)
    filedata = filedata.replace('__ENTITY_CAMEL__', ctx.ENTITY_CAMEL)
    filedata = filedata.replace('__ENTITY_KEBAB__', ctx.ENTITY_KEBAB)
    filedata = filedata.replace('__ENTITY_SNAKE__', ctx.ENTITY_SNAKE)
    filedata = filedata.replace('__ENTITY_ID__', ctx.ENTITY_ID)

    filedata = filedata.replace(
        '__KEYS_PASCAL_SPACED__QUOTED__', ', '.join(map(str, keys_pascal_spaced_quoted)))
    filedata = filedata.replace(
        '__TABLE_TEMPLATE_IMPORTS__', '\n'.join(map(str, table_template_imports)))
    filedata = filedata.replace(
        '__DISPLAYED_COLUMNS__', ''.join(map(str, displayed_columns)))
    filedata = filedata.replace('__COLLECTIONS_DECLARATIONS__', '\n'.join(
        map(str, collections_declarations)))
    filedata = filedata.replace(
        '__INJECTED_SERVICES__', '\n'.join(map(str, injected_services)))
    filedata = filedata.replace(
        '__COLLECTIONS_INIT__', '\n'.join(map(str, collections_init)))
    filedata = filedata.replace(
        '__BE4FE_CONSTRAINTS__', '\n'.join(map(str, be4fe_constraints)))
    filedata = filedata.replace(
        '__ENTITY_INITIALIZER__', '\n'.join(map(str, entity_initializer)))

    ctx.save_data(
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}', filedata)
