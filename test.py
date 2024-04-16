from model.parameters import *
from model.global_vars import *
from model.person import *
from model.setup import *
from model.go import *
from model.conclusion import *
from model.MODEL import *

import numpy as np


seed = np.random.randint(1000000)
print(seed)
# seed = 1101
# 1101 il contagio si ferma

mod = model(seed)
#mod.par.a1_reductionPerc = 0.99
mod.run(seed)

mod.par.enableRL = False
