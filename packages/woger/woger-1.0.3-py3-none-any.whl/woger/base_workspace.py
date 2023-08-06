from functools import total_ordering
from pathlib import Path

import os
from typing import Union

from .action_tracker import ActionTracker
from .base_action import BaseAction
from .state import WorkspaceState
from .workspace_meta import WorkspaceMeta


class NotDefinedError(Exception):
    pass


class BaseWorkspace(metaclass=WorkspaceMeta):
    """Base class for Workspace subclasses

    Examples
    --------

    .. include:: ../examples/basic_workspace.rst

    """
    state_path = '.state.json'

    def __init__(self, path: Union[bytes, str]):
        """Creates a workspace

        Parameters
        ----------
        path: path-like
            Workspace path
        """
        self.path = Path(path)
        os.makedirs(str(self.path), exist_ok=True)

        self.state = WorkspaceState(self.state_path)

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.path)

    @property
    def id(self):
        """Workspace id attribute

        Id is used to sort workspaces from oldest to latest
        """
        dirname = self.path.parts[-1]
        try:
            return int(dirname)
        except ValueError:
            return str(dirname)

    def track(self, action: BaseAction) -> ActionTracker:
        """Tracks the action inside the workspace

        Creates an ActionTracker object with action and this workspace as constructor parameters

        Parameters
        ----------
        action: subclass of BaseAction
            Action to track
        """
        return ActionTracker(action, self)

    def __eq__(self, other):
        return self.path == other.path
