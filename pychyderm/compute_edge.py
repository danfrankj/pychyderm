from pychyderm.versioned_object import VersionedObject


class ComputeEdge(VersionedObject):
    def __init__(self, edge_id):
        self.edge_id = edge_id
        self._storage = {}  # TODO abstract storage
        self._commit_sha = None

    def compute(self, data, commit_sha=None):
        return self._storage[commit_sha or self.commit_sha](data=data)
