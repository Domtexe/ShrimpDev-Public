from __future__ import annotations
from typing import Any
from .persistence import LearningPersistence


class HeatmapAnalyzer:
    def __init__(self, persistence: LearningPersistence) -> None:
        self.persistence = persistence

    def _get_historical_events(self) -> list[dict[str, Any]]:
        events = []
        for e in self.persistence.data:
            if e.get("event") == "historical_import":
                events.append(e)
        events.sort(key=lambda x: x.get("timestamp", ""))
        return events

    def compute_module_scores(self) -> list[dict[str, Any]]:
        hist = self._get_historical_events()
        if not hist:
            return []
        n = len(hist)

        stats = {}
        for idx, entry in enumerate(hist):
            payload = entry.get("payload", {}) or {}
            heat = payload.get("module_heatmap", []) or []
            rec = 0.5 + float(idx + 1) / float(n)

            for item in heat:
                if not isinstance(item, (list, tuple)) or len(item) < 2:
                    continue
                modul = str(item[0])
                try:
                    count = float(item[1])
                except:
                    continue
                if modul not in stats:
                    stats[modul] = {"score": 0.0, "count": 0}
                stats[modul]["count"] += count
                stats[modul]["score"] += count * rec

        out = []
        for m, d in stats.items():
            out.append({"module": m, "score": d["score"], "count": int(d["count"])})
        out.sort(key=lambda x: x["score"], reverse=True)
        return out
