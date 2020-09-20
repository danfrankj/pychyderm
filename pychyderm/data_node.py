from pychyderm.versioned_object import VersionedObject


class DataNode(VersionedObject):
    def __init__(self, node_id: str) -> None:
        self._node_id = node_id
        self._commit_sha = None
        self._storage = {}  # TODO abstract storage

    @property
    def node_id(self):
        return self._node_id

    @property
    def id(self):
        return self.node_id

    def extract(self, commit_sha=None):
        return self._storage[commit_sha or self.commit_sha]

    def validate_commit_obj(self, obj) -> bool:
        return True  # TODO subclass Data Nodes


# TODO sublcass of DataNode