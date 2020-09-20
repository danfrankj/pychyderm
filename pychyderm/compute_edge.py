from typing import Optional, Any, Dict
from pychyderm.versioned_object import VersionedObject


class ComputeEdge(VersionedObject):
    def __init__(self, edge_id: str) -> None:
        self._edge_id = edge_id
        self._storage: Dict[str, Any] = {}  # TODO abstract storage
        self._commit_sha: Optional[str] = None

    @property
    def edge_id(self) -> str:
        return self._edge_id

    @property
    def id(self):
        return self.edge_id

    def validate_commit_obj(self, obj) -> bool:
        return callable(obj)

    def compute(self, data, commit_sha: Optional[str] = None):
        return self._storage[commit_sha or self.commit_sha](data=data)
