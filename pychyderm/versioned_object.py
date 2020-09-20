import time
import datetime
import hashlib
from typing import Dict
from dataclasses import dataclass
from collections import OrderedDict
from termcolor import colored
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime.datetime
    message: str
    author: str
    commit_sha: str


class VersionedObject(ABC):  # Mixin
    @property
    def commit_sha(self) -> str:
        assert self._commit_sha is not None
        return self._commit_sha

    @property
    def commit_log(self) -> Dict[str, LogEntry]:
        if not hasattr(self, "_commit_log"):
            self._commit_log = OrderedDict()
        return self._commit_log

    @abstractmethod
    def validate_commit_obj(self, obj) -> bool:
        pass

    def commit(self, obj, commit_sha=None, message="no message", author="unknown"):

        commit_time = datetime.datetime.now()
        commit_sha = (
            commit_sha
            or hashlib.sha256(str(commit_time.timestamp()).encode("utf8")).hexdigest()
        )
        log_entry = LogEntry(
            author=author, message=message, timestamp=commit_time, commit_sha=commit_sha
        )
        if self.has_commit(commit_sha):
            raise KeyError(f"Attempted to commit an already commited sha {log_entry} ")
        if not self.validate_commit_obj(obj):
            raise ValueError(f"invalid commit to {type(self)}:{self.id}. {log_entry}")
        self._storage[commit_sha] = obj
        self.commit_log[commit_sha] = log_entry
        self._commit_sha = commit_sha

    def print_log(self) -> None:
        for sha, entry in self.commit_log.items():
            print(colored(f"commit {sha}", "yellow"))
            print(f"Author: {entry.author}")
            print(f"Date: {entry.timestamp}")
            print("")
            print(f"    {entry.message}")
            print("")

    def checkout(self, commit_sha: str) -> None:
        assert commit_sha in self._storage
        self._commit_sha = commit_sha

    def checkout_by_message(self, message: str) -> LogEntry:
        matched_entries = [
            entry for entry in self.commit_log.values() if entry.message == message
        ]
        if len(matched_entries) == 0:
            raise ValueError("unable to find commit with that message")
        if len(matched_entries) > 1:
            raise ValueError("found multiple entries with that message")
        return matched_entries[0]

    def has_commit(self, commit_sha: str) -> bool:
        return commit_sha in self._storage