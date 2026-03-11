import re
import requests
import os
import sys
from pathlib import Path

ctx_stack_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(ctx_stack_dir))
import frontend_context


class FrontendComponentContext:
    def description(ctx):
        return "create frontend component context"

    def exec(ctx):
        if not (ctx.read_opts()):
            ctx.fatal("arguments required")
        if not hasattr(ctx, "ENTITY_ARG"):
            ctx.fatal("argument required")


def create(job):
    ctx = frontend_context.create(job)
    ctx.exec(FrontendComponentContext)
    return ctx
