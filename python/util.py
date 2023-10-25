"""
Common utility functions.
"""

import os
import time

try:
    import psutil
except ImportError:
    psutil = None


def get_time():
    """
    Returns the processor time in ms.
    """
    return time.process_time() * 1000


def get_memory():
    """
    Returns the memory used in MB.
    """
    if not psutil:
        return -1
    i = psutil.Process(os.getpid()).memory_info()
    mem = {
        'rss': BtoMB(i.rss),
        'text': BtoMB(i.text),
        'data': BtoMB(i.data),
    }
    return mem['data']


def BtoMB(n):
    return n / 1000 / 1000
