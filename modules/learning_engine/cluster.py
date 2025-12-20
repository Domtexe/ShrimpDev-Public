# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List, Dict, Any
from .persistence import LearningPersistence

class ClusterAnalyzer:
    def __init__(self, persistence: LearningPersistence) -> None:
        self.persistence = persistence

    def _get_hist(self):
        return [e for e in self.persistence.data if e.get("event")=="historical_import"]

    def compute_error_clusters(self) -> List[Dict[str,Any]]:
        hist = self._get_hist()
        agg={}
        for e in hist:
            hot = e.get("payload",{}).get("error_hotspots",[]) or []
            for item in hot:
                if not isinstance(item,(list,tuple)) or len(item)<2:
                    continue
                err=str(item[0]).strip()
                try: c=int(item[1])
                except: continue
                agg[err]=agg.get(err,0)+c
        out=[{"error":k,"count":v} for k,v in agg.items()]
        out.sort(key=lambda x:x["count"], reverse=True)
        return out

    def compute_success_clusters(self)->List[Dict[str,Any]]:
        hist=self._get_hist()
        agg={}
        for e in hist:
            hot=e.get("payload",{}).get("runner_frequency",[]) or []
            for item in hot:
                if not isinstance(item,(list,tuple)) or len(item)<2:
                    continue
                run=str(item[0]).strip()
                try:c=int(item[1])
                except: continue
                agg[run]=agg.get(run,0)+c
        out=[{"runner":k,"count":v} for k,v in agg.items()]
        out.sort(key=lambda x:x["count"], reverse=True)
        return out
