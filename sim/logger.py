"""Deterministic trace logger. No timestamps. Ordered event numbering."""


class TraceLogger:
    """Records execution events in deterministic order."""

    def __init__(self):
        self._events = []
        self._counter = 0

    def log(self, event_type: str, detail: str, data: dict = None):
        self._counter += 1
        entry = {
            "seq": self._counter,
            "event": event_type,
            "detail": detail,
        }
        if data is not None:
            entry["data"] = data
        self._events.append(entry)

    def get_trace(self) -> list:
        return list(self._events)

    def format_trace(self) -> str:
        lines = []
        for e in self._events:
            line = f"[{e['seq']:04d}] {e['event']}: {e['detail']}"
            if "data" in e:
                line += f" | {e['data']}"
            lines.append(line)
        return "\n".join(lines)

    def reset(self):
        self._events = []
        self._counter = 0
