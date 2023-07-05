import os
import sys
import pandas as pd
from typing import List, Tuple, Dict, Any
from ortoolpy import addvar, addvars, addbinvars
import pandas as pd
from pulp import LpProblem , LpMinimize , LpVariable , lpSum , PULP_CBC_CMD , LpStatus
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from SetData import setdata