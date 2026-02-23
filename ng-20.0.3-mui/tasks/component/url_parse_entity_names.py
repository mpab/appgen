import re
import requests
import os
import sys
from pathlib import Path


def description(ctx):
    return f"parse entity names from url {ctx.ENTITY_ARG}"


def exec(ctx):
    try:
        response = requests.get(ctx.ENTITY_ARG)
    except Exception as e:
        ctx.error(f'{e}')
        ctx.fatal(f'reading url failed for: {ctx.ENTITY_ARG}')

    ctx.ENTITY_URL = ctx.ENTITY_ARG
    try:
        ctx.RESPONSE_JSON = response.json()
        ctx.ENTITY_PASCAL = ctx.ENTITY_URL.split("/")[-1]
    except Exception as e:
        ctx.error(f'{e}')
        ctx.fatal(f'parsing json failed for: {ctx.ENTITY_ARG}')

    if 'localhost' not in ctx.ENTITY_URL:
        ctx.warn(f'cannot parse/substitute "localhost" in {ctx.ENTITY_URL}')
        ctx.SERVICE_URL = ctx.ENTITY_URL
    else:
        ctx.API_URL = ctx.ENTITY_URL.replace('localhost', "' + window.location.hostname + '")
        ctx.info(ctx.API_URL)

    ctx.ENTITY_PASCAL_SPACED = ' '.join(
        re.findall(r'[A-Z][^A-Z]*', ctx.ENTITY_PASCAL))
    ctx.ENTITY_LOWER_SPACED = ctx.ENTITY_PASCAL_SPACED.lower()
    ctx.ENTITY_SNAKE = ctx.ENTITY_LOWER_SPACED.replace(" ", "_").lower()
    names = ctx.from_snake(ctx.ENTITY_SNAKE)
    ctx.ENTITY_SNAKE_UCASE = names.SNAKE_UCASE
    ctx.ENTITY_KEBAB = names.KEBAB
    ctx.ENTITY_CAMEL = names.CAMEL
    ctx.ENTITY_PASCAL_SPACED_NO_ENUM = names.PASCAL_SPACED_NO_ENUM

    ctx.GENERATED_ENTITY_PATH = f'{ctx.APP_PAGES_PATH}/{ctx.ENTITY_KEBAB}'
    ctx.ensure_folder(ctx.GENERATED_ENTITY_PATH)

