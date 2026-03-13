CSS_FILE = 'xxxx-crud-form.component.css'

def description(ctx):
    return f'copy: {CSS_FILE}=>{ctx.ENTITY_KEBAB}.component.css'

def exec(ctx):
    ctx.copy_file(f'{ctx.PAGE_TEMPLATE_PATH}/{CSS_FILE}',
                f'{ctx.GENERATED_ENTITY_PATH}/{ctx.ENTITY_KEBAB}-form.component.css')