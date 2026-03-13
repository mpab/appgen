LF4 = "\n    "
LF8 = "\n        "


def description(ctx):
    return f'generate api file for: {", ".join(ctx.TABLE_DEFINITIONS)}'


def exec(ctx):
    for entity in ctx.TABLE_DEFINITIONS:
        generate_single(ctx, entity)


def generate_single(ctx, entity):

    if entity.endswith("_enum"):
        return

    entity_names = ctx.generate_entity_names_from_snake(entity)
    tdefs = ctx.TABLE_DEFINITIONS[entity]

    js_params = ""
    js_body = ""

    entity_columns = []
    for idx, tdef in enumerate(tdefs):
        if tdef[0] == entity_names.ID:
            continue
        js_params = js_params + "const { " + tdef[0] + " } = req.params;" + LF8
        js_body = js_body + "const { " + tdef[0] + " } = req.body;" + LF8

    js_params = js_params[: -len(LF8)]
    js_body = js_body[: -len(LF8)]

    sql_read_b4fe_promise_results = []
    sql_read_b4fe = []
    sql_read = f"{ctx.TAB12}await db.query(__SQL_READ__)"
    sql_read_b4fe_constraints = []

    for table in ctx.TABLE_DEFINITIONS:
        sql_read_b4fe_promise_results.append(f"{ctx.TAB12}{table}")
        sql = ctx.TABLES_SQL[table]
        if (
            ctx.has_opt(ctx.ENTITY_FIELDS_STEM)
            and table == ctx.ENTITY_FIELDS_TABLE_NAME
        ):  # get column of data
            sql_read_b4fe.append(
                sql_read.replace("__SQL_READ__", sql["sql_read_enum_as_array"])
            )
            continue  # don't add entity as a constraint
        else:  # get collection
            sql_read_b4fe.append(sql_read.replace("__SQL_READ__", sql["sql_read"]))
        if table == ctx.ENTITY_TABLE_NAME:
            continue  # don't add entity as a constraint
        sql_read_b4fe_constraints.append(f"{ctx.TAB16}{table}: {table}.rows")

    # generate api endpoint file
    with open(f"{ctx.COMPONENTS_API_ENDPOINTS_PATH}/be4fe.js", "r") as file:
        filedata = file.read()

    # grep contents
    sql = ctx.TABLES_SQL[entity]
    filedata = filedata.replace("__SQL_GET_INDEX__", sql["sql_get_index"])
    filedata = filedata.replace("__SQL_RESET_INDEX__", sql["sql_reset_index"])
    filedata = filedata.replace("__SQL_CREATE_ITEM__", sql["sql_create_item"])
    filedata = filedata.replace("__SQL_READ__", sql["sql_read"])
    filedata = filedata.replace("__SQL_READ_ITEM__", sql["sql_read_item"])
    filedata = filedata.replace("__SQL_UPDATE_ITEM__", sql["sql_update_item"])
    filedata = filedata.replace("__SQL_DELETE_ITEM__", sql["sql_delete_item"])

    filedata = filedata.replace("__ENTITY_PASCAL__", entity_names.PASCAL)
    filedata = filedata.replace("__JS_BODY__", js_body)
    filedata = filedata.replace("__JS_PARAMS__", js_params)
    filedata = filedata.replace("__ENTITY_ID__", entity_names.ID)
    filedata = filedata.replace("__ENTITY_SNAKE__", entity_names.SNAKE)

    filedata = filedata.replace(
        "__SQL_READ_B4FE_PROMISE_RESULTS___", ",\n".join(sql_read_b4fe_promise_results)
    )
    filedata = filedata.replace("__SQL_READ_B4FE__", ",\n".join(sql_read_b4fe))
    filedata = filedata.replace(
        "__SQL_READ_B4FE_CONSTRAINTS___", ",\n".join(sql_read_b4fe_constraints)
    )

    if ctx.has_opt(ctx.ENTITY_FIELDS_STEM):
        filedata = filedata.replace(
            "__ENTITY_FIELDS_TABLE_VECTOR__",
            f"{ctx.ENTITY_FIELDS_TABLE_NAME}.rows[0].array",
        )
    else:
        filedata = filedata.replace("__ENTITY_FIELDS_TABLE_VECTOR__", "[]")

    # save
    api_file = f"{ctx.APP_API_SRC_ENDPOINTS_PATH}/" + entity_names.KEBAB + ".js"
    ctx.save_data(api_file, filedata)

    # configure endpoint
    endpoint_cmd = f"expose(require('./endpoints/{entity_names.KEBAB}'));"
    endpoints_fp = f"{ctx.APP_API_SRC_PATH}/endpoints.js"
    ctx.append_data_if_not_present(endpoints_fp, endpoint_cmd)
    ctx.user_action([endpoints_fp, endpoint_cmd])
