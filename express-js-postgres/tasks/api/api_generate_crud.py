LF4 = "\n    "
LF8 = "\n        "


def description(ctx):
    return f'generate api file(s) for: {", ".join(ctx.TABLE_DEFINITIONS)}'


def exec(ctx):
    for table_name in ctx.TABLE_DEFINITIONS:
        generate_single(ctx, table_name)


def generate_single(ctx, entity):

    entity_names = ctx.from_snake(entity)
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

    # generate api endpoint file
    with open(f"{ctx.TEMPLATE_ENDPOINTS_PATH}/crud.js", "r") as file:
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
    filedata = filedata.replace("__ENTITY_SNAKE__", entity)

    # save
    api_file = f"{ctx.API_ENDPOINTS_PATH}/" + entity_names.KEBAB + ".js"
    ctx.save_data(api_file, filedata)

    # configure endpoint
    endpoint_cmd = f"expose(require('./endpoints/{entity_names.KEBAB}'));"
    endpoints_fp = f"{ctx.API_PATH}/endpoints.js"
    ctx.append_data_if_not_present(endpoints_fp, endpoint_cmd)
    ctx.user_action([endpoints_fp, endpoint_cmd])
