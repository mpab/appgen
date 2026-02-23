import os


def description(ctx):
    return f"check for entity fields option"


def exec(ctx):
    entity_fields_opt = ctx.match_opt_prefix_or_default(ctx.ENTITY_FIELDS_STEM)
    if entity_fields_opt == "":
        ctx.info(f"{ctx.ENTITY_FIELDS_STEM}None")
        return

    entity_fields_opt_csv_fp = f"{ctx.DATABASE_CSV_SEED_PATH}/{entity_fields_opt}"
    if not os.path.isfile(entity_fields_opt_csv_fp):
        ctx.fatal(
            f"expected file: {entity_fields_opt_csv_fp}, but found: none ({entity_fields_opt})"
        )

    ctx.ENTITY_FIELDS_CSV_FP = entity_fields_opt_csv_fp
    ctx.info(f"{ctx.ENTITY_FIELDS_STEM}{ctx.ENTITY_FIELDS_CSV_FP}")
