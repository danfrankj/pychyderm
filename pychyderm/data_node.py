from pychyderm.versioned_object import VersionedObject


class DataNode(VersionedObject):
    def __init__(self, node_id):
        self.node_id = node_id
        self._commit_sha = None
        self._storage = {}  # TODO abstract storage

    def extract(self, commit_sha=None):
        return self._storage[commit_sha or self.commit_sha]