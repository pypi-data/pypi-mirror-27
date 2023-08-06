import warnings
from operator import attrgetter, itemgetter
from typing import List, Optional, Iterable

from .base_workspace import BaseWorkspace


class WorkspaceStorage:
    """Stores workspaces"""
    def __init__(self, iterable: Optional[Iterable[BaseWorkspace]]=None, limit: Optional[int]=None):
        if iterable is None:
            iterable = []
        elif not isinstance(iterable, list):
            iterable = list(iterable)

        if limit is None:
            limit = float('+inf')

        self.workspaces = [
            (ws.id, ws)
            for ws in sorted(iterable, key=attrgetter('id'))
        ]

        self.limit = limit

        if len(self.workspaces) > self.limit:
            warnings.warn('Workspace count is greater than limit')

    def __iter__(self):
        yield from self.keys()

    def keys(self):
        yield from (key for key, _ in self.workspaces)

    def values(self) -> List[BaseWorkspace]:
        yield from (value for _, value in self.workspaces)

    def items(self):
        yield from self.workspaces

    def __getitem__(self, item) -> Optional[BaseWorkspace]:
        """Gets workspace from storage by id"""
        workspaces = dict(self.workspaces)
        return workspaces[item] if item in workspaces else None

    def at(self, index) -> Optional[BaseWorkspace]:
        """Gets workspace from storage by index

        To get the oldest workspace use index 0
        To get the latest workspace use index -1
        """
        if index >= len(self.workspaces):
            return None

        pair = self.workspaces[index]
        return pair[1]

    def add(self, workspace: BaseWorkspace):
        """Add a workspace

        Parameters
        ----------
        workspace: subclass of BaseWorkspace
            Workspace to be added
        """
        if not isinstance(workspace, BaseWorkspace):
            raise ValueError('Value must be of type {}'.format(BaseWorkspace.__name__))

        pair = (workspace.id, workspace)

        workspaces = list(self.workspaces)
        workspaces.append(pair)
        workspaces = sorted(workspaces, key=itemgetter(0))
        self.workspaces = workspaces

    def __repr__(self):
        return '<WorkspaceStorage {}>'.format(list(self.keys()))

    def __len__(self):
        return len(self.workspaces)

