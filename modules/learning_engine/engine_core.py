# engine_core.py
from .persistence import LearningPersistence
from .action_logger import ActionLogger
from .pattern_analyzer import PatternAnalyzer
from .suggestion_provider import SuggestionProvider
from .knowledge_graph import KnowledgeGraph


class LearningEngine:
    def __init__(self):
        self.persistence = LearningPersistence()
        self.logger = ActionLogger(self.persistence)
        self.patterns = PatternAnalyzer(self.persistence)
        self.suggestions = SuggestionProvider(self.persistence, self.patterns)
        self.graph = KnowledgeGraph(self.persistence)

    def log(self, event_type: str, payload: dict):
        self.logger.log(event_type, payload)

    def get_suggestions(self):
        return self.suggestions.get_suggestions()
