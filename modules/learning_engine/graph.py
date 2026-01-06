from __future__ import annotations
from typing import Any
from .persistence import LearningPersistence


class GraphAnalyzer:
    def __init__(self, persistence: LearningPersistence) -> None:
        self.persistence = persistence

    def _get_hist(self):
        return [e for e in self.persistence.data if e.get("event") == "historical_import"]

    def compute_links(self) -> list[dict[str, Any]]:
        hist = self._get_hist()
        linkmap = {}
        for e in hist:
            p = e.get("payload", {}) or {}
            mods = [
                str(m[0]) for m in p.get("module_heatmap", []) if isinstance(m, (list, tuple)) and m
            ]
            runs = [
                str(r[0])
                for r in p.get("runner_frequency", [])
                if isinstance(r, (list, tuple)) and r
            ]

            for r in runs:
                for m in mods:
                    linkmap[(r, m)] = linkmap.get((r, m), 0) + 1

        out = [{"runner": a, "module": b, "weight": w} for (a, b), w in linkmap.items()]
        out.sort(key=lambda x: x["weight"], reverse=True)
        return out
