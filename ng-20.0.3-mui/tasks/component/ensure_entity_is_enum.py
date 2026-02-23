def description(ctx):
    return f'ensure entity ends with _enum'


def exec(ctx):
    if (not ctx.ENTITY_SNAKE.endswith('_enum')):
        ctx.fatal(f'{ctx.ENTITY_SNAKE} is not an enum')
