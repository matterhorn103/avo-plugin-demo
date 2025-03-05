# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "platformdirs>=4.2.0",
# ]
# 
# [tool.avogadro.script]
# type = "energy"
# display-name = "Yell Hello"
# menu-path = [ "Extensions", 900 ]
# 
# [tool.pixi]
# channels = ["conda-forge"]
#
# [tool.pixi.dependencies]
# numpy = ">=2.2.0"
# ///

import numpy as np

print("HELLO, WORLD!")
