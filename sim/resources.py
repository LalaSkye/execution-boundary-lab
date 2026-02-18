"""In-memory simulated resources. No external I/O."""

import copy


class Filesystem:
    """Dict-based fake filesystem."""

    def __init__(self):
        self._store = {}

    def write(self, path: str, data):
        parts = path.strip("/").split("/")
        node = self._store
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = data

    def read(self, path: str):
        parts = path.strip("/").split("/")
        node = self._store
        for part in parts:
            node = node[part]
        return node

    def exists(self, path: str) -> bool:
        try:
            self.read(path)
            return True
        except (KeyError, TypeError):
            return False

    def delete(self, path: str, recursive: bool = False):
        parts = path.strip("/").split("/")
        node = self._store
        for part in parts[:-1]:
            node = node[part]
        target = parts[-1]
        if recursive and isinstance(node.get(target), dict):
            del node[target]
        elif isinstance(node.get(target), dict) and node[target]:
            raise RuntimeError(f"Cannot delete non-empty directory: {path}")
        else:
            del node[target]

    def snapshot(self) -> dict:
        return copy.deepcopy(self._store)


class Database:
    """Dict-based fake database."""

    def __init__(self):
        self._tables = {}

    def insert(self, table: str, record_id: str, data: dict):
        self._tables.setdefault(table, {})
        self._tables[table][record_id] = copy.deepcopy(data)

    def update(self, table: str, record_id: str, data: dict):
        if table not in self._tables or record_id not in self._tables[table]:
            raise KeyError(f"Record {record_id} not found in {table}")
        self._tables[table][record_id].update(data)

    def read(self, table: str, record_id: str) -> dict:
        return copy.deepcopy(self._tables[table][record_id])

    def delete(self, table: str, record_id: str):
        del self._tables[table][record_id]

    def find_first(self, table: str) -> tuple:
        """Return (record_id, data) for the first record in a table."""
        if table not in self._tables or not self._tables[table]:
            raise KeyError(f"No records in {table}")
        record_id = next(iter(self._tables[table]))
        return record_id, copy.deepcopy(self._tables[table][record_id])

    def snapshot(self) -> dict:
        return copy.deepcopy(self._tables)


class ResourceManager:
    """Holds all simulated resources."""

    def __init__(self):
        self.fs = Filesystem()
        self.db = Database()

    def snapshot(self) -> dict:
        return {
            "filesystem": self.fs.snapshot(),
            "database": self.db.snapshot(),
        }
