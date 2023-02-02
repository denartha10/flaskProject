from ConVert import *
import os.path


def exists(path):
    return os.path.exists(path)


def remove(path):
    os.remove(path)
