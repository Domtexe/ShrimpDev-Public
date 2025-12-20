# suggestion_provider.py
class SuggestionProvider:
    def __init__(self, persistence, patterns):
        self.persistence = persistence
        self.patterns = patterns

    def get_suggestions(self):
        out = []

        recent = self.patterns.recent_activity()
        if recent:
            out.append(f"Zuletzt bearbeitet: {recent[-1].get('payload',{}).get('file','(unbekannt)')}")

        mods = self.patterns.most_common_modules()
        if mods:
            top = sorted(mods.items(), key=lambda x: x[1], reverse=True)[0]
            out.append(f"Auffälliges Modul: {top[0]} ({top[1]} Aktionen)")

        return out
