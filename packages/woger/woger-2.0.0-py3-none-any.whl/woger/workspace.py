import os

from woger.base_path_structure import BasePathStructure
from .action_tracker import ActionTracker
from .base_action import BaseAction
from .state import WorkspaceState


class Workspace:
    """Base class for Workspace subclasses

    Examples
    --------

    .. include:: ../examples/basic_workspace.rst

    """

    def __init__(self, path_structure: BasePathStructure):
        """Creates a workspace

        Parameters
        ----------
        root: path-like
            Workspace root path
        path_structure: BasePathStructure subclass
            Filled path structure to create Workspace instances
        """
        self.path = path_structure
        os.makedirs(str(self.root), exist_ok=True)

        self.state_path = self.root / '.state.json'
        self.state = WorkspaceState(self.state_path)

    @property
    def root(self):
        return self.path._root

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.root)

    @property
    def id(self):
        """Workspace id attribute

        Id is used to sort workspaces from oldest to latest
        """
        dirname = self.root.name
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
        return self.root == other.root
