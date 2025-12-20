from tkinter import messagebox
import tkinter as tk

def build_intake_tab(parent, app):
    frm = tk.Frame(parent); frm.pack(fill="both", expand=True, padx=12, pady=12)
    tk.Label(frm, text="ShrimpDev Intake").pack(anchor="w")
    tk.Label(frm, text="Ziel: Code/Module/Runner verarbeiten - kein ShrimpHub-Flow.").pack(anchor="w", pady=(2,8))

def do_scan(app):
    messagebox.showinfo("Scan Project", "Projekt wird gescannt... (Demo)")

# Platzhalter für spätere Dev-Tasks
