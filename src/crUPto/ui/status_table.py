"""
status_table.py - Live-updating status table for crUPto using tUilKit Canvas, Cursor, Chroma.
Pure rendering logic, no printing/logging.
"""
from collections import OrderedDict

class StatusTable:
    def __init__(self, columns, order=None):
        self.columns = list(columns)
        self.order = list(order) if order else []
        self.rows = OrderedDict()

    def set_row(self, key, values):
        self.rows[key] = list(values)
        if self.order and key not in self.order:
            self.order.append(key)

    def remove_row(self, key):
        if key in self.rows:
            del self.rows[key]
        if key in self.order:
            self.order.remove(key)

    def _build_table(self):
        # Header
        header = [col for col in self.columns]
        sep = ["─" * max(3, len(col)) for col in self.columns]
        # Row order: use self.order if set, else insertion order
        keys = self.order if self.order else list(self.rows.keys())
        lines = ["  ".join(header), "  ".join(sep)]
        for key in keys:
            if key in self.rows:
                row = self.rows[key]
                styled = [row[0]]
                if len(row) > 1:
                    styled.append(row[1])
                styled.extend(row[2:])
                lines.append("  ".join(styled))
        return lines

    def render(self):
        lines = self._build_table()
        return "\n".join(lines) + "\n"

    def update(self):
        lines = self._build_table()
        return "\n".join(lines) + "\n"

    def clear(self):
        self.rows.clear()

    def as_text(self):
        lines = self._build_table()
        return "\n".join(lines) + "\n"
