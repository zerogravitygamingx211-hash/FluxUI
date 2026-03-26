import customtkinter as ctk
import tkinter as tk
import threading
import time
import os
import winsound
import cv2
import matplotlib.pyplot as plt
import shutil
import subprocess
import sys
import traceback
import datetime

from components import FLUXWidgetMixin

# =========================================================
# FLUX CORE RUNTIME
# =========================================================


class FLUX(FLUXWidgetMixin):

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("900x600")

        self.widgets = {}
        self.vars = {}
        self.events = {}

    # =========================================================
    # WINDOW CONTROL
    # =========================================================
    def APP(self, title, w, h):
        self.root.title(title)
        self.root.geometry(f"{w}x{h}")

    # =========================================================
    # VARIABLE SYSTEM
    # =========================================================
    def SET(self, name, value):
        self.vars[name] = value

    def GET(self, name):
        return self.vars.get(name)

    def SET_VAR(self, key, value):
        self.vars[key] = value

    def GET_VAR(self, key):
        return self.vars.get(key)

    # =========================================================
    # EVENT SYSTEM
    # =========================================================
    def ON(self, event_name, widget_name, func):
        self.events[(event_name, widget_name)] = func

    def TRIGGER(self, event_name, widget_name):
        key = (event_name, widget_name)
        if key in self.events:
            self.events[key]()

    # =========================================================
    # ACTION SYSTEM
    # =========================================================
    def DO(self, *actions):
        for action in actions:
            try:
                action()
            except Exception as e:
                print("[ACTION ERROR]", e)

    # =========================================================
    # AUDIO ENGINE
    # =========================================================
    def AUDIO(self, file, loop=False):
        if not os.path.exists(file):
            print("[AUDIO ERROR] Missing:", file)
            return

        def run():
            flag = winsound.SND_FILENAME | winsound.SND_ASYNC
            if loop:
                flag |= winsound.SND_LOOP
            winsound.PlaySound(file, flag)

        threading.Thread(target=run, daemon=True).start()

    def AUDIO_STOP(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    # =========================================================
    # VIDEO ENGINE
    # =========================================================
    def VIDEO(self, file, window_name="FLUX VIDEO"):
        if not os.path.exists(file):
            print("[VIDEO ERROR] Missing:", file)
            return

        def play():
            cap = cv2.VideoCapture(file)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow(window_name, frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

        threading.Thread(target=play, daemon=True).start()

    # =========================================================
    # GRAPH ENGINE
    # =========================================================
    def GRAPH(self, x, y, title="FLUX GRAPH"):
        def plot():
            plt.title(title)
            plt.plot(x, y)
            plt.show()

        threading.Thread(target=plot, daemon=True).start()

    # =========================================================
    # TIMING
    # =========================================================
    def WAIT(self, seconds):
        time.sleep(seconds)

    def LOOP(self, func, delay=0.016):
        def run():
            while True:
                try:
                    func()
                except Exception as e:
                    print("[LOOP ERROR]", e)
                time.sleep(delay)

        threading.Thread(target=run, daemon=True).start()

    def AFTER(self, seconds, func):
        def run():
            time.sleep(seconds)
            func()

        threading.Thread(target=run, daemon=True).start()

    # =========================================================
    # ONCLICK EVENT BINDING
    # =========================================================
    def ONCLICK(self, widget_name, *actions):
        widget = self.widgets.get(widget_name)
        if not widget:
            return

        def handler():
            for action in actions:
                try:
                    action()
                except Exception as e:
                    print("[ONCLICK ERROR]", e)

        try:
            widget.configure(command=handler)
        except:
            widget.bind("<Button-1>", lambda e: handler())

    # =========================================================
    # INLINE ACTION BUILDERS
    # =========================================================
    def AUDIO_ACTION(self, file, loop=False):
        return lambda: self.AUDIO(file, loop)

    def GRAPH_ACTION(self, x, y, title="Graph"):
        return lambda: self.GRAPH(x, y, title)

    def SET_ACTION(self, key, value):
        return lambda: self.SET_VAR(key, value)

    def PRINT_ACTION(self, value):
        return lambda: print(value)

    # =========================================================
    # RUN LOOP
    # =========================================================
    def RUN(self):
        self.root.mainloop()


# =========================================================
# FLUX DEBUGGER
# =========================================================

class FLUXDebugger:

    def __init__(self, engine):
        self.engine = engine
        self.breakpoints = set()
        self.logs = []
        self.step_mode = False
        self.paused = False
        self.current_line = 0
        self.variables_snapshot = {}

    def log(self, msg):
        self.logs.append(msg)
        print("[FLUX LOG]", msg)

    def error(self, err):
        trace = traceback.format_exc()
        full = f"[FLUX ERROR] {err}\n{trace}"
        self.logs.append(full)
        print(full)

    def snapshot_vars(self):
        try:
            self.variables_snapshot = dict(self.engine.vars)
        except:
            self.variables_snapshot = {}

    def enable_step_mode(self):
        self.step_mode = True
        self.log("Step mode enabled")

    def disable_step_mode(self):
        self.step_mode = False
        self.log("Step mode disabled")

    def pause(self):
        self.paused = True
        self.log("Execution paused")

    def resume(self):
        self.paused = False
        self.log("Execution resumed")

    def add_breakpoint(self, line):
        self.breakpoints.add(line)
        self.log(f"Breakpoint added at line {line}")

    def remove_breakpoint(self, line):
        self.breakpoints.discard(line)
        self.log(f"Breakpoint removed at line {line}")

    def check(self, line):
        self.current_line = line
        if line in self.breakpoints:
            self.log(f"Hit breakpoint at line {line}")
            self.pause()
        while self.paused:
            time.sleep(0.1)
        if self.step_mode:
            self.pause()

    def step(self):
        self.paused = False
        self.log("Step executed")

    def watch_file(self, file, compiler):
        last_mod = 0

        def watcher():
            nonlocal last_mod
            while True:
                try:
                    mod = os.path.getmtime(file)
                    if mod != last_mod:
                        last_mod = mod
                        self.log("File changed — recompiling...")
                        compiler.run(file)
                    time.sleep(1)
                except Exception as e:
                    self.error(e)

        threading.Thread(target=watcher, daemon=True).start()

    def launch_ide(self):
        ide = ctk.CTkToplevel(self.engine.root)
        ide.title("FLUX IDE DEBUGGER")
        ide.geometry("500x400")

        log_box = ctk.CTkTextbox(ide, width=480, height=300)
        log_box.pack()

        def refresh():
            log_box.delete("0.0", "end")
            for l in self.logs[-50:]:
                log_box.insert("end", str(l) + "\n")
            ide.after(1000, refresh)

        refresh()

    def safe_run(self, func, line=0):
        try:
            self.check(line)
            self.snapshot_vars()
            func()
        except Exception as e:
            self.error(e)


# =========================================================
# FLUX BUILD SYSTEM
# =========================================================

class FLUXBuilder:

    def __init__(self):
        self.project_name = "FLUX_APP"
        self.entry_file = "main.py"
        self.output_dir = "dist"
        self.build_dir = "build"
        self.icon = None
        self.files = []

    def SET_PROJECT(self, name):
        self.project_name = name

    def SET_ENTRY(self, file):
        self.entry_file = file

    def SET_ICON(self, icon_path):
        self.icon = icon_path

    def ADD_FILE(self, file):
        if os.path.exists(file):
            self.files.append(file)
        else:
            print("[BUILDER ERROR] Missing file:", file)

    def COPY_FILES(self):
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)
        for f in self.files:
            shutil.copy(f, self.build_dir)
        shutil.copy(self.entry_file, self.build_dir)

    def BUILD_EXE(self):
        self.COPY_FILES()
        cmd = [
            "pyinstaller",
            "--noconfirm",
            "--onefile",
            "--windowed",
            os.path.join(self.build_dir, self.entry_file)
        ]
        if self.icon:
            cmd.insert(3, f"--icon={self.icon}")
        print("[BUILDER] Running:", " ".join(cmd))
        subprocess.run(cmd)

    def CLEAN(self):
        for folder in [self.build_dir, self.output_dir]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        print("[BUILDER] Cleaned build directories")

    def LAUNCH_INSTALLER(self):
        app = ctk.CTk()
        app.title("FLUX Installer Wizard")
        app.geometry("500x300")

        label = ctk.CTkLabel(app, text="Install FLUX Application", font=("Arial", 20))
        label.pack(pady=20)

        status = ctk.CTkLabel(app, text="Ready to install...")
        status.pack(pady=10)

        def install():
            status.configure(text="Building EXE...")
            try:
                self.BUILD_EXE()
                status.configure(text="Build Complete ✔")
            except Exception as e:
                status.configure(text=f"Error: {e}")

        btn = ctk.CTkButton(app, text="Install / Build", command=install)
        btn.pack(pady=20)
        app.mainloop()

    def RUN_DEV(self):
        print("[FLUX DEV MODE] Running entry file...")
        subprocess.run([sys.executable, self.entry_file])


# =========================================================
# FLUX UTILITY ENGINE
# =========================================================

class FLUXUtilityEngine:

    def __init__(self, engine):
        self.engine = engine
        self.tasks = {}
        self.apps = {}
        self.clipboard = ""
        self.scheduled = []

    def CREATE_NOTE(self, name, text=""):
        self.apps[name] = {
            "type": "note",
            "text": text,
            "created": str(datetime.datetime.now())
        }

    def EDIT_NOTE(self, name, text):
        if name in self.apps:
            self.apps[name]["text"] = text

    def READ_NOTE(self, name):
        return self.apps.get(name, {}).get("text", "")

    def ADD_TASK(self, name, priority=1):
        self.tasks[name] = {
            "done": False,
            "priority": priority,
            "created": str(datetime.datetime.now())
        }

    def COMPLETE_TASK(self, name):
        if name in self.tasks:
            self.tasks[name]["done"] = True

    def LIST_TASKS(self):
        return self.tasks

    def SET_TIMER(self, seconds, callback):
        def run():
            time.sleep(seconds)
            callback()

        threading.Thread(target=run, daemon=True).start()

    def SCHEDULE(self, hour, minute, callback):
        def run():
            while True:
                now = datetime.datetime.now()
                if now.hour == hour and now.minute == minute:
                    callback()
                    time.sleep(60)
                time.sleep(1)

        threading.Thread(target=run, daemon=True).start()

    def WRITE_FILE(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def READ_FILE(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def ORGANIZE_FOLDER(self, path):
        if not os.path.exists(path):
            print("[ERROR] Folder not found")
            return
        for file in os.listdir(path):
            ext = file.split(".")[-1]
            folder = os.path.join(path, ext)
            if not os.path.exists(folder):
                os.makedirs(folder)
            try:
                os.rename(os.path.join(path, file), os.path.join(folder, file))
            except:
                pass

    def COPY(self, text):
        self.clipboard = text

    def PASTE(self):
        return self.clipboard

    def RUN_APP(self, name, func):
        self.apps[name] = {"type": "app", "run": func}

    def START_APP(self, name):
        app = self.apps.get(name)
        if app and app["type"] == "app":
            app["run"]()

    def SERVICE(self, name, func, interval=5):
        def loop():
            while True:
                func()
                time.sleep(interval)

        threading.Thread(target=loop, daemon=True).start()


# =========================================================
# FLUX UNIFIED RUNTIME CORE
# =========================================================

class FLUXRuntime:

    def __init__(self, ui_engine, graph_engine, utility_engine, vault, saveas_engine, game_engine=None):
        self.ui = ui_engine
        self.graph = graph_engine
        self.utility = utility_engine
        self.vault = vault
        self.saveas = saveas_engine
        self.game = game_engine

        self.memory = {}
        self.last_result = None

    def EXEC(self, command, *args, **kwargs):
        cmd = command.upper()

        # UI
        if cmd == "WINDOW":
            self.ui.WINDOW(*args)
        elif cmd == "LABEL":
            self.ui.LABEL(*args)
        elif cmd == "BUTTON":
            self.ui.BUTTON(*args)
        elif cmd == "INPUT":
            self.ui.INPUT(*args)
        elif cmd == "TEXTBOX":
            self.ui.TEXTBOX(*args)
        elif cmd == "SWITCH":
            self.ui.SWITCH(*args)
        elif cmd == "SLIDER":
            self.ui.SLIDER(*args)
        elif cmd == "DROPDOWN":
            self.ui.DROPDOWN(*args)
        elif cmd == "ALERT":
            self.ui.ALERT(*args)
        elif cmd == "ERROR":
            self.ui.ERROR(*args)
        elif cmd == "CONFIRM":
            self.last_result = self.ui.CONFIRM(*args)

        # Graph
        elif cmd == "LINE_PLOT":
            self.last_result = self.graph.LINE_PLOT(*args)
        elif cmd == "BAR_CHART":
            self.last_result = self.graph.BAR_CHART(*args)
        elif cmd == "PIE_CHART":
            self.last_result = self.graph.PIE_CHART(*args)
        elif cmd == "SCATTER":
            self.last_result = self.graph.SCATTER(*args)
        elif cmd == "HISTOGRAM":
            self.last_result = self.graph.HISTOGRAM(*args)
        elif cmd == "SAVE_GRAPH":
            self.last_result = self.vault.SAVE_GRAPH(*args)

        # Save / Export
        elif cmd == "SAVE_AS":
            self.last_result = self.saveas.SAVE_AS(*args)
        elif cmd == "SAVE_AS_IMAGE":
            self.last_result = self.saveas.SAVE_AS_IMAGE(*args)
        elif cmd == "SAVE_AS_DATA":
            self.last_result = self.saveas.SAVE_AS_DATA(*args)

        # Vault
        elif cmd == "SAVE":
            self.vault.SAVE(*args)
        elif cmd == "GET":
            self.last_result = self.vault.GET(*args)
        elif cmd == "GET_DATA":
            self.last_result = self.vault.GET_DATA(*args)
        elif cmd == "LIST":
            self.last_result = self.vault.LIST()

        # Utility
        elif cmd == "NOTE":
            self.utility.CREATE_NOTE(*args)
        elif cmd == "TASK":
            self.utility.ADD_TASK(*args)
        elif cmd == "TIMER":
            self.utility.SET_TIMER(*args)
        elif cmd == "SCHEDULE":
            self.utility.SCHEDULE(*args)
        elif cmd == "WRITE_FILE":
            self.utility.WRITE_FILE(*args)
        elif cmd == "READ_FILE":
            self.last_result = self.utility.READ_FILE(*args)
        elif cmd == "COPY":
            self.utility.COPY(*args)
        elif cmd == "PASTE":
            self.last_result = self.utility.PASTE()

        # Game engine
        elif cmd == "CREATE_OBJECT":
            self.game.CREATE_OBJECT(*args)
        elif cmd == "FORCE":
            self.game.APPLY_FORCE(*args)
        elif cmd == "START_GAME":
            self.game.START_LOOP()
        elif cmd == "STOP_GAME":
            self.game.STOP_LOOP()

        else:
            print(f"[FLUX ERROR] Unknown command: {command}")

    def RESULT(self):
        return self.last_result

    def SET(self, key, value):
        self.memory[key] = value

    def GET_VAR(self, key):
        return self.memory.get(key, None)

    def RUN_SCRIPT(self, script_list):
        for line in script_list:
            if isinstance(line, dict):
                self.EXEC(line["cmd"], *line.get("args", []))
