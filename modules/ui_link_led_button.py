from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class LinkLedButton(ttk.Frame):
    """
    Classic-looking compound control:
    [ Link ] with a small right-aligned square LED INSIDE the button.
    - No checkbox look
    - No images
    - LED indicates state: off/on/busy/error
    """

    def __init__(
        self,
        master,
        text: str = "Link",
        command=None,
        width: int = 64,
        height: int = 22,
        led_size: int = 8,
        padding_x: int = 6,
        **kw
    ):
                # Swallow legacy kwargs from older toolbar implementations
        # (must be removed before ttk.Frame init, otherwise TclError)
        kw.pop('show_icon', None)
        kw.pop('icon', None)
        kw.pop('icon_image', None)
        kw.pop('image', None)
        kw.pop('compound', None)
        super().__init__(master, **kw)
        self.command = command
        self._base_text = text
        self._state = "off"
        self._enabled = True

        # Light/classic palette matching ShrimpDev classic UI
        self.COL_BG = "#f0f0f0"
        self.COL_BG_HOVER = "#e6e6e6"
        self.COL_BORDER = "#7a7a7a"
        self.COL_TEXT = "#000000"
        self.COL_TEXT_DIM = "#777777"

        self.COL_OFF_LED = "#c9c9c9"
        self.COL_ON_LED = "#2ad36f"
        self.COL_BUSY_LED = "#ffb020"
        self.COL_ERR_LED = "#ff3b3b"

        self.width = int(width)
        self.height = int(height)
        self.led_size = int(led_size)
        self.padding_x = int(padding_x)

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=False)

        # Base button rect
        self._bg_rect = self.canvas.create_rectangle(
            0, 0, self.width - 1, self.height - 1,
            fill=self.COL_BG, outline=self.COL_BORDER, width=1
        )

        # Text (left)
        self._text = self.canvas.create_text(
            self.padding_x,
            self.height // 2,
            text=text,
            anchor="w",
            fill=self.COL_TEXT,
            font=("Segoe UI", 9),
        )

        # LED square (right, INSIDE)
        led_x2 = self.width - self.padding_x
        led_x1 = led_x2 - self.led_size
        led_y1 = (self.height - self.led_size) // 2
        led_y2 = led_y1 + self.led_size

        self._led_border = self.canvas.create_rectangle(
            led_x1, led_y1, led_x2, led_y2,
            outline=self.COL_BORDER, width=1, fill=""
        )
        self._led_fill = self.canvas.create_rectangle(
            led_x1 + 1, led_y1 + 1, led_x2 - 1, led_y2 - 1,
            outline="", fill=self.COL_OFF_LED
        )

        # Bindings (whole surface clickable)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Enter>", self._on_hover)
        self.canvas.bind("<Leave>", self._on_hover)
        for item in (self._bg_rect, self._text, self._led_border, self._led_fill):
            self.canvas.tag_bind(item, "<Button-1>", self._on_click)

        self.set_state("off")

    def _on_hover(self, ev):
        if not self._enabled:
            return
        if ev.type == tk.EventType.Enter:
            self.canvas.itemconfig(self._bg_rect, fill=self.COL_BG_HOVER)
        else:
            self.canvas.itemconfig(self._bg_rect, fill=self.COL_BG)

    def _on_click(self, _ev=None):

        if not self._enabled:

            return

        if callable(self.command):

            self.command()



    def set_enabled(self, enabled: bool):
        self._enabled = bool(enabled)
        if not self._enabled:
            self.canvas.itemconfig(self._text, fill=self.COL_TEXT_DIM)
            self.canvas.itemconfig(self._bg_rect, fill=self.COL_BG)
        else:
            self.canvas.itemconfig(self._text, fill=self.COL_TEXT)
            self.set_state(self._state)

    def set_state(self, state: str):

        """Set LED state and keep LED geometry visible under toolbar resizing."""

        st = (state or "").lower().strip()

        if st not in ("off", "on", "busy", "error"):

            st = "off"

        self._state = st


        # --- Relayout to current canvas size (prevents off-screen LED) ---

        try:

            w = int(self.canvas.winfo_width() or 0)

            h = int(self.canvas.winfo_height() or 0)

            if w <= 4: w = int(getattr(self, "width", 0) or 0)

            if h <= 4: h = int(getattr(self, "height", 0) or 0)

            if w > 8 and h > 8:

                # background

                try:

                    self.canvas.coords(self._bg_rect, 1, 1, w-1, h-1)

                except Exception:

                    pass

                # LED

                px = int(getattr(self, "padding_x", 10) or 10)

                ls = int(getattr(self, "led_size", 10) or 10)

                led_x2 = w - px

                led_x1 = led_x2 - ls

                led_y1 = (h - ls) // 2

                led_y2 = led_y1 + ls

                try:

                    self.canvas.coords(self._led_border, led_x1, led_y1, led_x2, led_y2)

                except Exception:

                    pass

                try:

                    self.canvas.coords(self._led_fill, led_x1+1, led_y1+1, led_x2-1, led_y2-1)

                except Exception:

                    pass

                try:

                    self.canvas.tag_raise(self._led_fill)

                    self.canvas.tag_raise(self._led_border)

                except Exception:

                    pass

        except Exception:

            pass


        # --- Disabled behavior ---

        if not self._enabled:

            try:

                self.canvas.itemconfig(self._led_fill, fill=self.COL_OFF_LED)

                self.canvas.tag_raise(self._led_fill)

                self.canvas.tag_raise(self._led_border)

            except Exception:

                pass

            return
        # --- Color selection (LED only) ---
        if st == "off":
            led = self.COL_OFF_LED
        elif st == "on":
            led = self.COL_ON_LED
        elif st == "busy":
            led = self.COL_BUSY_LED
        else:
            led = self.COL_ERR_LED

        # --- Update LED ---

        try:

            self.canvas.itemconfig(self._led_fill, fill=led)

            self.canvas.tag_raise(self._led_fill)

            self.canvas.tag_raise(self._led_border)

        except Exception:

            pass

