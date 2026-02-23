import os
import tasks.api._parse_schema_file


def description(ctx):
    return f"analyse {ctx.ENTITY_ARG} (and dependencies) using constraints and checking data validity"


def exec(ctx):
    ctx.TABLE_DEFINITIONS = {}
    (entity_name, _) = tasks.api._parse_schema_file.parse(ctx, ctx.ENTITY_ARG, 0)
    ctx.ENTITY_TABLE_NAME = entity_name
    # for key in ctx.TABLE_DEFINITIONS:
    #     print (key)
    #     print (ctx.TABLE_DEFINITIONS[key])
    # exit()
