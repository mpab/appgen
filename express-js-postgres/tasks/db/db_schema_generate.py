import os.path


def description(ctx):
    return f'generate json schema file(s) for: {", ".join(ctx.TABLE_DEFINITIONS)}'


def exec(ctx):
    schema_fp = f"{ctx.JSON_SCHEMA_PATH}/{ctx.ENTITY_SNAKE}.json"
    if os.path.isfile(schema_fp):
        if not ctx.get_opt("--clobber-schema"):
            ctx.info(f"not overwriting {schema_fp} (--clobber-schema not set)")
            return
        ctx.warn(f"overwriting: {schema_fp} (--clobber-schema)")
    else:
        ctx.warn(f"generating: {schema_fp} (no existing file)")

    schema_properties = []
    schema_fields = []

    for e in ctx.TABLE_DEFINITIONS[ctx.ENTITY_SNAKE]:
        prop = ""
        for tdef in ctx.TABLE_DEFINITIONS:
            if tdef == ctx.ENTITY_SNAKE:
                continue
            a_def = ctx.TABLE_DEFINITIONS[tdef]
            for r in a_def:
                if r[0] == e[0]:
                    prop = (
                        ctx.TAB04
                        + f'"{e[0]}": '
                        + "{"
                        + f' "$ref": "{tdef}.json/{r[0]} "'
                        + ', "constraint": '
                        + f'"{e[1]}"'
                        + " }"
                    )
        if prop == "":
            prop = (
                ctx.TAB04
                + f'"{e[0]}": '
                + '{ "type": '
                + f'"{e[2]}", "constraint": '
                + f'"{e[1]}"'
                + " }"
            )
        schema_properties.append(prop)
        schema_fields.append(f'"{e[0]}"')

    with open(f"{ctx.TEMPLATE_DATABASE_PATH}/schema.json", "r") as file:
        filedata = file.read()
    # grep contents
    filedata = filedata.replace("__ENTITY_SNAKE__", ctx.ENTITY_SNAKE)
    schema_properties = ",\n".join(schema_properties)
    filedata = filedata.replace("__SCHEMA_PROPERTIES__", schema_properties)
    schema_fields = ", ".join(schema_fields)
    filedata = filedata.replace("__SCHEMA_FIELDS__", schema_fields)
    ctx.save_data(schema_fp, filedata)
