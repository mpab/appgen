def description(ctx):
    return f'entity naming summary: {ctx.ENTITY_URL}'


def exec(ctx):
    ctx.banner(["Entity Names"])
    print(ctx.ENTITY_PASCAL)
    print(ctx.ENTITY_CAMEL)
    print(ctx.ENTITY_PASCAL_SPACED)
    print(ctx.ENTITY_SNAKE)
    print(ctx.ENTITY_KEBAB)
    print(ctx.ENTITY_LOWER_SPACED)