# action_logger.py
import datetime


class ActionLogger:
    def __init__(self, persistence):
        self.persistence = persistence

    def log(self, event_type: str, payload: dict):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": event_type,
            "payload": payload,
        }
        self.persistence.append(entry)
