#!/usr/bin/env python
# coding: utf-8

"""
    create at 2017/11/7 by allen
"""

from app.lib.pine_wrapper import PineFlask, PineBlueprint
from app import init_app

# use PineFlask, PineBlueprint to support rest_route
app = PineFlask(__name__, instance_relative_config=True)
api = PineBlueprint('api', __name__)
app = init_app(app=app, bp_list=[api])
