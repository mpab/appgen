def description(ctx):
    return f'summary of user actions'

def exec(ctx):
    todo = 0
    for action in ctx.USER_ACTIONS:
        with open(action[0], 'r') as file:
            filedata = file.read()
            if (not action[1] in filedata):
                ctx.info(f'{action[0]}: {action[1]}')
                todo = todo + 1
    if not todo:
        ctx.ok('none')
