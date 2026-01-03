# pattern_analyzer.py
class PatternAnalyzer:
    def __init__(self, persistence):
        self.persistence = persistence

    def recent_activity(self):
        return self.persistence.data[-20:]

    def most_common_modules(self):
        stats = {}
        for e in self.persistence.data:
            p = e.get("payload", {})
            m = p.get("module")
            if m:
                stats[m] = stats.get(m, 0) + 1
        return stats
