TS_NAME = "-api.model.ts"


def description(ctx):
    return f"generate: {ctx.ENTITY_KEBAB}{TS_NAME}"


def exec(ctx):
    entity_references_imports = []
    entity_references_declarations = []

    for reference_entity in ctx.REFERENCES:
        names = ctx.generate_entity_names_from_snake(reference_entity)
        entity_references_imports.append(
            "import { "
            + names.PASCAL
            + "Model }"
            + f" from '../{names.KEBAB}/{names.KEBAB}.model';"
        )

    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        field_name = field.name
        if field_name in ctx.ENTITY_REF_MAP.keys():
            reference_entity = ctx.ENTITY_REF_MAP[field_name]
            names = ctx.generate_entity_names_from_snake(reference_entity)
            entity_references_declarations.append(
                f"{ctx.TAB08}{reference_entity}: {names.PASCAL}Model[],"
            )

    with open(f"{ctx.PAGE_TEMPLATE_PATH}/be4fe{TS_NAME}", "r") as file:
        filedata = file.read()
    filedata = filedata.replace("__ENTITY_PASCAL__", ctx.ENTITY_PASCAL)
    filedata = filedata.replace("__ENTITY_KEBAB__", ctx.ENTITY_KEBAB)

    filedata = filedata.replace(
        "__ENTITY_REFERENCES_IMPORTS__", "\n".join(map(str, entity_references_imports))
    )
    filedata = filedata.replace(
        "__ENTITY_REFERENCES_DECLARATIONS__",
        "\n".join(map(str, entity_references_declarations)),
    )

    ctx.save_data(f"{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{TS_NAME}", filedata)
