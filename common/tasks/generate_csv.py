import os.path


def description(ctx):
    return (
        f'generate csv schema and seed file(s) for: {", ".join(ctx.TABLE_DATAFRAMES)}'
    )


def exec(ctx):
    csv_fp1 = f"{ctx.CSV_SCHEMA_PATH}/{ctx.ENTITY_TABLE_NAME}.csv"
    save(ctx, csv_fp1)

    csv_fp2 = f"{ctx.DATABASE_CSV_SEED_PATH}/{ctx.ENTITY_TABLE_NAME}.csv"
    save(ctx, csv_fp2)

    ctx.completed(f"save: {csv_fp1}, {csv_fp2}")


def save(ctx, csv_fp):
    if os.path.isfile(csv_fp):
        if not ctx.get_opt("--clobber-csv"):
            ctx.info(f"not overwriting {csv_fp} (--clobber-csv not set)")
            return
        ctx.warn(f"overwriting: {csv_fp} (--clobber-csv)")
    else:
        ctx.warn(f"generating: {csv_fp} (no existing file)")

    ctx.TABLE_DATAFRAMES[ctx.ENTITY_TABLE_NAME].to_csv(
        csv_fp, index=False, lineterminator="\n"
    )
