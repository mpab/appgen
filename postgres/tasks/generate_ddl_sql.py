LF4 = "\n    "
LF8 = "\n        "


def description(ctx):
    return f'generate sql file(s) for: {", ".join(ctx.TABLE_DEFINITIONS)}'


def exec(ctx):
    for table_name in ctx.TABLE_DEFINITIONS:
        generate_single(ctx, table_name)


def generate_single(ctx, entity):

    entity_names = ctx.generate_entity_names_from_snake(entity)
    tdefs = ctx.TABLE_DEFINITIONS[entity]

    sql_drop_table = "drop table if exists " + entity + " cascade;"
    sql_create_table = "create table if not exists " + entity + " ("

    items_k = []
    items_v = []

    entity_columns = []
    for idx, tdef in enumerate(tdefs):
        if idx == 0:
            continue  # skip id
        entity_columns.append(tdef[0])
        items_k.append(tdef[0])
        items_v.append("'${" + tdef[0] + "}'")

    for tdef in tdefs:
        sql_create_table = sql_create_table + LF4 + tdef[0] + " " + tdef[1] + ","

    sql_create_table = sql_create_table[:-1] + "\n);"

    sql_items_v_csv = ",".join(items_v)
    sql_items_k_quoted = list(map(lambda k: '"' + k + '"', items_k))
    sql_items_k_quoted_csv = ",".join(sql_items_k_quoted)
    kv_assign = list(map(lambda k, v: k + "=" + v, sql_items_k_quoted, items_v))
    kv_assign_csv = ",".join(kv_assign)

    sql_create_item = (
        "`insert into "
        + entity
        + " ("
        + sql_items_k_quoted_csv
        + ") values ("
        + sql_items_v_csv
        + ") returning *;`"
    )
    sql_update_item = (
        "`update "
        + entity
        + " set "
        + kv_assign_csv
        + ' where "'
        + entity_names.ID
        + '" = ${'
        + entity_names.ID
        + "} returning *;`"
    )

    # DDL

    sql_file = f"{ctx.DATABASE_SQL_PATH}/drop-table-" + entity_names.KEBAB + ".sql"
    ctx.save_data(sql_file, sql_drop_table)

    sql_file = f"{ctx.DATABASE_SQL_PATH}/create-table-" + entity_names.KEBAB + ".sql"
    ctx.save_data(sql_file, sql_create_table)

    drop_table_cmd = f"exec_psql './sql/drop-table-{entity_names.KEBAB}.sql'"
    create_table_cmd = f"exec_psql './sql/create-table-{entity_names.KEBAB}.sql'"
    recreate_tables_fp = f"{ctx.DATABASE_SCRIPTS_PATH}/recreate-tables"

    ctx.append_data_if_not_present(recreate_tables_fp, drop_table_cmd)
    ctx.user_action([recreate_tables_fp, drop_table_cmd])

    ctx.append_data_if_not_present(recreate_tables_fp, create_table_cmd)
    ctx.user_action([recreate_tables_fp, create_table_cmd])

    # seed table
    seed_file_fp = f"{ctx.DATABASE_SCRIPTS_PATH}/seed-table-" + entity_names.KEBAB
    with open(f"{ctx.COMPONENTS_DB}/seed-table", "r") as file:
        filedata = file.read()
    # grep contents
    filedata = filedata.replace("__ENTITY_SNAKE__", entity_names.SNAKE)
    entity_columns = ",".join(entity_columns)
    filedata = filedata.replace("__ENTITY_COLUMNS__", entity_columns)
    ctx.save_data(seed_file_fp, filedata)
    ctx.setx(seed_file_fp)

    seed_table_cmd = f'"./seed-table-{entity_names.KEBAB}"'
    seed_all_tables_fp = f"{ctx.DATABASE_SCRIPTS_PATH}/seed-tables"

    ctx.append_data_if_not_present(seed_all_tables_fp, seed_table_cmd)
    ctx.setx(seed_all_tables_fp)
    ctx.user_action([seed_all_tables_fp, seed_table_cmd])
