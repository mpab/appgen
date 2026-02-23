import io
import os.path
import json

class FieldInfo:
    def __init__(self, name, data_type, js_type, js_init, reference):
        self.name = name
        self.data_type = data_type
        self.js_type = js_type
        self.js_init = js_init
        self.reference = reference
    def __str__(self):
        return f'{self.name}, {self.data_type}, {self.js_type}, {self.js_init}, {self.reference}'


def parse_url_entity(entity_snake, entity_snake_id, item_keys_list):
    entity_fields = []
    for key in item_keys_list:
        if key == entity_snake_id:
            entity_fields.append(FieldInfo(key, 'entity_id', "number", -1, key))
        elif key.endswith('_enum_id'):
            ref = key.removesuffix('_id')
            entity_fields.append(FieldInfo(key, 'reference', "number", -1, ref))
        elif key.endswith('_enum'):
            if entity_snake == key: # self name field
                entity_fields.append(FieldInfo(key, 'text', "string", "''", key))
            else:
                entity_fields.append(FieldInfo(key, 'reference', "string", "''", key))
        elif key.endswith('_id'):
            entity_fields.append(FieldInfo(key, 'integer', "number", -1, key))
        else:
            entity_fields.append(FieldInfo(key, 'text', "string", "''", key))

    return entity_fields


def parse_schema_file(ctx):
    _parse_schema_file(ctx, ctx.ENTITY_ARG, 0)


def _parse_schema_file(ctx, filename, depth):

    with open(filename, 'r') as file:
        filedata = file.read()
    schema = json.loads(filedata) 

    entity_name = schema['title']
    if not entity_name == entity_name.lower():
        ctx.fatal(f'title/entity name must be lower case: {entity_name}')
    ctx.info(f'analyzing schema: {entity_name}')

    names = ctx.from_snake(entity_name)

    if depth == 0:
        ctx.ENTITY_SNAKE = entity_name
        ctx.ENTITY_SNAKE_UCASE = names.SNAKE_UCASE
        ctx.ENTITY_LOWER_SPACED = names.LOWER_SPACED
        ctx.ENTITY_PASCAL = names.PASCAL
        ctx.ENTITY_PASCAL_SPACED = names.PASCAL_SPACED
        ctx.ENTITY_PASCAL_SPACED_NO_ENUM = names.PASCAL_SPACED_NO_ENUM # hack
        ctx.ENTITY_KEBAB = names.KEBAB
        ctx.ENTITY_CAMEL = names.CAMEL
        ctx.ENTITY_ID = names.ID
        # TODO: add --url= option
        ctx.API_URL = f"http://' + window.location.hostname + ':3000/api/{ctx.ENTITY_PASCAL}"

        ctx.GENERATED_ENTITY_PATH = f'{ctx.APP_PAGES_PATH}/{ctx.ENTITY_KEBAB}'
        ctx.ensure_folder(ctx.GENERATED_ENTITY_PATH)
    else: # must be a reference
        ctx.REFERENCES.append(entity_name)
    

    properties = schema['properties']

    _= properties[names.ID] # barf if not present

    entity_fields = []
    
    for field in properties:
        field_def = properties[field]

        if '$ref' in field_def: # special ref handling as $ref does not have a type
            ref = field_def['$ref']
            ref_fp = os.path.dirname(ctx.ENTITY_ARG) + '/' + os.path.dirname(ref)
            ref_schema = _parse_schema_file(ctx, ref_fp, depth + 1)

            ref_entity = ref_schema['properties'][field]
            ref_entity_type = ref_entity['type']
            if not (ref_entity_type == 'integer' or  ref_entity_type == 'string'):
                ctx.fatal(f'in schema file - {ref}, unhandled reference type - {ref_entity_type}')

            ref = field.removesuffix('_id')

            if ref_entity_type == 'integer':
                entity_fields.append(FieldInfo(field, 'reference', "number", -1, ref))
            elif ref_entity_type == 'string':
                entity_fields.append(FieldInfo(field, 'reference', "string", "''", ref))
            else:
                ctx.fatal(f'unhandled type: {field}: {ref_entity_type}')
        else:
            entity_type = schema['properties'][field]['type'] # safe to get type

            if field == names.ID:
                entity_fields.append(FieldInfo(field, 'entity_id', "number", -1, field))
            elif entity_type == 'integer':
                entity_fields.append(FieldInfo(field, 'integer', "number", -1, field))
            elif entity_type == 'string':
                entity_fields.append(FieldInfo(field, 'text', "string", "''", field))
            else:
                ctx.fatal(f'unhandled type: {field}: {entity_type}')

    ctx.ENTITY_DEFINITIONS[entity_name] = entity_fields
    return schema
