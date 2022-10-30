#! /usr/bin/python3

import logging
from pathlib import Path
import sys
logging.basicConfig(stream=sys.stderr)
print("path",Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from GreenH2 import server as application
application.secret_key = 'monkeys'
