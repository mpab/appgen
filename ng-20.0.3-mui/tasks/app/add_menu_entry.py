import json


MENU_STEM='--menu='
MENU_CHILD_STEM='--menu.child='


def description(ctx):
    return f'add entry to menu'


def exec(ctx):

    no_menu = True
    if ctx.has_opt(MENU_STEM):
        no_menu = False
    else:
        ctx.info(f'no menu')

    if ctx.has_opt(MENU_CHILD_STEM):
        no_menu = False
    else:
        ctx.info(f'no child menu')

    ctx.NO_MENU = no_menu
    if no_menu: return

    menu = {}
    children = []

    for opt in ctx.get_opts():
        if opt.startswith(MENU_STEM):
            menu_item = opt.removeprefix(MENU_STEM)
            menu['name'] = menu_item
        if opt.startswith(MENU_CHILD_STEM):
            menu_child = opt.removeprefix(MENU_CHILD_STEM)
            children.append(menu_child)

    if len(children) and len(menu) > 1:
        ctx.fatal('expected: single menu parent, found: multiple')

    if len(children) and not len(menu):
        ctx.fatal('expected: menu parent, found: none')

    menu_children = []
    for menu_child in children:
        menu_children.append({'name': menu_child})

    if len(menu_children):
        menu['children'] = menu_children

    fpath = f'{ctx.APP_COMPONENT_PATH}/app.menu.json'
    with open(fpath, 'r') as file:
        filedata = file.read()
    app_menu = json.loads(filedata)

    if not isinstance(app_menu, list):
        ctx.fatal(f'not a list: {fpath}')

    # replace or append
    append = True
    for idx, existing_item in enumerate(app_menu):
        if existing_item['name'] == menu['name']:
            app_menu[idx] = menu
            append = False
            break
    if append:
        app_menu.append(menu)

    ctx.save_data(fpath, json.dumps(app_menu, indent=2))
