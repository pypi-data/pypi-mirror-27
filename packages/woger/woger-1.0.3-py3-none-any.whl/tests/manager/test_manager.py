from pathlib import Path


def test_manager_latest_workspace(fs):
    from woger import WorkspaceManager, BaseWorkspace

    class Workspace(BaseWorkspace):
        def __lt__(self, other):
            return self.state_path < other.state_path

    root = Path('/') / 'global'
    subdirs = [
        root / name
        for name in ['134', '235', '9', '17']
    ]
    for subdir in subdirs:
        fs.CreateDirectory(subdir)

    wm = WorkspaceManager(root, Workspace)

    assert wm.latest().id == 235


def test_manager_current_and_target(fs):
    from woger import WorkspaceManager, BaseWorkspace

    root = Path('/') / 'global'
    ws1_path = root / str(346134)
    ws2_path = root / str(824842)
    state_path = root / '.state.json'

    fs.CreateFile(
        state_path,
        contents='\n'.join([
            '{',
            '"current": 346134,',
            '"target": 824842',
            '}'
        ])
    )
    fs.CreateDirectory(ws1_path)
    fs.CreateDirectory(ws2_path)

    class Workspace(BaseWorkspace):
        pass

    manager = WorkspaceManager(
        root,
        Workspace,
    )

    assert manager.state_path == state_path
    assert manager.current().path == ws1_path
    assert manager.target().path == ws2_path


def test_manager_search_latest_finished(fs):
    from woger import WorkspaceManager, BaseWorkspace, BaseAction

    root = Path('root')

    fs.CreateFile(
        root / '346' / '.state.json',
        contents='{"load_raw_xml":"finished","parse_xml": "finished"}',
    )
    fs.CreateFile(
        root / '134' / '.state.json',
        contents='{"load_raw_xml":"finished","parse_xml": "finished"}',
    )
    fs.CreateFile(
        root / '576' / '.state.json',
        contents='{"load_raw_xml": "finished","parse_xml": "started"}',
    )

    class Action(BaseAction):
        load_raw_xml = 'load_raw_xml'
        parse_xml = 'parse_xml'

    wm = WorkspaceManager(root, BaseWorkspace)
    ws = wm.find_latest_finished(Action.parse_xml)

    assert ws.id == 346


def test_manager_search_latest_finished_none(fs):
    from woger import WorkspaceManager, BaseWorkspace, BaseAction

    root = Path('root')

    fs.CreateFile(
        root / '346' / '.state.json',
        contents='{"load_raw_xml":"finished","parse_xml": "failed"}',
    )
    fs.CreateFile(
        root / '134' / '.state.json',
        contents='{"load_raw_xml": "started"}',
    )
    fs.CreateFile(
        root / '576' / '.state.json',
        contents='{"load_raw_xml": "finished","parse_xml": "started"}',
    )

    class Action(BaseAction):
        load_raw_xml = 'load_raw_xml'
        parse_xml = 'parse_xml'

    wm = WorkspaceManager(root, BaseWorkspace)
    ws = wm.find_latest_finished(Action.parse_xml)

    assert ws is None
