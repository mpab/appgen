from component._parse_entity import parse_url_entity 
API_UUID = "BB9D0245-82F4-4E65-BD6E-D7A2A1694656"

def description(ctx):
    return f'parse: {ctx.ENTITY_URL} as shape {API_UUID} at: [result]'


def exec(ctx):
    is_enum_entity = ctx.ENTITY_SNAKE.endswith('_enum')
    if (is_enum_entity):
        ctx.fatal(f'{ctx.ENTITY_SNAKE} is an enum')

    result = ctx.RESPONSE_JSON['result']
    version = result['version']
    shape = version['shape']
    if not shape == API_UUID:
        ctx.fatal(f'expected shape: {API_UUID}, found: {shape}')
    ctx.API_UUID = API_UUID
    entities = result['entities']

    if isinstance(entities, list):
        ctx.ENTITY = entities[0]
    elif isinstance(result, dict):
        ctx.fatal('unhandled dictionary result type')
    else:
        ctx.fatal(f'unknown result type')

    # expects a response shape with an array of result
    item_keys_list = list(ctx.ENTITY.keys())
    ctx.ENTITY_ID = item_keys_list[0]
    expected_entity_id = ctx.ENTITY_SNAKE + '_id'
    if (ctx.ENTITY_ID != expected_entity_id):
        ctx.fatal(f'{ctx.ENTITY_ID} != {expected_entity_id}')

    ctx.ENTITY_DEFINITIONS = {}
    ctx.ENTITY_DEFINITIONS[ctx.ENTITY_SNAKE] = parse_url_entity(ctx.ENTITY_SNAKE, ctx.ENTITY_ID, item_keys_list)

    ctx.REFERENCES = result['references']
    ctx.ENTITY_REF_MAP = {}

    for reference_entity in ctx.REFERENCES:
        reference_entity_id = ctx.from_snake(reference_entity).ID
        ctx.ENTITY_DEFINITIONS[reference_entity] = parse_url_entity(reference_entity, reference_entity_id, ctx.REFERENCES[reference_entity][0])
        ctx.ENTITY_REF_MAP[reference_entity_id] = reference_entity
        if not reference_entity_id in ctx.ENTITY:
            ctx.fatal(f'expected: {ctx.ENTITY_SNAKE}.{reference_entity_id} from reference {reference_entity}, found: none')

    ctx.completed(description(ctx))