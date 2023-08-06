#!/usr/bin/env python
from IPython import embed
from brewer.controller import Controller
from brewer.slack import BrewerBot
from brewer.version import VERSION
from brewer.color import *

controller = Controller()
bot = BrewerBot()

green(("Brewer version %s" % VERSION))

embed()
