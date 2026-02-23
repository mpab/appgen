def description(ctx):
    return f'summary of completed tasks'

def exec(ctx):
    done = 0
    for task in ctx.COMPLETED_TASKS:
        ctx.ok(task)
        done = done + 1
    if not done:
        ctx.ok('none')
