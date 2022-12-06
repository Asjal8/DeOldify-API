import sys
import logging
from deoldify._device import _Device

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)

device = _Device()
