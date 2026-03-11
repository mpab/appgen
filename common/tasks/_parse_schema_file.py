import io
import os.path
import json
import jsonschema


def parse(ctx, schema_fp, depth):

    with open(schema_fp, "r") as file:
        filedata = file.read()
    schema = json.loads(filedata)

    entity_name = schema["title"]
    if not entity_name == entity_name.lower():
        ctx.fatal(f"title/entity name must be lower case: {entity_name}")
    ctx.info(f"analyzing schema: {schema_fp}")

    properties = schema["properties"]
    expected_id = f"{entity_name}_id"
    entity_id = properties[expected_id]

    table_definition = []
    schema_definition = []

    for field in properties:
        field_def = properties[field]

        if "$ref" in field_def:
            ref = field_def["$ref"]
            ref_fp = f"{ctx.JSON_SCHEMA_PATH}/{os.path.dirname(ref)}"
            ctx.info(f"found reference schema: {ref_fp}")
            (_, ref_schema) = parse(ctx, ref_fp, depth + 1)

            ref_entity = ref_schema["properties"][field]
            ref_entity_type = ref_entity["type"]
            if not (ref_entity_type == "integer" or ref_entity_type == "string"):
                ctx.fatal(
                    f"in schema file - {ref}, unhandled reference type - {ref_entity_type}"
                )

            field_constraint = field_def["constraint"]
            table_definition.append([field, field_constraint])

            schema_definition.append(
                [field, ref_entity_type, "is_ref", field_def["ref_entity"]]
            )

        elif "constraint" in field_def:
            field_constraint = field_def["constraint"]
            table_definition.append([field, field_constraint])

            field_type = field_def["type"]
            schema_definition.append([field, field_type, "is_not_ref"])
        else:
            ctx.fatal(
                f"in schema file - {schema_fp}, missing property 'constraint' - {field}: {field_def}"
            )

    ctx.TABLE_DEFINITIONS[entity_name] = table_definition
    ctx.SCHEMA_DEFINITIONS[entity_name] = schema_definition
    return (entity_name, schema)
