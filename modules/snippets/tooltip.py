import tkinter as tk
class Tooltip:
    def __init__(self, widget, text:str="", delay:int=550):
        self.widget=widget; self.text=text; self.delay=delay
        self.tip=None; self._after=None
        widget.bind("<Enter>", self._schedule); widget.bind("<Leave>", self._hide)

    def _schedule(self, _e=None):
        self._after = self.widget.after(self.delay, self._show)

    def _show(self):
        if self.tip: return
        x,y,cx,cy = self.widget.bbox("insert") or (0,0,0,0)
        x += self.widget.winfo_rootx()+12; y += self.widget.winfo_rooty()+24
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(tw, text=self.text, bg="#ffffe0", relief="solid", borderwidth=1)
        lbl.pack(ipadx=4, ipady=2)

    def _hide(self, _e=None):
        if self._after: self.widget.after_cancel(self._after); self._after=None
        if self.tip:
            self.tip.destroy(); self.tip=None
