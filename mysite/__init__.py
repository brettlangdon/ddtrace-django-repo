import logging
import sys

from ddtrace.writer import log

handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
