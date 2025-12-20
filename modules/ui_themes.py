from tkinter import ttk
def apply_default(app):
    style = ttk.Style(app)
    app.bind("<<ToggleTheme>>", lambda e: None)  # Hook reserviert
