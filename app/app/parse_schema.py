import os
import app._parse_schema_file as _parse_schema_file


def description(ctx):
    return f"analyse {ctx.ENTITY_SNAKE} (and dependencies) using constraints and checking data validity"


def exec(ctx):
    # minor kludge to avoid overwriting any _fields_enum tables/schemas
    # TODO: attach _fields_enum to schema?
    if not hasattr(ctx, "TABLE_DEFINITIONS"):
        ctx.TABLE_DEFINITIONS = {}
    if not hasattr(ctx, "SCHEMA_DEFINITIONS"):
        ctx.SCHEMA_DEFINITIONS = {}

    schema_fp = f"{ctx.JSON_SCHEMA_PATH}/{ctx.ENTITY_SNAKE}.json"
    (entity_name, _) = _parse_schema_file.parse(ctx, schema_fp, 0)
    ctx.ENTITY_TABLE_NAME = entity_name

    # for key in ctx.TABLE_DEFINITIONS:
    #     print(key)
    #     print(ctx.TABLE_DEFINITIONS[key])
    # exit()
