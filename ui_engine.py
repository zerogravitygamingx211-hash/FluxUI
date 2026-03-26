import customtkinter as ctk
import tkinter as tk

# =========================================================
# FLUX CORE RUNTIME
# =========================================================

class FLUX:

    def __init__(self):

        # init UI system
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("900x600")

        # registries
        self.widgets = {}      # UI objects
        self.vars = {}         # variables
        self.events = {}       # event bindings

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

    # =========================================================
    # EVENT BASE SYSTEM (CORE ONLY)
    # =========================================================

    def ON(self, event_name, widget_name, func):
        """
        Manual event binding registry.
        No abstraction, just direct mapping.
        """
        self.events[(event_name, widget_name)] = func

    def TRIGGER(self, event_name, widget_name):
        key = (event_name, widget_name)

        if key in self.events:
            self.events[key]()

    # =========================================================
    # BASE RUN LOOP
    # =========================================================

    def RUN(self):
        self.root.mainloop()
import customtkinter as ctk
import tkinter as tk

# =========================================================
# FLUX UI LAYER (DIRECT MANUAL BINDINGS)
# =========================================================

class FLUX:

    # =========================================================
    # WINDOW (already exists in Part 1, kept for completeness)
    # =========================================================
    def APP(self, title, w, h):
        self.root.title(title)
        self.root.geometry(f"{w}x{h}")

    # =========================================================
    # INTERNAL WIDGET REGISTRY HELPER
    # =========================================================
    def _register(self, name, widget):
        self.widgets[name] = widget
        return widget

    # =========================================================
    # CTK LABEL
    # =========================================================
    def CTK_CTkLabel(self, name, **kwargs):
        widget = ctk.CTkLabel(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK BUTTON
    # =========================================================
    def CTK_CTkButton(self, name, **kwargs):
        widget = ctk.CTkButton(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK ENTRY
    # =========================================================
    def CTK_CTkEntry(self, name, **kwargs):
        widget = ctk.CTkEntry(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK FRAME
    # =========================================================
    def CTK_CTkFrame(self, name, **kwargs):
        widget = ctk.CTkFrame(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK TEXTBOX
    # =========================================================
    def CTK_CTkTextbox(self, name, **kwargs):
        widget = ctk.CTkTextbox(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK SWITCH
    # =========================================================
    def CTK_CTkSwitch(self, name, **kwargs):
        widget = ctk.CTkSwitch(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK SLIDER
    # =========================================================
    def CTK_CTkSlider(self, name, **kwargs):
        widget = ctk.CTkSlider(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK PROGRESS BAR
    # =========================================================
    def CTK_CTkProgressBar(self, name, **kwargs):
        widget = ctk.CTkProgressBar(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK OPTION MENU
    # =========================================================
    def CTK_CTkOptionMenu(self, name, **kwargs):
        widget = ctk.CTkOptionMenu(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK COMBO BOX
    # =========================================================
    def CTK_CTkComboBox(self, name, **kwargs):
        widget = ctk.CTkComboBox(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK TAB VIEW
    # =========================================================
    def CTK_CTkTabview(self, name, **kwargs):
        widget = ctk.CTkTabview(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # CTK SCROLLABLE FRAME
    # =========================================================
    def CTK_CTkScrollableFrame(self, name, **kwargs):
        widget = ctk.CTkScrollableFrame(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # TK INTER RAW BINDINGS (NO CTK WRAPPING)
    # =========================================================

    def TK_Label(self, name, **kwargs):
        widget = tk.Label(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def TK_Button(self, name, **kwargs):
        widget = tk.Button(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def TK_Entry(self, name, **kwargs):
        widget = tk.Entry(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def TK_Canvas(self, name, **kwargs):
        widget = tk.Canvas(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # WIDGET ACCESS SYSTEM
    # =========================================================

    def GET_WIDGET(self, name):
        return self.widgets.get(name)

    def SET_TEXT(self, name, text):
        w = self.widgets.get(name)
        if w:
            try:
                w.configure(text=text)
            except:
                pass

    # =========================================================
    # CLICK BINDING (DIRECT EVENT HOOK)
    # =========================================================

    def BIND_CLICK(self, name, func):
        w = self.widgets.get(name)
        if not w:
            return

        try:
            w.configure(command=func)
        except:
            try:
                w.bind("<Button-1>", lambda e: func())
            except:
                pass
import threading
import time
import os
import winsound
import cv2
import matplotlib.pyplot as plt

# =========================================================
# FLUX MULTIMEDIA + ACTION ENGINE
# =========================================================

class FLUX:

    # =========================================================
    # ACTION SYSTEM CORE
    # =========================================================
    def DO(self, *actions):
        """
        Executes chained actions:
        DO(AUDIO("a.wav"), GRAPH(...), SET(...))
        """
        for action in actions:
            try:
                action()
            except Exception as e:
                print("[ACTION ERROR]", e)

    # =========================================================
    # VARIABLE ACTION HELPERS
    # =========================================================
    def SET_VAR(self, key, value):
        self.vars[key] = value

    def GET_VAR(self, key):
        return self.vars.get(key)

    # =========================================================
    # AUDIO ENGINE (NATIVE WIN SOUND)
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
    # VIDEO ENGINE (OPEN CV STREAM)
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
    # MATPLOTLIB GRAPH ENGINE
    # =========================================================
    def GRAPH(self, x, y, title="FLUX GRAPH"):
        def plot():
            plt.title(title)
            plt.plot(x, y)
            plt.show()

        threading.Thread(target=plot, daemon=True).start()

    # =========================================================
    # DELAY ACTION
    # =========================================================
    def WAIT(self, seconds):
        time.sleep(seconds)

    # =========================================================
    # EVENT ACTION BINDING SYSTEM
    # =========================================================
    def ONCLICK(self, widget_name, *actions):
        """
        Example:
        ONCLICK("btn1", AUDIO("a.wav"), GRAPH(...))
        """

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
    # INLINE ACTION BUILDERS (FLUX STYLE FUNCTIONS)
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
    # ANIMATION LOOP ENGINE
    # =========================================================
    def LOOP(self, func, delay=0.016):
        def run():
            while True:
                try:
                    func()
                except Exception as e:
                    print("[LOOP ERROR]", e)
                time.sleep(delay)

        threading.Thread(target=run, daemon=True).start()

    # =========================================================
    # SIMPLE TIMER ACTION
    # =========================================================
    def AFTER(self, seconds, func):
        def run():
            time.sleep(seconds)
            func()

        threading.Thread(target=run, daemon=True).start()
import re

# =========================================================
# FLUX LANGUAGE PARSER + COMPILER
# =========================================================

class FLUXParser:

    def __init__(self, engine):
        self.engine = engine
        self.tokens = []
        self.ast = []

    # =========================================================
    # LOAD FILE
    # =========================================================
    def load(self, file):
        with open(file, "r", encoding="utf-8") as f:
            return f.readlines()

    # =========================================================
    # TOKENIZER (VERY SIMPLE LINE-BASED DSL)
    # =========================================================
    def tokenize(self, lines):
        tokens = []

        for line in lines:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            tokens.append(line)

        self.tokens = tokens
        return tokens

    # =========================================================
    # PARSER → AST
    # =========================================================
    def parse(self, tokens):
        ast = []
        i = 0

        while i < len(tokens):
            line = tokens[i]

            # APP
            if line.startswith("APP"):
                m = re.findall(r'APP\s+"(.+)"\s+SIZE\s+(\d+)\s+(\d+)', line)
                if m:
                    name, w, h = m[0]
                    ast.append(("APP", name, int(w), int(h)))

            # BUTTON
            elif line.startswith("BUTTON"):
                m = re.findall(r'BUTTON\s+(\w+)\s+"(.+)"\s+(\d+)\s+(\d+)', line)
                if m:
                    name, text, x, y = m[0]
                    ast.append(("BUTTON", name, text, int(x), int(y)))

            # TEXT
            elif line.startswith("TEXT"):
                m = re.findall(r'TEXT\s+"(.+)"\s+(\d+)\s+(\d+)', line)
                if m:
                    text, x, y = m[0]
                    ast.append(("TEXT", text, int(x), int(y)))

            # INPUT
            elif line.startswith("INPUT"):
                m = re.findall(r'INPUT\s+(\w+)\s+(\d+)\s+(\d+)', line)
                if m:
                    name, x, y = m[0]
                    ast.append(("INPUT", name, int(x), int(y)))

            # STYLE (ignored for now but stored)
            elif line.startswith("STYLE"):
                ast.append(("STYLE_RAW", line))

            # ONCLICK
            elif line.startswith("ONCLICK"):
                ast.append(("ONCLICK_RAW", line))

            # AUDIO EVENT
            elif "AUDIO" in line:
                m = re.findall(r'AUDIO\s+"(.+)"', line)
                if m:
                    ast.append(("AUDIO", m[0]))

            # GRAPH EVENT
            elif "GRAPH" in line:
                ast.append(("GRAPH_RAW", line))

            else:
                print("[WARNING] Unknown line:", line)

            i += 1

        self.ast = ast
        return ast

    # =========================================================
    # EXECUTOR (AST → ENGINE CALLS)
    # =========================================================
    def run(self, ast):

        for node in ast:

            # ---------------- APP ----------------
            if node[0] == "APP":
                _, name, w, h = node
                self.engine.APP(name, w, h)

            # ---------------- BUTTON ----------------
            elif node[0] == "BUTTON":
                _, name, text, x, y = node
                self.engine.CTK_CTkButton(
                    name,
                    text=text,
                    command=lambda: print(f"[{name}] clicked")
                )

            # ---------------- TEXT ----------------
            elif node[0] == "TEXT":
                _, text, x, y = node
                self.engine.CTK_CTkLabel(
                    f"text_{x}_{y}",
                    text=text
                )

            # ---------------- INPUT ----------------
            elif node[0] == "INPUT":
                _, name, x, y = node
                self.engine.CTK_CTkEntry(name)

            # ---------------- AUDIO ----------------
            elif node[0] == "AUDIO":
                _, file = node
                self.engine.AUDIO(file)

            # ---------------- GRAPH (demo only) ----------------
            elif node[0] == "GRAPH_RAW":
                try:
                    x = [1, 2, 3]
                    y = [3, 6, 9]
                    self.engine.GRAPH(x, y)
                except:
                    pass

    # =========================================================
    # FULL PIPELINE
    # =========================================================
    def compile(self, file):
        lines = self.load(file)
        tokens = self.tokenize(lines)
        ast = self.parse(tokens)
        self.run(ast)

# =========================================================
# FLUX EVENT SYSTEM + BLOCK STRUCTURE PARSER
# =========================================================

import re

class FLUXEventCompiler:

    def __init__(self, engine):
        self.engine = engine
        self.events = {}   # widget -> actions
        self.blocks = []
        self.current_block = None

    # =========================================================
    # BLOCK LOADER
    # =========================================================
    def load(self, file):
        with open(file, "r", encoding="utf-8") as f:
            return [line.rstrip() for line in f.readlines()]

    # =========================================================
    # PREPROCESSOR (REMOVES EMPTY LINES)
    # =========================================================
    def preprocess(self, lines):
        return [l for l in lines if l.strip() and not l.strip().startswith("#")]

    # =========================================================
    # BLOCK PARSER (LIKE JS BRACES)
    # =========================================================
    def parse_blocks(self, lines):

        blocks = []
        stack = []

        current = {"type": "ROOT", "body": []}

        for line in lines:
            line = line.strip()

            # OPEN BLOCK
            if line.endswith("{"):
                block_type = line.replace("{", "").strip()
                new_block = {"type": block_type, "body": []}
                stack.append(current)
                current = new_block

            # CLOSE BLOCK
            elif line == "}":
                finished = current
                current = stack.pop()
                current["body"].append(finished)

            else:
                current["body"].append(line)

        blocks.append(current)
        return current

    # =========================================================
    # EVENT PARSER
    # =========================================================
    def parse_events(self, lines):

        for line in lines:

            # ONCLICK btn1 -> AUDIO "click.wav"
            if "ONCLICK" in line:

                m = re.findall(r'ONCLICK\s+(\w+)\s*->\s*(.+)', line)
                if m:
                    widget, action = m[0]

                    if widget not in self.events:
                        self.events[widget] = []

                    self.events[widget].append(action)

            # SIMPLE AUDIO EVENT
            elif "AUDIO" in line and "ONCLICK" not in line:
                m = re.findall(r'AUDIO\s+"(.+)"', line)
                if m:
                    self.events.setdefault("__global__", []).append(("AUDIO", m[0]))

    # =========================================================
    # ACTION EXECUTOR
    # =========================================================
    def execute_action(self, action):

        action = action.strip()

        # AUDIO
        if action.startswith("AUDIO"):
            m = re.findall(r'AUDIO\s+"(.+)"', action)
            if m:
                self.engine.AUDIO(m[0])

        # GRAPH
        elif action.startswith("GRAPH"):
            self.engine.GRAPH([1, 2, 3], [3, 6, 9])

        # PRINT
        elif action.startswith("PRINT"):
            m = re.findall(r'PRINT\s+"(.+)"', action)
            if m:
                print(m[0])

        # SET VAR
        elif action.startswith("SET"):
            m = re.findall(r'SET\s+(\w+)\s+(\w+)', action)
            if m:
                self.engine.SET_VAR(m[0][0], m[0][1])

    # =========================================================
    # BIND EVENTS TO ENGINE
    # =========================================================
    def bind_events(self):

        for widget, actions in self.events.items():

            def handler(actions=actions):
                for a in actions:
                    self.execute_action(a)

            try:
                self.engine.BIND_CLICK(widget, handler)
            except:
                print("[EVENT ERROR] Cannot bind:", widget)

    # =========================================================
    # RUN FULL PIPELINE
    # =========================================================
    def run(self, file):

        lines = self.load(file)
        lines = self.preprocess(lines)

        self.parse_events(lines)
        self.bind_events()
# =========================================================
# FLUX DOM-LIKE UI STRUCTURE ENGINE
# =========================================================

import re

class FLUXDOM:

    def __init__(self, engine):
        self.engine = engine
        self.tree = []
        self.stack = []
        self.errors = []

    # =========================================================
    # LOAD FILE
    # =========================================================
    def load(self, file):
        with open(file, "r", encoding="utf-8") as f:
            return [l.rstrip() for l in f.readlines()]

    # =========================================================
    # BASIC VALIDATOR
    # =========================================================
    def error(self, msg, line):
        self.errors.append(f"[ERROR] {msg} | {line}")
        print(f"[ERROR] {msg} | {line}")

    # =========================================================
    # PARSE DOM TREE (LIKE HTML)
    # =========================================================
    def parse(self, lines):

        root = {"type": "ROOT", "children": []}
        self.stack = [root]

        for line in lines:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            # =================================================
            # OPEN BLOCK { COLUMN / ROW / FRAME }
            # =================================================
            if line.endswith("{"):
                tag = line.replace("{", "").strip()

                node = {
                    "type": tag,
                    "children": []
                }

                self.stack[-1]["children"].append(node)
                self.stack.append(node)

            # =================================================
            # CLOSE BLOCK
            # =================================================
            elif line == "}":
                if len(self.stack) > 1:
                    self.stack.pop()
                else:
                    self.error("Unexpected closing bracket", line)

            # =================================================
            # COMPONENTS
            # =================================================

            # BUTTON btn "text"
            elif line.startswith("BUTTON"):
                m = re.findall(r'BUTTON\s+(\w+)\s+"(.+)"', line)
                if m:
                    name, text = m[0]

                    node = {
                        "type": "BUTTON",
                        "name": name,
                        "text": text
                    }

                    self.stack[-1]["children"].append(node)
                else:
                    self.error("Invalid BUTTON syntax", line)

            # TEXT "hello"
            elif line.startswith("TEXT"):
                m = re.findall(r'TEXT\s+"(.+)"', line)
                if m:
                    node = {
                        "type": "TEXT",
                        "text": m[0]
                    }
                    self.stack[-1]["children"].append(node)
                else:
                    self.error("Invalid TEXT syntax", line)

            # INPUT name
            elif line.startswith("INPUT"):
                m = re.findall(r'INPUT\s+(\w+)', line)
                if m:
                    node = {
                        "type": "INPUT",
                        "name": m[0]
                    }
                    self.stack[-1]["children"].append(node)

            # EVENT
            elif "ONCLICK" in line:
                m = re.findall(r'ONCLICK\s+(\w+)\s*->\s*(.+)', line)
                if m:
                    node = {
                        "type": "EVENT",
                        "target": m[0][0],
                        "action": m[0][1]
                    }
                    self.stack[-1]["children"].append(node)

            else:
                self.error("Unknown syntax", line)

        return root

    # =========================================================
    # RENDER TREE → ENGINE UI
    # =========================================================
    def render_node(self, node):

        t = node["type"]

        # ROOT
        if t == "ROOT":
            for c in node["children"]:
                self.render_node(c)

        # COLUMN / ROW (LAYOUT ONLY)
        elif t in ["COLUMN", "ROW", "FRAME"]:
            for c in node["children"]:
                self.render_node(c)

        # BUTTON
        elif t == "BUTTON":
            widget = self.engine.CTK_CTkButton(
                node["name"],
                text=node["text"]
            )

            # attach events if any
            for c in node.get("children", []):
                if c["type"] == "EVENT":
                    self.engine.BIND_CLICK(node["name"], lambda a=c["action"]: self.execute(a))

        # TEXT
        elif t == "TEXT":
            self.engine.CTK_CTkLabel(
                f"text_{node['text'][:5]}",
                text=node["text"]
            )

        # INPUT
        elif t == "INPUT":
            self.engine.CTK_CTkEntry(node["name"])

        # EVENT ONLY NODE
        elif t == "EVENT":
            self.engine.ONCLICK(
                node["target"],
                self.wrap_action(node["action"])
            )

    # =========================================================
    # ACTION WRAPPER
    # =========================================================
    def wrap_action(self, action):

        def run():

            if action.startswith("AUDIO"):
                m = re.findall(r'AUDIO\s+"(.+)"', action)
                if m:
                    self.engine.AUDIO(m[0])

            elif action.startswith("GRAPH"):
                self.engine.GRAPH([1,2,3],[3,6,9])

            elif action.startswith("PRINT"):
                m = re.findall(r'PRINT\s+"(.+)"', action)
                if m:
                    print(m[0])

            elif action.startswith("SET"):
                m = re.findall(r'SET\s+(\w+)\s+(.+)', action)
                if m:
                    self.engine.SET_VAR(m[0][0], m[0][1])

        return run

    # =========================================================
    # RUN FULL PIPELINE
    # =========================================================
    def run(self, file):

        lines = self.load(file)
        tree = self.parse(lines)

        self.render_node(tree)

        if self.errors:
            print("\n[FLUX WARNINGS]")
            for e in self.errors:
                print(e)
# =========================================================
# FLUX DEBUGGER + RUNTIME CONTROL CENTER
# =========================================================

import time
import traceback
import threading

class FLUXDebugger:

    def __init__(self, engine):
        self.engine = engine

        self.breakpoints = set()
        self.logs = []
        self.step_mode = False
        self.paused = False
        self.current_line = 0

        self.variables_snapshot = {}

    # =========================================================
    # LOG SYSTEM
    # =========================================================
    def log(self, msg):
        self.logs.append(msg)
        print("[FLUX LOG]", msg)

    # =========================================================
    # ERROR HANDLER (STACK TRACE STYLE)
    # =========================================================
    def error(self, err):
        trace = traceback.format_exc()
        full = f"[FLUX ERROR] {err}\n{trace}"
        self.logs.append(full)
        print(full)

    # =========================================================
    # VARIABLE INSPECTOR
    # =========================================================
    def snapshot_vars(self):
        try:
            self.variables_snapshot = dict(self.engine.vars)
        except:
            self.variables_snapshot = {}

    # =========================================================
    # STEP EXECUTION CONTROL
    # =========================================================
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

    # =========================================================
    # BREAKPOINT SYSTEM
    # =========================================================
    def add_breakpoint(self, line):
        self.breakpoints.add(line)
        self.log(f"Breakpoint added at line {line}")

    def remove_breakpoint(self, line):
        self.breakpoints.discard(line)
        self.log(f"Breakpoint removed at line {line}")

    # =========================================================
    # CHECK EXECUTION STATE
    # =========================================================
    def check(self, line):
        self.current_line = line

        if line in self.breakpoints:
            self.log(f"Hit breakpoint at line {line}")
            self.pause()

        while self.paused:
            time.sleep(0.1)

        if self.step_mode:
            self.pause()

    # =========================================================
    # STEP FORWARD
    # =========================================================
    def step(self):
        self.paused = False
        self.log("Step executed")

    # =========================================================
    # LIVE RELOAD SIMULATOR
    # =========================================================
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

    # =========================================================
    # MINI IDE WINDOW (INSIDE CTK)
    # =========================================================
    def launch_ide(self):

        import customtkinter as ctk

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

    # =========================================================
    # EXECUTION WRAPPER (SAFE RUN)
    # =========================================================
    def safe_run(self, func, line=0):
        try:
            self.check(line)
            self.snapshot_vars()
            func()
        except Exception as e:
            self.error(e)
# =========================================================
# FLUX BUILD SYSTEM (EXE + INSTALLER WIZARD)
# =========================================================

import os
import shutil
import subprocess
import sys

class FLUXBuilder:

    def __init__(self):
        self.project_name = "FLUX_APP"
        self.entry_file = "main.py"
        self.output_dir = "dist"
        self.build_dir = "build"
        self.icon = None
        self.files = []

    # =========================================================
    # SET PROJECT INFO
    # =========================================================
    def SET_PROJECT(self, name):
        self.project_name = name

    def SET_ENTRY(self, file):
        self.entry_file = file

    def SET_ICON(self, icon_path):
        self.icon = icon_path

    # =========================================================
    # ADD FILES TO PACKAGE
    # =========================================================
    def ADD_FILE(self, file):
        if os.path.exists(file):
            self.files.append(file)
        else:
            print("[BUILDER ERROR] Missing file:", file)

    # =========================================================
    # COPY PROJECT FILES
    # =========================================================
    def COPY_FILES(self):
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)

        for f in self.files:
            shutil.copy(f, self.build_dir)

        shutil.copy(self.entry_file, self.build_dir)

    # =========================================================
    # PYINSTALLER BUILD PROCESS
    # =========================================================
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

    # =========================================================
    # CLEAN BUILD FILES
    # =========================================================
    def CLEAN(self):
        for folder in [self.build_dir, self.output_dir]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        print("[BUILDER] Cleaned build directories")

    # =========================================================
    # SIMPLE INSTALLER WIZARD (CTK)
    # =========================================================
    def LAUNCH_INSTALLER(self):

        import customtkinter as ctk

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

    # =========================================================
    # QUICK RUN MODE (DEV TEST)
    # =========================================================
    def RUN_DEV(self):
        print("[FLUX DEV MODE] Running entry file...")
        subprocess.run([sys.executable, self.entry_file])
# =========================================================
# FLUX IDE + VISUAL BUILDER CORE
# =========================================================

import customtkinter as ctk
import threading
import time

class FLUXIDE:

    def __init__(self, engine, compiler, debugger, builder):
        self.engine = engine
        self.compiler = compiler
        self.debugger = debugger
        self.builder = builder

        self.file_path = None
        self.running = False

    # =========================================================
    # LAUNCH FULL IDE
    # =========================================================
    def LAUNCH(self):

        self.app = ctk.CTk()
        self.app.title("FLUX IDE PRO")
        self.app.geometry("1000x600")

        # =====================================================
        # LEFT PANEL (FILE / CONTROLS)
        # =====================================================
        self.left = ctk.CTkFrame(self.app, width=200)
        self.left.pack(side="left", fill="y")

        ctk.CTkLabel(self.left, text="FLUX IDE", font=("Arial", 20)).pack(pady=10)

        self.run_btn = ctk.CTkButton(
            self.left,
            text="RUN",
            command=self.RUN_FILE
        )
        self.run_btn.pack(pady=5)

        self.build_btn = ctk.CTkButton(
            self.left,
            text="BUILD EXE",
            command=self.BUILD
        )
        self.build_btn.pack(pady=5)

        self.debug_btn = ctk.CTkButton(
            self.left,
            text="DEBUG MODE",
            command=self.DEBUG
        )
        self.debug_btn.pack(pady=5)

        self.live_btn = ctk.CTkButton(
            self.left,
            text="LIVE RELOAD",
            command=self.LIVE
        )
        self.live_btn.pack(pady=5)

        # =====================================================
        # CENTER PANEL (EDITOR)
        # =====================================================
        self.editor = ctk.CTkTextbox(self.app, width=600)
        self.editor.pack(side="left", fill="both", expand=True)

        # =====================================================
        # RIGHT PANEL (OUTPUT / DEBUG LOGS)
        # =====================================================
        self.right = ctk.CTkFrame(self.app, width=200)
        self.right.pack(side="right", fill="y")

        ctk.CTkLabel(self.right, text="OUTPUT").pack()

        self.output = ctk.CTkTextbox(self.right, height=300)
        self.output.pack(fill="both", expand=True)

        self.app.mainloop()

    # =========================================================
    # RUN CURRENT FILE
    # =========================================================
    def RUN_FILE(self):

        code = self.editor.get("0.0", "end")

        file = "temp.flux"
        with open(file, "w", encoding="utf-8") as f:
            f.write(code)

        self.output.insert("end", "\n[RUNNING FLUX]\n")

        try:
            self.compiler.run(file)
            self.output.insert("end", "[SUCCESS]\n")
        except Exception as e:
            self.output.insert("end", f"[ERROR] {e}\n")

    # =========================================================
    # DEBUG MODE
    # =========================================================
    def DEBUG(self):

        self.output.insert("end", "\n[DEBUG MODE ENABLED]\n")

        self.debugger.launch_ide()

    # =========================================================
    # BUILD EXE
    # =========================================================
    def BUILD(self):

        self.output.insert("end", "\n[BUILDING EXE]\n")

        try:
            self.builder.BUILD_EXE()
            self.output.insert("end", "[BUILD COMPLETE]\n")
        except Exception as e:
            self.output.insert("end", f"[BUILD ERROR] {e}\n")

    # =========================================================
    # LIVE RELOAD MODE
    # =========================================================
    def LIVE(self):

        self.output.insert("end", "\n[LIVE RELOAD STARTED]\n")

        def watcher():
            last = ""

            while True:
                try:
                    code = self.editor.get("0.0", "end")

                    if code != last:
                        last = code

                        file = "live.flux"
                        with open(file, "w", encoding="utf-8") as f:
                            f.write(code)

                        self.compiler.run(file)

                    time.sleep(1)

                except Exception as e:
                    self.output.insert("end", f"[LIVE ERROR] {e}\n")

        threading.Thread(target=watcher, daemon=True).start()
# =========================================================
# FLUX NODE-BASED VISUAL PROGRAMMING ENGINE
# =========================================================

import customtkinter as ctk

class FLUXNode:

    def __init__(self, id, node_type, data=None):
        self.id = id
        self.type = node_type
        self.data = data or {}
        self.outputs = []
        self.inputs = []

    def connect(self, other):
        self.outputs.append(other)
        other.inputs.append(self)


class FLUXNodeEngine:

    def __init__(self, engine):
        self.engine = engine
        self.nodes = {}
        self.execution_order = []

    # =========================================================
    # CREATE NODE
    # =========================================================
    def CREATE_NODE(self, node_id, node_type, **data):
        node = FLUXNode(node_id, node_type, data)
        self.nodes[node_id] = node
        return node

    # =========================================================
    # CONNECT NODES
    # =========================================================
    def CONNECT(self, from_id, to_id):
        if from_id in self.nodes and to_id in self.nodes:
            self.nodes[from_id].connect(self.nodes[to_id])

    # =========================================================
    # BUILD EXECUTION GRAPH (TOPO SORT SIMPLE)
    # =========================================================
    def BUILD_GRAPH(self):

        visited = set()
        order = []

        def visit(node):
            if node.id in visited:
                return
            visited.add(node.id)

            for out in node.outputs:
                visit(out)

            order.append(node)

        for node in self.nodes.values():
            visit(node)

        self.execution_order = list(reversed(order))

    # =========================================================
    # EXECUTE GRAPH
    # =========================================================
    def EXECUTE(self):

        for node in self.execution_order:

            t = node.type
            d = node.data

            # -------------------------------------------------
            if t == "AUDIO":
                self.engine.AUDIO(d.get("file", ""))

            elif t == "PRINT":
                print(d.get("text", ""))

            elif t == "GRAPH":
                self.engine.GRAPH([1,2,3], [3,6,9])

            elif t == "SET":
                self.engine.SET_VAR(d.get("key"), d.get("value"))

            elif t == "WAIT":
                import time
                time.sleep(d.get("seconds", 1))

    # =========================================================
    # VISUAL NODE EDITOR (BASIC UI BUILDER)
    # =========================================================
    def LAUNCH_EDITOR(self):

        app = ctk.CTk()
        app.title("FLUX NODE EDITOR")
        app.geometry("900x600")

        left = ctk.CTkFrame(app, width=200)
        left.pack(side="left", fill="y")

        canvas = ctk.CTkFrame(app)
        canvas.pack(side="right", fill="both", expand=True)

        # -------------------------------------------------
        # NODE CREATION BUTTONS
        # -------------------------------------------------

        def add_audio():
            node = self.CREATE_NODE(
                f"audio_{len(self.nodes)}",
                "AUDIO",
                file="click.wav"
            )
            print("Created:", node.id)

        def add_print():
            node = self.CREATE_NODE(
                f"print_{len(self.nodes)}",
                "PRINT",
                text="Hello FLUX"
            )
            print("Created:", node.id)

        def run_graph():
            self.BUILD_GRAPH()
            self.EXECUTE()

        ctk.CTkLabel(left, text="NODE TOOLBOX").pack(pady=10)

        ctk.CTkButton(left, text="AUDIO NODE", command=add_audio).pack(pady=5)
        ctk.CTkButton(left, text="PRINT NODE", command=add_print).pack(pady=5)
        ctk.CTkButton(left, text="RUN GRAPH", command=run_graph).pack(pady=20)

        app.mainloop()
# =========================================================
# FLUX NODE-BASED VISUAL PROGRAMMING ENGINE
# =========================================================

import customtkinter as ctk

class FLUXNode:

    def __init__(self, id, node_type, data=None):
        self.id = id
        self.type = node_type
        self.data = data or {}
        self.outputs = []
        self.inputs = []

    def connect(self, other):
        self.outputs.append(other)
        other.inputs.append(self)


class FLUXNodeEngine:

    def __init__(self, engine):
        self.engine = engine
        self.nodes = {}
        self.execution_order = []

    # =========================================================
    # CREATE NODE
    # =========================================================
    def CREATE_NODE(self, node_id, node_type, **data):
        node = FLUXNode(node_id, node_type, data)
        self.nodes[node_id] = node
        return node

    # =========================================================
    # CONNECT NODES
    # =========================================================
    def CONNECT(self, from_id, to_id):
        if from_id in self.nodes and to_id in self.nodes:
            self.nodes[from_id].connect(self.nodes[to_id])

    # =========================================================
    # BUILD EXECUTION GRAPH (TOPO SORT SIMPLE)
    # =========================================================
    def BUILD_GRAPH(self):

        visited = set()
        order = []

        def visit(node):
            if node.id in visited:
                return
            visited.add(node.id)

            for out in node.outputs:
                visit(out)

            order.append(node)

        for node in self.nodes.values():
            visit(node)

        self.execution_order = list(reversed(order))

    # =========================================================
    # EXECUTE GRAPH
    # =========================================================
    def EXECUTE(self):

        for node in self.execution_order:

            t = node.type
            d = node.data

            # -------------------------------------------------
            if t == "AUDIO":
                self.engine.AUDIO(d.get("file", ""))

            elif t == "PRINT":
                print(d.get("text", ""))

            elif t == "GRAPH":
                self.engine.GRAPH([1,2,3], [3,6,9])

            elif t == "SET":
                self.engine.SET_VAR(d.get("key"), d.get("value"))

            elif t == "WAIT":
                import time
                time.sleep(d.get("seconds", 1))

    # =========================================================
    # VISUAL NODE EDITOR (BASIC UI BUILDER)
    # =========================================================
    def LAUNCH_EDITOR(self):

        app = ctk.CTk()
        app.title("FLUX NODE EDITOR")
        app.geometry("900x600")

        left = ctk.CTkFrame(app, width=200)
        left.pack(side="left", fill="y")

        canvas = ctk.CTkFrame(app)
        canvas.pack(side="right", fill="both", expand=True)

        # -------------------------------------------------
        # NODE CREATION BUTTONS
        # -------------------------------------------------

        def add_audio():
            node = self.CREATE_NODE(
                f"audio_{len(self.nodes)}",
                "AUDIO",
                file="click.wav"
            )
            print("Created:", node.id)

        def add_print():
            node = self.CREATE_NODE(
                f"print_{len(self.nodes)}",
                "PRINT",
                text="Hello FLUX"
            )
            print("Created:", node.id)

        def run_graph():
            self.BUILD_GRAPH()
            self.EXECUTE()

        ctk.CTkLabel(left, text="NODE TOOLBOX").pack(pady=10)

        ctk.CTkButton(left, text="AUDIO NODE", command=add_audio).pack(pady=5)
        ctk.CTkButton(left, text="PRINT NODE", command=add_print).pack(pady=5)
        ctk.CTkButton(left, text="RUN GRAPH", command=run_graph).pack(pady=20)

        app.mainloop()
# =========================================================
# FLUX EVERYDAY UTILITY SYSTEM
# (Apps, automation, tools, productivity layer)
# =========================================================

import os
import time
import threading
import datetime

class FLUXUtilityEngine:

    def __init__(self, engine):
        self.engine = engine
        self.tasks = {}
        self.apps = {}
        self.clipboard = ""
        self.scheduled = []

    # =========================================================
    # SIMPLE NOTES APP SYSTEM
    # =========================================================
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

    # =========================================================
    # TODO SYSTEM
    # =========================================================
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

    # =========================================================
    # TIMER SYSTEM
    # =========================================================
    def SET_TIMER(self, seconds, callback):
        def run():
            time.sleep(seconds)
            callback()

        threading.Thread(target=run, daemon=True).start()

    # =========================================================
    # SCHEDULER (DAILY / TIME BASED)
    # =========================================================
    def SCHEDULE(self, hour, minute, callback):

        def run():
            while True:
                now = datetime.datetime.now()
                if now.hour == hour and now.minute == minute:
                    callback()
                    time.sleep(60)
                time.sleep(1)

        threading.Thread(target=run, daemon=True).start()

    # =========================================================
    # FILE AUTOMATION SYSTEM
    # =========================================================
    def WRITE_FILE(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def READ_FILE(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    # =========================================================
    # AUTO FOLDER ORGANIZER
    # =========================================================
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
                os.rename(
                    os.path.join(path, file),
                    os.path.join(folder, file)
                )
            except:
                pass

    # =========================================================
    # CLIPBOARD SYSTEM (SIMPLE)
    # =========================================================
    def COPY(self, text):
        self.clipboard = text

    def PASTE(self):
        return self.clipboard

    # =========================================================
    # QUICK APP RUNNER (LIKE MINI OS LAUNCHER)
    # =========================================================
    def RUN_APP(self, name, func):
        self.apps[name] = {
            "type": "app",
            "run": func
        }

    def START_APP(self, name):
        app = self.apps.get(name)
        if app and app["type"] == "app":
            app["run"]()

    # =========================================================
    # BACKGROUND SERVICE SYSTEM
    # =========================================================
    def SERVICE(self, name, func, interval=5):

        def loop():
            while True:
                func()
                time.sleep(interval)

        threading.Thread(target=loop, daemon=True).start()
# =========================================================
# FLUX FULL UI CORE (CTK COMPLETE WRAPPER LAYER)
# Makes FLUX usable for real daily apps
# =========================================================

import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser


class FLUXUIRuntime:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.widgets = {}
        self.variables = {}

        self.font_default = ("Segoe UI", 14)

    # =========================================================
    # WINDOW CONTROL
    # =========================================================
    def WINDOW(self, title="FLUX APP", w=800, h=600):
        self.root.title(title)
        self.root.geometry(f"{w}x{h}")

    def RESIZEABLE(self, state=True):
        self.root.resizable(state, state)

    def ICONIFY(self):
        self.root.iconify()

    def FULLSCREEN(self, state=True):
        self.root.attributes("-fullscreen", state)

    # =========================================================
    # LABEL SYSTEM
    # =========================================================
    def LABEL(self, id, text, x=0, y=0, size=14):
        lbl = ctk.CTkLabel(self.root, text=text, font=("Segoe UI", size))
        lbl.place(x=x, y=y)
        self.widgets[id] = lbl

    def UPDATE_LABEL(self, id, text):
        if id in self.widgets:
            self.widgets[id].configure(text=text)

    # =========================================================
    # BUTTON SYSTEM
    # =========================================================
    def BUTTON(self, id, text, x, y, w=120, h=35, command=None):
        btn = ctk.CTkButton(self.root, text=text, width=w, height=h, command=command)
        btn.place(x=x, y=y)
        self.widgets[id] = btn

    def DISABLE_BUTTON(self, id):
        if id in self.widgets:
            self.widgets[id].configure(state="disabled")

    def ENABLE_BUTTON(self, id):
        if id in self.widgets:
            self.widgets[id].configure(state="normal")

    # =========================================================
    # INPUT SYSTEM
    # =========================================================
    def INPUT(self, id, x, y, w=200):
        entry = ctk.CTkEntry(self.root, width=w)
        entry.place(x=x, y=y)
        self.widgets[id] = entry

    def GET_INPUT(self, id):
        return self.widgets[id].get()

    def SET_INPUT(self, id, value):
        self.widgets[id].delete(0, "end")
        self.widgets[id].insert(0, value)

    # =========================================================
    # TEXTBOX (MULTI-LINE)
    # =========================================================
    def TEXTBOX(self, id, x, y, w=300, h=150):
        box = ctk.CTkTextbox(self.root, width=w, height=h)
        box.place(x=x, y=y)
        self.widgets[id] = box

    def WRITE_BOX(self, id, text):
        self.widgets[id].delete("0.0", "end")
        self.widgets[id].insert("0.0", text)

    def READ_BOX(self, id):
        return self.widgets[id].get("0.0", "end")

    # =========================================================
    # SWITCH / TOGGLE
    # =========================================================
    def SWITCH(self, id, x, y, text="Toggle"):
        var = ctk.BooleanVar()
        sw = ctk.CTkSwitch(self.root, text=text, variable=var)
        sw.place(x=x, y=y)
        self.widgets[id] = sw
        self.variables[id] = var

    def GET_SWITCH(self, id):
        return self.variables[id].get()

    # =========================================================
    # SLIDER
    # =========================================================
    def SLIDER(self, id, x, y, from_=0, to=100):
        slider = ctk.CTkSlider(self.root, from_=from_, to=to)
        slider.place(x=x, y=y)
        self.widgets[id] = slider

    def GET_SLIDER(self, id):
        return self.widgets[id].get()

    # =========================================================
    # PROGRESS BAR
    # =========================================================
    def PROGRESS(self, id, x, y, w=200):
        bar = ctk.CTkProgressBar(self.root, width=w)
        bar.place(x=x, y=y)
        self.widgets[id] = bar

    def SET_PROGRESS(self, id, value):
        self.widgets[id].set(value)

    # =========================================================
    # DROPDOWN
    # =========================================================
    def DROPDOWN(self, id, values, x, y):
        menu = ctk.CTkOptionMenu(self.root, values=values)
        menu.place(x=x, y=y)
        self.widgets[id] = menu

    def GET_DROPDOWN(self, id):
        return self.widgets[id].get()

    # =========================================================
    # FRAMES (LAYOUT SYSTEM)
    # =========================================================
    def FRAME(self, id, x, y, w=200, h=200):
        frame = ctk.CTkFrame(self.root, width=w, height=h)
        frame.place(x=x, y=y)
        self.widgets[id] = frame

    # =========================================================
    # POPUPS
    # =========================================================
    def ALERT(self, title, message):
        messagebox.showinfo(title, message)

    def ERROR(self, title, message):
        messagebox.showerror(title, message)

    def CONFIRM(self, title, message):
        return messagebox.askyesno(title, message)

    # =========================================================
    # FILE PICKER
    # =========================================================
    def OPEN_FILE(self):
        return filedialog.askopenfilename()

    def SAVE_FILE(self):
        return filedialog.asksaveasfilename()

    # =========================================================
    # COLOR PICKER
    # =========================================================
    def PICK_COLOR(self):
        return colorchooser.askcolor()

    # =========================================================
    # RUN LOOP
    # =========================================================
    def RUN(self):
        self.root.mainloop()
# =========================================================
# FLUX MATPLOTLIB ENGINE LAYER
# (Graphs, charts, analytics, dashboards)
# =========================================================

import matplotlib.pyplot as plt
import numpy as np
import threading


class FLUXGraphEngine:

    def __init__(self):
        self.figures = {}
        self.counter = 0

    # =========================================================
    # BASIC LINE PLOT
    # =========================================================
    def LINE_PLOT(self, x_data, y_data, title="Line Graph", xlabel="X", ylabel="Y"):

        self.counter += 1
        fig_id = f"fig_{self.counter}"

        plt.figure()

        plt.plot(x_data, y_data)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.grid(True)

        plt.show()

        self.figures[fig_id] = "line_plot"

        return fig_id

    # =========================================================
    # MULTI LINE PLOT
    # =========================================================
    def MULTI_LINE(self, datasets, labels=None, title="Multi Line"):

        plt.figure()

        for i, data in enumerate(datasets):
            plt.plot(data, label=(labels[i] if labels else f"Line {i+1}"))

        plt.title(title)
        plt.legend()
        plt.grid(True)

        plt.show()

    # =========================================================
    # BAR CHART
    # =========================================================
    def BAR_CHART(self, categories, values, title="Bar Chart"):

        plt.figure()

        plt.bar(categories, values)

        plt.title(title)

        plt.show()

    # =========================================================
    # PIE CHART
    # =========================================================
    def PIE_CHART(self, labels, values, title="Pie Chart"):

        plt.figure()

        plt.pie(values, labels=labels, autopct="%1.1f%%")

        plt.title(title)

        plt.show()

    # =========================================================
    # SCATTER PLOT
    # =========================================================
    def SCATTER(self, x, y, title="Scatter Plot"):

        plt.figure()

        plt.scatter(x, y)

        plt.title(title)

        plt.grid(True)

        plt.show()

    # =========================================================
    # HISTOGRAM
    # =========================================================
    def HISTOGRAM(self, data, bins=10, title="Histogram"):

        plt.figure()

        plt.hist(data, bins=bins)

        plt.title(title)

        plt.show()

    # =========================================================
    # REAL-TIME LIVE PLOT (THREAD BASED)
    # =========================================================
    def LIVE_PLOT(self, generator_func, interval=1, title="Live Plot"):

        plt.ion()
        fig, ax = plt.subplots()

        data_x = []
        data_y = []

        def loop():

            while True:

                x, y = generator_func()

                data_x.append(x)
                data_y.append(y)

                ax.clear()

                ax.plot(data_x, data_y)

                ax.set_title(title)

                plt.pause(interval)

        threading.Thread(target=loop, daemon=True).start()

    # =========================================================
    # DASHBOARD STYLE GRID PLOT
    # =========================================================
    def DASHBOARD(self, plots):

        plt.figure()

        for i, p in enumerate(plots):

            plt.subplot(len(plots), 1, i + 1)

            p()

        plt.show()

    # =========================================================
    # SAVE FIGURE
    # =========================================================
    def SAVE(self, filename="graph.png"):
        plt.savefig(filename)
# =========================================================
# FLUX GRAPH RETURN + DATA STORAGE SYSTEM
# (Save, retrieve, reuse graphs + datasets)
# =========================================================


class FLUXResultVault:

    def __init__(self):
        self.store = {}   # main registry
        self.last_id = None

    # =========================================================
    # SAVE ANY RESULT (IMAGE / DATA / GRAPH NAME)
    # =========================================================
    def SAVE(self, name, data_type, data):

        """
        data_type:
        - 'graph'
        - 'data'
        - 'image'
        - 'text'
        """

        self.store[name] = {
            "type": data_type,
            "data": data
        }

        self.last_id = name

        print(f"[FLUX] Saved -> {name} ({data_type})")

    # =========================================================
    # GET RESULT BY NAME
    # =========================================================
    def GET(self, name):

        return self.store.get(name, None)

    # =========================================================
    # GET ONLY DATA PART
    # =========================================================
    def GET_DATA(self, name):

        item = self.store.get(name)

        if item:
            return item["data"]

        return None

    # =========================================================
    # AUTO NAME RETURN (FOR GRAPHS)
    # =========================================================
    def AUTO_NAME(self, prefix="graph"):

        import time

        name = f"{prefix}_{int(time.time()*1000)}"

        return name

    # =========================================================
    # SAVE GRAPH FROM MPL ENGINE
    # =========================================================
    def SAVE_GRAPH(self, plt, name=None):

        if name is None:
            name = self.AUTO_NAME("graph")

        plt.savefig(f"{name}.png")

        self.SAVE(name, "graph", f"{name}.png")

        return name

    # =========================================================
    # LIST ALL SAVED ITEMS
    # =========================================================
    def LIST(self):

        return list(self.store.keys())

    # =========================================================
    # DELETE ITEM
    # =========================================================
    def DELETE(self, name):

        if name in self.store:
            del self.store[name]
            print(f"[FLUX] Deleted -> {name}")

    # =========================================================
    # CLEAR ALL
    # =========================================================
    def CLEAR(self):

        self.store.clear()
        print("[FLUX] Vault cleared")

    # =========================================================
    # EXPORT ALL DATA (for backup system)
    # =========================================================
    def EXPORT(self):

        return self.store
# =========================================================
# FLUX SAVE AS SYSTEM (ADVANCED EXPORT CONTROL)
# Adds user-defined file export for graphs & images
# =========================================================

import os


class FLUXSaveAsEngine:

    def __init__(self, vault):
        self.vault = vault

    # =========================================================
    # SAVE AS (MAIN FEATURE)
    # =========================================================
    def SAVE_AS(self, plt_object, filename):

        """
        filename examples:
        - graph.png
        - chart.jpg
        - output_1.png
        """

        # auto fix extension if missing
        if "." not in filename:
            filename += ".png"

        # ensure directory exists
        folder = os.path.dirname(filename)

        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        # save figure
        plt_object.savefig(filename)

        # store in vault
        self.vault.SAVE(
            name=filename,
            data_type="graph",
            data=filename
        )

        print(f"[FLUX] SAVE_AS -> {filename}")

        return filename

    # =========================================================
    # SAVE AS IMAGE (explicit helper)
    # =========================================================
    def SAVE_AS_IMAGE(self, plt_object, name, format="png"):

        filename = f"{name}.{format}"

        plt_object.savefig(filename)

        self.vault.SAVE(name, "image", filename)

        print(f"[FLUX] Image saved -> {filename}")

        return filename

    # =========================================================
    # SAVE AS DATA EXPORT
    # =========================================================
    def SAVE_AS_DATA(self, name, data, format="txt"):

        filename = f"{name}.{format}"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(data))

        self.vault.SAVE(name, "data", filename)

        print(f"[FLUX] Data saved -> {filename}")

        return filename

    # =========================================================
    # OVERWRITE SAVE (force replace)
    # =========================================================
    def OVERWRITE(self, plt_object, filename):

        if os.path.exists(filename):
            os.remove(filename)

        plt_object.savefig(filename)

        self.vault.SAVE(filename, "graph", filename)

        print(f"[FLUX] Overwritten -> {filename}")

        return filename

    # =========================================================
    # EXPORT MULTI FORMAT (png + jpg backup)
    # =========================================================
    def EXPORT_ALL(self, plt_object, name):

        png = f"{name}.png"
        jpg = f"{name}.jpg"

        plt_object.savefig(png)
        plt_object.savefig(jpg)

        self.vault.SAVE(name + "_png", "graph", png)
        self.vault.SAVE(name + "_jpg", "graph", jpg)

        print(f"[FLUX] Exported -> {png}, {jpg}")

        return [png, jpg]

    # =========================================================
    # QUICK EXPORT (auto decide format)
    # =========================================================
    def QUICK_SAVE(self, plt_object, name="output"):

        filename = f"{name}.png"

        plt_object.savefig(filename)

        self.vault.SAVE(name, "graph", filename)

        return filename
# =========================================================
# FLUX UNIFIED RUNTIME CORE
# (The "brain" that connects EVERYTHING)
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

    # =========================================================
    # EXECUTE GENERIC FLUX COMMAND
    # =========================================================
    def EXEC(self, command, *args, **kwargs):

        cmd = command.upper()

        # =====================================================
        # UI COMMANDS
        # =====================================================
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

        # =====================================================
        # GRAPH COMMANDS
        # =====================================================
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

        # =====================================================
        # SAVE / EXPORT SYSTEM
        # =====================================================
        elif cmd == "SAVE_AS":
            self.last_result = self.saveas.SAVE_AS(*args)

        elif cmd == "SAVE_AS_IMAGE":
            self.last_result = self.saveas.SAVE_AS_IMAGE(*args)

        elif cmd == "SAVE_AS_DATA":
            self.last_result = self.saveas.SAVE_AS_DATA(*args)

        # =====================================================
        # VAULT SYSTEM
        # =====================================================
        elif cmd == "SAVE":
            self.vault.SAVE(*args)

        elif cmd == "GET":
            self.last_result = self.vault.GET(*args)

        elif cmd == "GET_DATA":
            self.last_result = self.vault.GET_DATA(*args)

        elif cmd == "LIST":
            self.last_result = self.vault.LIST()

        # =====================================================
        # UTILITY SYSTEM
        # =====================================================
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

        # =====================================================
        # GAME ENGINE
        # =====================================================
        elif cmd == "CREATE_OBJECT":
            self.game.CREATE_OBJECT(*args)

        elif cmd == "FORCE":
            self.game.APPLY_FORCE(*args)

        elif cmd == "START_GAME":
            self.game.START_LOOP()

        elif cmd == "STOP_GAME":
            self.game.STOP_LOOP()

        # =====================================================
        # UNKNOWN COMMAND HANDLING
        # =====================================================
        else:
            print(f"[FLUX ERROR] Unknown command: {command}")

    # =========================================================
    # GET LAST OUTPUT (like return system)
    # =========================================================
    def RESULT(self):

        return self.last_result

    # =========================================================
    # STORE VARIABLE (FLUX MEMORY)
    # =========================================================
    def SET(self, key, value):

        self.memory[key] = value

    def GET_VAR(self, key):

        return self.memory.get(key, None)

    # =========================================================
    # RUN MULTI COMMAND SCRIPT (BASIC INTERPRETER)
    # =========================================================
    def RUN_SCRIPT(self, script_list):

        for line in script_list:

            if isinstance(line, dict):

                self.EXEC(line["cmd"], *line.get("args", []))