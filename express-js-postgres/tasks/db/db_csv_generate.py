import os.path


def description(ctx):
    return f'generate csv file(s) for: {", ".join(ctx.TABLE_DATAFRAMES)}'


def exec(ctx):
    csv_fp = f"{ctx.DATABASE_CSV_SEED_PATH}/{ctx.ENTITY_TABLE_NAME}.csv"
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
    ctx.completed(f"save: {csv_fp}")
