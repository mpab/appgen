import json


MENU_STEM = "--menu="
MENU_CHILD_STEM = "--menu.child="


def description(ctx):
    return f"remove entry from menu"


def exec(ctx):

    no_menu = True
    if ctx.has_opt(MENU_STEM):
        no_menu = False
    else:
        ctx.info(f"no menu")

    if ctx.has_opt(MENU_CHILD_STEM):
        no_menu = False
    else:
        ctx.info(f"no child menu")

    ctx.NO_MENU = no_menu
    if no_menu:
        return

    menu = {}
    children = []

    item_to_remove = None

    for opt in ctx.get_opts():
        if opt.startswith(MENU_STEM):
            menu_item = opt.removeprefix(MENU_STEM)
            item_to_remove = menu_item
        if opt.startswith(MENU_CHILD_STEM):
            item_to_remove = opt.removeprefix(MENU_CHILD_STEM)

    if not item_to_remove:
        ctx.fatal("no menu item specified")

    fpath = f"{ctx.APP_APP_PATH}/app.menu.json"
    with open(fpath, "r") as file:
        filedata = file.read()
    app_menu = json.loads(filedata)

    if not isinstance(app_menu, list):
        ctx.fatal(f"not a list: {fpath}")

    # TODO
