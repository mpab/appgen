def description(ctx):
    return f'fail if entity ends with _enum'


def exec(ctx):
    if (ctx.ENTITY_SNAKE.endswith('_enum')):
        ctx.fatal(f'{ctx.ENTITY_SNAKE} is not an enum')
