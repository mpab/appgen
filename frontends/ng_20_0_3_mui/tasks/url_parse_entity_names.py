import re
import requests
import os
import sys


def description(ctx):
    return f"parse entity names from url {ctx.ENTITY_ARG}"


def exec(ctx):
    try:
        response = requests.get(ctx.ENTITY_ARG)
    except Exception as e:
        ctx.error(f"{e}")
        ctx.fatal(f"reading url failed for: {ctx.ENTITY_ARG}")

    ctx.ENTITY_URL = ctx.ENTITY_ARG
    try:
        ctx.RESPONSE_JSON = response.json()
    except Exception as e:
        ctx.error(f"{e}")
        ctx.fatal(f"reading json failed for: {ctx.ENTITY_ARG}")

    if "localhost" not in ctx.ENTITY_URL:
        ctx.warn(f'cannot parse/substitute "localhost" in {ctx.ENTITY_URL}')
        ctx.SERVICE_URL = ctx.ENTITY_URL
    else:
        ctx.API_URL = ctx.ENTITY_URL.replace(
            "localhost", "' + window.location.hostname + '"
        )
        ctx.info(ctx.API_URL)

    ctx.set_entity_names_url_pascal()

    ctx.GENERATED_ENTITY_PATH = f"{ctx.APP_PAGES_PATH}/{ctx.ENTITY_KEBAB}"
    ctx.ensure_folder(ctx.GENERATED_ENTITY_PATH)
