import time

from woger import BaseWorkspace


def _load_xml(fs, ws):
    fs.CreateFile(ws.raw_path)


def _parse_xml(fs, ws):
    fs.CreateFile(ws.parsed_path)


def test_manager_workspace_update(fs):
    from woger import WorkspaceManager, BaseAction

    class Workspace(BaseWorkspace):
        raw_path = 'data.xml'
        parsed_path = 'data.json'

    class Action(BaseAction):
        load_xml = 'load_data'
        parse_xml = 'parse_xml'

    manager = WorkspaceManager('root', Workspace)
    assert manager.current() is None

    latest_finished_ws = manager.find_latest_finished(Action.parse_xml)
    assert latest_finished_ws is None

    timestamp = 1346134
    manager.create(timestamp)
    manager.target_latest()

    ws = manager.target()
    tracker = ws.track(Action.load_xml)

    if not tracker.finished():
        assert tracker.started() or tracker.failed() or tracker.undefined()
        with tracker:
            assert tracker.started()
            _load_xml(fs, ws)
        assert tracker.finished()

    tracker = ws.track(Action.parse_xml)

    if not tracker.finished():
        with tracker:
            assert tracker.started()
            _parse_xml(fs, ws)
        assert tracker.finished()

    assert manager.current() is None
    manager.update()
    assert manager.current() == manager.storage[timestamp] == manager.target()
