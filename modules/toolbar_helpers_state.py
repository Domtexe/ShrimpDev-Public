# toolbar_helpers_state.py
# R2954: Safe, minimal button state setter (no debug, no legacy vars)

from __future__ import annotations

def safe_set_btn_state(btn, enabled: bool, busy: bool = False) -> None:
    """
    Robust replacement for legacy _set_btn_state.
    - Never references undefined vars
    - No debug side-effects
    - Guards against missing Tk methods
    """
    try:
        # Normalize desired state
        state = "normal" if enabled and not busy else "disabled"

        # Tk Button compatibility
        if hasattr(btn, "configure"):
            btn.configure(state=state)
        elif hasattr(btn, "config"):
            btn.config(state=state)

        # Optional visual cue if present
        if hasattr(btn, "update_idletasks"):
            btn.update_idletasks()
    except Exception:
        # Intentionally swallow: UI must not crash on state updates
        return
