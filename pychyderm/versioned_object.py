import time
import hashlib


class VersionedObject:
    @property
    def commit_sha(self):
        assert self._commit_sha is not None
        return self._commit_sha

    def commit(self, obj, commit_sha=None, checkout=True):
        commit_sha = hashlib.sha265(str(time.time()).encode("utf8")).hexdigest()
        if self.has_commit(commit_sha):
            raise KeyError(f"already commited an object with sha {commit_sha}")
        self._storage[commit_sha] = obj
        if checkout:
            self.checkout(commit_sha)

    def checkout(self, commit_sha):
        assert commit_sha in self._storage
        self._commit_sha = commit_sha

    def has_commit(self, commit_sha):
        return commit_sha in self._storage