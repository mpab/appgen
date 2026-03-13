from ui._parse_entity import parse_schema_file


def description(ctx):
    return f"parse: {ctx.ENTITY_ARG} as entity collection, extending with js type info"


def exec(ctx):
    ctx.ENTITY_DEFINITIONS = {}
    ctx.REFERENCES = []
    parse_schema_file(ctx)

    ctx.ENTITY_REF_MAP = {}

    for reference_entity in ctx.REFERENCES:
        elements = ctx.ENTITY_DEFINITIONS[reference_entity]
        ref = ctx.ENTITY_DEFINITIONS[reference_entity]
        element_id = next(iter(elements)).name
        ctx.ENTITY_REF_MAP[element_id] = reference_entity
    ctx.completed(description(ctx))
    # print(ctx.REFERENCES)
    # for key in ctx.ENTITY_REF_MAP:
    #     print (key)
    #     print (ctx.ENTITY_REF_MAP[key])
    # exit()
