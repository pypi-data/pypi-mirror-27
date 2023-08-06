from enum import Enum
from splunkapi3.model.model import Model


class Direction(Enum):
    asc = 1,
    desc = 2


class SortMode(Enum):
    auto = 1,
    alpha = 2,
    alpha_case = 3,
    num = 4


class Options(Model):

    def __init__(self,
                 count: int = None,
                 offset: int = None,
                 sort_dir: Direction = None,
                 sort_key: str = None,
                 sort_mode: SortMode = None,
                 search: str = None,
                 summarize: bool = None):
        self.count = count
        self.offset = offset
        self.sort_dir = sort_dir.name if sort_dir else None
        self.sort_key = sort_key
        self.sort_mode = sort_mode.name if sort_mode else None
        self.search = search
        self.summarize = summarize
