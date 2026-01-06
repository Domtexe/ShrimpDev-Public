"""
Robust action router for UI layers (NO Tk imports).

Intent:
- UI calls `call_action(app, logic_tools, action_name, logger=...)`
- No globals(), minimal assumptions
- Best-effort: if action missing -> returns False, no crash
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

@dataclass(frozen=True)
class CallResult:
    ok: bool
    message: str = ""

def _log(logger: Optional[Callable[[str], None]], msg: str) -> None:
    try:
        if logger:
            logger(msg)
    except Exception:
        pass

def resolve_action(logic_tools: Any, action_name: str) -> Optional[Callable[..., Any]]:
    """Return callable action from logic_tools if present."""
    try:
        fn = getattr(logic_tools, action_name, None)
        return fn if callable(fn) else None
    except Exception:
        return None

def call_action(
    app: Any,
    logic_tools: Any,
    action_name: str,
    *,
    logger: Optional[Callable[[str], None]] = None,
) -> CallResult:
    """Call an action safely. Never raises (best-effort)."""
    if not action_name or not isinstance(action_name, str):
        return CallResult(False, "invalid action name")

    fn = resolve_action(logic_tools, action_name)
    if fn is None:
        _log(logger, f"[action_router] missing: {action_name}")
        return CallResult(False, f"missing: {action_name}")

    try:
        fn(app)
        _log(logger, f"[action_router] ok: {action_name}")
        return CallResult(True, "ok")
    except Exception as e:
        _log(logger, f"[action_router] fail: {action_name}: {e}")
        return CallResult(False, f"exception: {e}")
