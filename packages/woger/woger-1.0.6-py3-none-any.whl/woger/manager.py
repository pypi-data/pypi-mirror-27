import warnings
from pathlib import Path

import os
from typing import Optional,  Type

from .storage import WorkspaceStorage
from .state import WorkspaceState
from .base_workspace import BaseWorkspace

_TARGET = 'target'
_CURRENT = 'current'

def _load_workspaces(root_path: Path, workspace_cls):
    path_list = [
        root_path / path
        for path in os.listdir(root_path)
        if os.path.isdir(root_path / path)
    ]
    return map(workspace_cls, path_list)


class WorkspaceManager:
    """Manages workspaces

    Allows you to
    - detect workspaces
    - manage current, target and latest workspaces
    - track workspace actions
    - search for workspaces with finished actions
    """
    def __init__(self, path, workspace_cls: Type[BaseWorkspace]):
        """Initialize workspace manager

        Parameters
        ----------
        path: path-like
            Workspace storage path
        workspace_cls: class object of BaseWorkspace subclass
            Workspace class object
        """
        self.path = Path(path)
        self._state_path = Path('.state.json')
        os.makedirs(self.path, exist_ok=True)

        self.workspace_cls = workspace_cls

        workspaces = _load_workspaces(self.path, workspace_cls)
        self.storage = WorkspaceStorage(workspaces)

        self.state = WorkspaceState(self.state_path)

    @property
    def current_ws_id(self):
        return self.state[_CURRENT]

    @current_ws_id.setter
    def current_ws_id(self, value):
        import traceback
        traceback.print_stack()
        self.state[_CURRENT] = value

    @property
    def target_ws_id(self):
        return self.state[_TARGET]

    @target_ws_id.setter
    def target_ws_id(self, value):
        self.state[_TARGET] = value

    @property
    def state_path(self):
        """Path to the state file

        Is used internally
        """
        return self.path / self._state_path

    def create(self, name) -> BaseWorkspace:
        """Creates a Workspace

        Parameters
        ----------
        name: str or int
            Workspace name
        """
        if isinstance(name, int):
            name = str(name)
        path = self.path / name
        ws = self.workspace_cls(path)
        self.storage.add(ws)
        return ws

    def latest(self) -> BaseWorkspace:
        """Returns latest workspace"""
        return self.storage.at(-1)

    def current(self) -> Optional[BaseWorkspace]:
        """Returns current workspace"""
        return self.storage[self.current_ws_id]

    def target(self) -> BaseWorkspace:
        """Returns target workspace"""
        return self.storage[self.target_ws_id]

    def __repr__(self):
        return '<{self.__class__.__name__}(path={self.path}, storage={self.storage})>'.format(self=self)

    def find_latest_finished(self, action) -> Optional[BaseWorkspace]:
        """Searches for latest workspace with finished action constraint"""
        workspaces = list(self.storage.values())
        for ws in reversed(workspaces):
            tracker = ws.track(action)
            if tracker.finished():
                return ws

    def target_latest(self):
        self.target_ws_id = self.latest().id

    def update(self):
        """Move from current workspace to target one"""
        if self.current_ws_id == self.target_ws_id:
            warnings.warn('Current and target workspaces are the same')
            return

        self.current_ws_id = self.target_ws_id
