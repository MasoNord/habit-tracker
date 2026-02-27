from pathlib import Path


def get_root_path():
    return Path(__name__).parent.parent.parent.parent.parent