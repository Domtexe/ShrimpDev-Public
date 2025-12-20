# persistence.py
import json
from pathlib import Path

DB = Path(r"D:\ShrimpDev\learning_journal.json")

class LearningPersistence:
    def __init__(self):
        self.data = []
        self.load()

    def load(self):
        if DB.exists():
            try:
                self.data = json.loads(DB.read_text(encoding="utf-8"))
            except:
                self.data = []
        else:
            self.data = []

    def save(self):
        DB.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")

    def append(self, entry):
        self.data.append(entry)
        self.save()
