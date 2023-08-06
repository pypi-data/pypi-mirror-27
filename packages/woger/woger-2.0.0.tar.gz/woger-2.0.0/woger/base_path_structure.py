from pathlib import Path
from typing import Union

from .workspace_meta import PathStructureMeta


class BasePathStructure(metaclass=PathStructureMeta):
    def __init__(self, root: Union[bytes, str]):
        """Creates path structure instance

        Parameters
        ----------
        root: path-like
            Path structure root
        """
        self._root = Path(root)
