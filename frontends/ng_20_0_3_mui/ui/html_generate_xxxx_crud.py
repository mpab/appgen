HTML_NAME = ".component.html"


def description(ctx):
    return f"generate: {ctx.ENTITY_KEBAB}{HTML_NAME}"


def exec(ctx):
    table_template_fragments = []

    with open(
        f"{ctx.PAGE_TEMPLATE_PATH}/xxxx-crud-fragment.component.html", "r"
    ) as file:
        template_fragment = file.read()

    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    for field_idx, field in enumerate(entity_fields):
        fragment = template_fragment.replace("__KEY_IDX__", f"{field_idx}")
        fragment = fragment.replace("__KEY__", field.name)
        table_template_fragments.append(fragment)

    with open(f"{ctx.PAGE_TEMPLATE_PATH}/xxxx-crud.component.html", "r") as file:
        filedata = file.read()
    filedata = filedata.replace(
        "__XXXX_TEMPLATE_FRAGMENTS__", "".join(map(str, table_template_fragments))
    )
    ctx.save_data(
        f"{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}{HTML_NAME}", filedata
    )
