HTML_NAME = "enum-_ru_.component.html"


def description(ctx):
    return f"generate: {HTML_NAME}=>{ctx.ENTITY_KEBAB}.component.html"


def exec(ctx):
    entity_fields = ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE]
    enum_key = entity_fields[1].name
    enum_names = ctx.generate_entity_names_from_snake(enum_key)
    with open(f"{ctx.PAGE_TEMPLATE_PATH}/{HTML_NAME}", "r") as file:
        filedata = file.read()
    filedata = filedata.replace("__ENTITY_PASCAL__", ctx.ENTITY_PASCAL)
    filedata = filedata.replace("__ENTITY_CAMEL__", ctx.ENTITY_CAMEL)
    filedata = filedata.replace("__ENTITY_KEBAB__", ctx.ENTITY_KEBAB)
    filedata = filedata.replace("__ENTITY_ID__", ctx.ENTITY_ID)
    filedata = filedata.replace("__KEY__", enum_key)
    filedata = filedata.replace(
        "__KEY_PASCAL_SPACED_NO_ENUM__", enum_names.PASCAL_SPACED_NO_ENUM
    )
    ctx.save_data(
        f"{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}.component.html", filedata
    )
