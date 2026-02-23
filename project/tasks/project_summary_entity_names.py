def description(ctx):
    return f"entity naming summary: {ctx.ENTITY_ARG}"


def exec(ctx):
    ctx.banner(["Entity Names"])
    print(f"ENTITY_PASCAL:          {ctx.ENTITY_PASCAL}")
    print(f"ENTITY_CAMEL:           {ctx.ENTITY_CAMEL}")
    print(f"ENTITY_PASCAL_SPACED:   {ctx.ENTITY_PASCAL_SPACED}")
    print(f"ENTITY_SNAKE:           {ctx.ENTITY_SNAKE}")
    print(f"ENTITY_KEBAB:           {ctx.ENTITY_KEBAB}")
    print(f"ENTITY_LOWER_SPACED:    {ctx.ENTITY_LOWER_SPACED}")
