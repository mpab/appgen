import os.path


def description(ctx):
    return f"generate entity names from: {ctx.ENTITY_ARG}"


def exec(ctx):
    fname = os.path.basename(ctx.ENTITY_ARG)
    name, _ = os.path.splitext(fname)

    ctx.ENTITY_SNAKE = name.replace(" ", "_").lower()
    names = ctx.from_snake(ctx.ENTITY_SNAKE)

    ctx.ENTITY_LOWER_SPACED = names.LOWER_SPACED
    ctx.ENTITY_PASCAL = names.PASCAL
    ctx.ENTITY_PASCAL_SPACED = names.PASCAL_SPACED
    ctx.ENTITY_KEBAB = names.KEBAB
    ctx.ENTITY_CAMEL = names.CAMEL
    ctx.ENTITY_ID = names.ID
    ctx.ENTITY_PASCAL_SPACED_NO_ENUM = names.PASCAL_SPACED_NO_ENUM
