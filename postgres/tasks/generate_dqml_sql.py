LF4 = "\n    "
LF8 = "\n        "


def description(ctx):
    return f'generate api sql for: {", ".join(ctx.TABLE_DEFINITIONS)}'


def exec(ctx):
    for table_name in ctx.TABLE_DEFINITIONS:
        generate_single(ctx, table_name)


def generate_single(ctx, entity):

    entity_names = ctx.generate_entity_names_from_snake(entity)
    tdefs = ctx.TABLE_DEFINITIONS[entity]

    sql_get_index = (
        f'"select pg_get_serial_sequence(' + f"'{entity}', '{entity_names.ID}'" + ')"'
    )  # result assigned to 'index_name'
    sql_reset_index = (
        "`select setval("
        + "'${index_name}'"
        + f",(select max({entity_names.ID}) from {entity}))`"
    )

    sql_read = f'`select * from {entity} order by "' + entity_names.ID + '";`'
    sql_read_enum_as_array = (
        f'`select array(select {entity} from {entity} order by "'
        + entity_names.ID
        + '");`'
    )
    sql_read_item = (
        f'`select * from {entity} where "'
        + entity_names.ID
        + '" = '
        + "${"
        + entity_names.ID
        + "};`"
    )
    sql_delete_item = (
        f'`delete from {entity} where "'
        + entity_names.ID
        + '" = '
        + "${"
        + entity_names.ID
        + "};`"
    )

    items_k = []
    items_v = []

    entity_columns = []
    for idx, tdef in enumerate(tdefs):
        if idx == 0:
            continue  # skip id
        entity_columns.append(tdef[0])
        items_k.append(tdef[0])
        items_v.append("'${" + tdef[0] + "}'")

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

    sql_statements = {}
    sql_statements["sql_get_index"] = sql_get_index
    sql_statements["sql_reset_index"] = sql_reset_index
    sql_statements["sql_create_item"] = sql_create_item
    sql_statements["sql_read"] = sql_read
    sql_statements["sql_read_enum_as_array"] = sql_read_enum_as_array
    sql_statements["sql_read_item"] = sql_read_item
    sql_statements["sql_update_item"] = sql_update_item
    sql_statements["sql_delete_item"] = sql_delete_item
    table_sql = {}
    ctx.TABLES_SQL[entity] = sql_statements
