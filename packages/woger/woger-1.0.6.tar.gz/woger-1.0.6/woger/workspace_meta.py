from pathlib import Path


def _get_path_property(hidden_name):
    def _joined_path(self):
        child_path = getattr(self, hidden_name)
        return self.path / child_path

    return property(_joined_path)


class WorkspaceMeta(type):
    def __new__(mcs, cls_name, bases, attrib):
        mapping = {}

        for name, value in attrib.items():
            if name.startswith('_') or name in ['path', 'id', 'track', 'state']:
                mapping[name] = value
                continue

            hidden_name = '_' + name
            mapping[hidden_name] = Path(value)
            mapping[name] = _get_path_property(hidden_name)

        return super().__new__(mcs, cls_name, bases, mapping)
