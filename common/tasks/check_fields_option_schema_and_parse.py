import os
import common.tasks._parse_schema_file as _parse_schema_file


def description(ctx):
    return f"check for entity fields option JSON, parse if found"


def exec(ctx):
    entity_fields_opt = ctx.match_opt_prefix_or_default(ctx.ENTITY_FIELDS_STEM)
    if entity_fields_opt == "":
        ctx.info(f"{ctx.ENTITY_FIELDS_STEM}None")
        return

    entity_fields_opt_fp = f"{ctx.JSON_SCHEMA_PATH}/{entity_fields_opt}"
    if not os.path.isfile(entity_fields_opt_fp):
        ctx.fatal(
            f"expected file: {entity_fields_opt_fp}, but found: none ({entity_fields_opt})"
        )

    ctx.ENTITY_FIELDS_SCHEMA_FP = entity_fields_opt_fp
    ctx.info(f"{ctx.ENTITY_FIELDS_STEM}{ctx.ENTITY_FIELDS_SCHEMA_FP}")

    (entity_name, _) = _parse_schema_file.parse(ctx, ctx.ENTITY_FIELDS_SCHEMA_FP, 0)
    ctx.ENTITY_FIELDS_TABLE_NAME = entity_name
