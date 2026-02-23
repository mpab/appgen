CSS_FILE = 'enum-_ru_.component.css'

def description(ctx):
    return f'setup app context'

def exec(ctx):
    ctx.copy_file(f'{ctx.PAGE_TEMPLATE_PATH}/{CSS_FILE}',
        f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}.component.css')