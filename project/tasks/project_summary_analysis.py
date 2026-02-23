def description(ctx):
    return f'csv analysis summary: {ctx.ENTITY_ARG}'


def exec(ctx):
    ctx.banner(["TABLE_DATAFRAMES"])
    for entity in ctx.TABLE_DATAFRAMES:
        print(f'table dataframe: {entity}')
        print(ctx.TABLE_DATAFRAMES[entity])

    ctx.banner(["TABLE_DEFINITIONS"])
    for entity in ctx.TABLE_DEFINITIONS:
        print (f'table: {entity}')
        tdef = ctx.TABLE_DEFINITIONS[entity]
        print(*tdef,sep=',\n')
        print()