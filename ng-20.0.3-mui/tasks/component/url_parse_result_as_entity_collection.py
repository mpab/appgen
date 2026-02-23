from component._parse_entity import parse_url_entity 


def description(ctx):
    return f'parse: {ctx.ENTITY_URL} as entity collection at: [result]'


def exec(ctx):
    result = ctx.RESPONSE_JSON['result']
    if isinstance(result, list):
        item = result[0]
    elif isinstance(result, dict):
        ctx.fatal('unhandled dictionary result type')
    else:
        ctx.fatal(f'unknown result type')

    # expects a response shape with an array of result
    item_keys_list = list(item.keys())
    print (item_keys_list)
    ctx.ENTITY_ID = item_keys_list[0]
    expected_entity_id = ctx.ENTITY_SNAKE + '_id'
    if (ctx.ENTITY_ID != expected_entity_id):
        ctx.fatal(f'{ctx.ENTITY_ID} != {expected_entity_id}')

    ctx.ENTITY_DEFINITIONS = {}
    ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE] = parse_url_entity(ctx.ENTITY_SNAKE, ctx.ENTITY_ID, item_keys_list)
    ctx.completed(description(ctx))