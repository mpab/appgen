import io
import os.path
import json
import jsonschema


def parse(ctx, filename, depth):

    with open(filename, "r") as file:
        filedata = file.read()
    schema = json.loads(filedata)

    entity_name = schema["title"]
    if not entity_name == entity_name.lower():
        ctx.fatal(f"title/entity name must be lower case: {entity_name}")
    ctx.info(f"analyzing schema: {entity_name}")

    properties = schema["properties"]
    expected_id = f"{entity_name}_id"
    entity_id = properties[expected_id]

    table_definition = []

    for field in properties:
        field_def = properties[field]

        if "$ref" in field_def:
            ref = field_def["$ref"]
            ref_fp = os.path.dirname(ctx.ENTITY_ARG) + "/" + os.path.dirname(ref)
            (_, ref_schema) = parse(ctx, ref_fp, depth + 1)

            ref_entity = ref_schema["properties"][field]
            ref_entity_type = ref_entity["type"]
            if not (ref_entity_type == "integer" or ref_entity_type == "string"):
                ctx.fatal(
                    f"in schema file - {ref}, unhandled reference type - {ref_entity_type}"
                )

            field_constraint = field_def["constraint"]
            table_definition.append([field, field_constraint])

        elif "constraint" in field_def:
            field_constraint = field_def["constraint"]
            table_definition.append([field, field_constraint])
        else:
            ctx.fatal(
                f"in schema file - {filename}, missing property 'constraint' - {field}: {field_def}"
            )

    ctx.TABLE_DEFINITIONS[entity_name] = table_definition
    return (entity_name, schema)
