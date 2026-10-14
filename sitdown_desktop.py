#!/usr/bin/env python3
"""The Sitdown BBS desktop launcher. Standard-library Tkinter GUI."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import zipfile

ROOT = Path(__file__).resolve().parent
DATA = Path.home() / ".sitdown-bbs"
CONFIG = DATA / "launcher.json"
THEME = {"background": "#121212", "panel": "#242424", "primary": "#C62828",
         "connected": "#008C45", "text": "#F5F5F0", "highlight": "#F4B942"}
COMMANDS = [
    ("/sitdown", "Main menu"), ("/help", "Quick help"),
    ("/mail", "Check your mail"), ("/boards", "The Social Club"),
    ("/fortune", "Jersey wisdom"), ("/tools", "Utilities"),
    ("/cancel", "Return to main menu"),
]


class SitdownApp:
    def __init__(self, root):
        self.root = root
        self.proc = None
        self.started = None
        self.demo = tk.BooleanVar(value=False)
        self.connection = tk.StringVar(value="serial")
        self.address = tk.StringVar()
        self.community = tk.StringVar(value="The Sitdown BBS")
        self.welcome = tk.StringVar(value="Ayyy, pull up a chair. We gotta talk.")
        self.status = tk.StringVar(value="Stopped")
        self.colors = THEME
        self.root.title("THE SITDOWN BBS | North Jersey Communications Division")
        self.root.geometry("840x670")
        self.root.configure(bg=THEME["background"])
        self.load()
        self.build()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(1000, self.poll)

    def load(self):
        if CONFIG.exists():
            try:
                data = json.loads(CONFIG.read_text(encoding="utf-8"))
                self.connection.set(data.get("connection", "serial"))
                self.address.set(data.get("address", ""))
                self.community.set(data.get("community", "The Sitdown BBS"))
                self.welcome.set(data.get("welcome", self.welcome.get()))
            except (ValueError, OSError):
                pass

    def save(self):
        DATA.mkdir(parents=True, exist_ok=True)
        CONFIG.write_text(json.dumps({
            "connection": self.connection.get(), "address": self.address.get(),
            "community": self.community.get(), "welcome": self.welcome.get()
        }, indent=2), encoding="utf-8")
        self.log("The Family Business: settings saved.")

    def build(self):
        c = self.colors
        def label(parent, text, size=11, color=None):
            return tk.Label(parent, text=text, font=("Helvetica", size, "bold"),
                            fg=color or c["text"], bg=c["background"])
        def button(parent, text, command, color=None):
            return tk.Button(parent, text=text, command=command, bg=color or c["primary"],
                             fg="white", activebackground=c["highlight"], relief="flat",
                             padx=13, pady=8, font=("Helvetica", 11, "bold"))
        label(self.root, "🤌 THE SITDOWN BBS", 25, c["highlight"]).pack(pady=(18, 1))
        label(self.root, "North Jersey Communications Division", 12).pack()
        label(self.root, "Ayyy, pull up a chair. We gotta talk.", 10).pack(pady=(2, 12))
        panel = tk.Frame(self.root, bg=c["background"])
        panel.pack(fill="x", padx=20)
        tk.Radiobutton(panel, text="USB / Serial radio", variable=self.connection,
                       value="serial", bg=c["background"], fg=c["text"], selectcolor=c["panel"]).pack(side="left")
        tk.Radiobutton(panel, text="Network radio", variable=self.connection,
                       value="tcp", bg=c["background"], fg=c["text"], selectcolor=c["panel"]).pack(side="left")
        tk.Checkbutton(panel, text="Demo mode (no radio)", variable=self.demo,
                       bg=c["background"], fg=c["highlight"], selectcolor=c["panel"]).pack(side="right")
        label(self.root, "Serial port (optional) or radio IP / hostname", 10).pack(anchor="w", padx=20, pady=(8, 2))
        tk.Entry(self.root, textvariable=self.address, bg=c["panel"], fg=c["text"],
                 insertbackground=c["text"], relief="flat", font=("Helvetica", 12)).pack(fill="x", padx=20, ipady=8)
        actions = tk.Frame(self.root, bg=c["background"])
        actions.pack(fill="x", padx=20, pady=12)
        for title, fn, color in [
            ("Start the Sitdown", self.start, c["connected"]),
            ("Fuggedaboutit (Stop)", self.stop, c["primary"]),
            ("The Playbook", self.commands, c["panel"]),
            ("The Family Business", self.settings, c["panel"]),
            ("The Books", self.backup, c["panel"])
        ]:
            button(actions, title, fn, color).pack(side="left", padx=(0, 7))
        label(self.root, "Status:", 11).pack(anchor="w", padx=20)
        tk.Label(self.root, textvariable=self.status, bg=c["background"],
                 fg=c["connected"], font=("Helvetica", 12, "bold")).pack(anchor="w", padx=20)
        self.output = tk.Text(self.root, bg=c["panel"], fg=c["text"], insertbackground=c["text"],
                              wrap="word", relief="flat", state="disabled", height=17)
        self.output.pack(fill="both", expand=True, padx=20, pady=(12, 20))
        self.log("Ready, pal. Pick a radio, or check Demo mode.")

    def log(self, message):
        self.output.configure(state="normal")
        self.output.insert("end", message + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def start(self):
        if self.proc or self.demo.get() and self.status.get() == "Demo running":
            return
        if self.demo.get():
            self.status.set("Demo running")
            self.log("DEMO: The Sitdown is open. No radio messages will be sent.")
            return
        self.save()
        config = ROOT / "config.ini"
        if not config.exists():
            messagebox.showerror("Need a Guy?", "Missing config.ini. Copy example_config.ini to config.ini and configure it first.")
            return
        cmd = [sys.executable, "-u", str(ROOT / "server.py"), "--config", str(config),
               "--interface-type", self.connection.get()]
        addr = self.address.get().strip()
        if addr:
            cmd += ["--host" if self.connection.get() == "tcp" else "--port", addr]
        try:
            self.proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, text=True)
            self.status.set("Connecting...")
            self.log("Starting BBS server...")
        except OSError as exc:
            self.proc = None
            messagebox.showerror("Ayy, somethin' ain't right!", str(exc))

    def poll(self):
        if self.proc:
            code = self.proc.poll()
            if code is not None:
                self.log(f"Server exited with code {code}. Check your radio and configuration.")
                self.status.set("Stopped")
                self.proc = None
            else:
                self.status.set("Server running (radio status unverified)")
        if self.root.winfo_exists():
            self.root.after(1000, self.poll)

    def stop(self):
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
            self.proc = None
        self.status.set("Stopped")
        self.log("Fuggedaboutit. Server stopped.")

    def commands(self):
        win = tk.Toplevel(self.root)
        win.title("The Playbook | Radio Commands")
        win.configure(bg=THEME["background"])
        tk.Label(win, text="DM these commands to your BBS radio", bg=THEME["background"],
                 fg=THEME["highlight"], font=("Helvetica", 14, "bold")).pack(padx=20, pady=12)
        selected = tk.StringVar(value=COMMANDS[0][0])
        for cmd, desc in COMMANDS:
            tk.Radiobutton(win, text=f"{cmd} — {desc}", value=cmd, variable=selected,
                           bg=THEME["background"], fg=THEME["text"],
                           selectcolor=THEME["panel"], anchor="w").pack(fill="x", padx=20)
        def copy():
            win.clipboard_clear()
            win.clipboard_append(selected.get())
            win.update()
        tk.Button(win, text="Copy selected command", command=copy,
                  bg=THEME["primary"], fg="white").pack(pady=15)

    def settings(self):
        win = tk.Toplevel(self.root)
        win.title("The Family Business")
        win.configure(bg=THEME["background"])
        for name, var in [("Community name", self.community), ("Welcome message (local setting)", self.welcome)]:
            tk.Label(win, text=name, bg=THEME["background"], fg=THEME["text"]).pack(anchor="w", padx=20, pady=(12, 0))
            tk.Entry(win, textvariable=var, width=55, bg=THEME["panel"], fg=THEME["text"],
                     insertbackground=THEME["text"]).pack(padx=20)
        tk.Label(win, text="Custom welcome is saved locally; radio reply integration is pending.",
                 bg=THEME["background"], fg=THEME["highlight"]).pack(padx=20, pady=10)
        tk.Button(win, text="Save", command=self.save, bg=THEME["connected"], fg="white").pack(pady=12)

    def backup(self):
        DATA.mkdir(parents=True, exist_ok=True)
        destination = filedialog.asksaveasfilename(defaultextension=".zip",
                     initialfile="sitdown-backup.zip", filetypes=[("Zip archive", "*.zip")])
        if not destination:
            return
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in [CONFIG, ROOT / "config.ini", *ROOT.glob("*.db")]:
                if path.exists() and path.is_file():
                    archive.write(path, path.name)
        self.log("The Books: backup saved. Treat backups as sensitive; they may contain messages and keys.")

    def close(self):
        self.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    SitdownApp(root)
    root.mainloop()
