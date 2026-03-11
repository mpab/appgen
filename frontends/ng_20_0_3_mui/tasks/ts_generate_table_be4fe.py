TS_NAME = ".component.ts"


def description(ctx):
    return f"generate: {ctx.ENTITY_KEBAB}{TS_NAME}"


def exec(ctx):
    collections_declarations = []
    collections_init = []
    services_read = []
    keys_pascal_spaced_quoted = []
    keys_indexes_quoted = []

    with open(
        f"{ctx.PAGE_TEMPLATE_PATH}/table-crud-fragment-service-read.component.ts", "r"
    ) as file:
        collection_init = file.read()

    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        key_names = ctx.generate_entity_names_from_snake(field.name)
        keys_pascal_spaced_quoted.append(f'"{key_names.PASCAL_SPACED}"')
        keys_indexes_quoted.append(f'"{field_idx}"')

        if field.data_type == "reference":
            collection_name = f"{key_names.PASCAL}Collection"
            collection = f"{collection_name}: {key_names.PASCAL}Model[] = [];"
            collections_declarations.append(ctx.TAB04 + collection)

            service_inject = (
                f"public {key_names.CAMEL}Service: {key_names.PASCAL}Service,"
            )

            collections_init.append(
                collection_init.replace("__KEY_CAMEL__", key_names.CAMEL)
            )

    with open(f"{ctx.PAGE_TEMPLATE_PATH}/table-be4fe.component.ts", "r") as file:
        filedata = file.read()
    filedata = filedata.replace("__ENTITY_PASCAL__", ctx.ENTITY_PASCAL)
    filedata = filedata.replace("__ENTITY_CAMEL__", ctx.ENTITY_CAMEL)
    filedata = filedata.replace("__ENTITY_KEBAB__", ctx.ENTITY_KEBAB)
    filedata = filedata.replace("__ENTITY_SNAKE__", ctx.ENTITY_SNAKE)
    filedata = filedata.replace("__ENTITY_ID__", ctx.ENTITY_ID)

    filedata = filedata.replace(
        "__KEYS_PASCAL_SPACED__QUOTED__", ", ".join(map(str, keys_pascal_spaced_quoted))
    )
    filedata = filedata.replace(
        "__KEYS_INDEXES_QUOTED__", ", ".join(map(str, keys_indexes_quoted))
    )
    filedata = filedata.replace(
        "__COLLECTIONS_DECLARATIONS__", "\n".join(map(str, collections_declarations))
    )
    filedata = filedata.replace(
        "__COLLECTIONS_INIT__", "\n".join(map(str, collections_init))
    )

    ctx.save_data(f"{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}", filedata)
