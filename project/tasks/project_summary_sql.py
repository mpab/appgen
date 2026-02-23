def description(ctx):
    return f'sql summary: {ctx.ENTITY_ARG}'


def exec(ctx):
    for entity in ctx.TABLES_SQL:
        ctx.banner ([f'SQL: {entity}'])
        sql_cmd = ctx.TABLES_SQL[entity]
        print(*sql_cmd,sep=',\n')
        print()