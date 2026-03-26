import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser

# =========================================================
# FLUX UI COMPONENT DEFINITIONS
# Widget registration, CTK/TK wrappers, FLUXUIRuntime,
# FLUXNode and FLUXNodeEngine
# =========================================================


# =========================================================
# WIDGET MIXIN — mixed into FLUX core class
# =========================================================

class FLUXWidgetMixin:
    """
    All CTK / TK widget factory methods.
    Expects self.root and self.widgets to exist (provided by FLUX core).
    """

    def _register(self, name, widget):
        self.widgets[name] = widget
        return widget

    # =========================================================
    # CTK WIDGETS
    # =========================================================
    def CTK_CTkLabel(self, name, **kwargs):
        widget = ctk.CTkLabel(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkButton(self, name, **kwargs):
        widget = ctk.CTkButton(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkEntry(self, name, **kwargs):
        widget = ctk.CTkEntry(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkFrame(self, name, **kwargs):
        widget = ctk.CTkFrame(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkTextbox(self, name, **kwargs):
        widget = ctk.CTkTextbox(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkSwitch(self, name, **kwargs):
        widget = ctk.CTkSwitch(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkSlider(self, name, **kwargs):
        widget = ctk.CTkSlider(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkProgressBar(self, name, **kwargs):
        widget = ctk.CTkProgressBar(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkOptionMenu(self, name, **kwargs):
        widget = ctk.CTkOptionMenu(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkComboBox(self, name, **kwargs):
        widget = ctk.CTkComboBox(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkTabview(self, name, **kwargs):
        widget = ctk.CTkTabview(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    def CTK_CTkScrollableFrame(self, name, **kwargs):
        widget = ctk.CTkScrollableFrame(self.root, **kwargs)
        widget.pack()
        return self._register(name, widget)

    # =========================================================
    # TK RAW BINDINGS
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
    # WIDGET ACCESS
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


# =========================================================
# FLUX UI RUNTIME (standalone full CTK wrapper)
# =========================================================

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
    # LABEL
    # =========================================================
    def LABEL(self, id, text, x=0, y=0, size=14):
        lbl = ctk.CTkLabel(self.root, text=text, font=("Segoe UI", size))
        lbl.place(x=x, y=y)
        self.widgets[id] = lbl

    def UPDATE_LABEL(self, id, text):
        if id in self.widgets:
            self.widgets[id].configure(text=text)

    # =========================================================
    # BUTTON
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
    # INPUT
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
    # TEXTBOX
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
    # FRAME
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
    # FILE / COLOR PICKERS
    # =========================================================
    def OPEN_FILE(self):
        return filedialog.askopenfilename()

    def SAVE_FILE(self):
        return filedialog.asksaveasfilename()

    def PICK_COLOR(self):
        return colorchooser.askcolor()

    # =========================================================
    # RUN LOOP
    # =========================================================
    def RUN(self):
        self.root.mainloop()


# =========================================================
# FLUX NODE (visual programming primitive)
# =========================================================

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


# =========================================================
# FLUX NODE ENGINE
# =========================================================

class FLUXNodeEngine:

    def __init__(self, engine):
        self.engine = engine
        self.nodes = {}
        self.execution_order = []

    def CREATE_NODE(self, node_id, node_type, **data):
        node = FLUXNode(node_id, node_type, data)
        self.nodes[node_id] = node
        return node

    def CONNECT(self, from_id, to_id):
        if from_id in self.nodes and to_id in self.nodes:
            self.nodes[from_id].connect(self.nodes[to_id])

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

    def EXECUTE(self):
        for node in self.execution_order:
            t = node.type
            d = node.data

            if t == "AUDIO":
                self.engine.AUDIO(d.get("file", ""))
            elif t == "PRINT":
                print(d.get("text", ""))
            elif t == "GRAPH":
                self.engine.GRAPH([1, 2, 3], [3, 6, 9])
            elif t == "SET":
                self.engine.SET_VAR(d.get("key"), d.get("value"))
            elif t == "WAIT":
                import time
                time.sleep(d.get("seconds", 1))

    def LAUNCH_EDITOR(self):
        app = ctk.CTk()
        app.title("FLUX NODE EDITOR")
        app.geometry("900x600")

        left = ctk.CTkFrame(app, width=200)
        left.pack(side="left", fill="y")

        canvas = ctk.CTkFrame(app)
        canvas.pack(side="right", fill="both", expand=True)

        def add_audio():
            node = self.CREATE_NODE(f"audio_{len(self.nodes)}", "AUDIO", file="click.wav")
            print("Created:", node.id)

        def add_print():
            node = self.CREATE_NODE(f"print_{len(self.nodes)}", "PRINT", text="Hello FLUX")
            print("Created:", node.id)

        def run_graph():
            self.BUILD_GRAPH()
            self.EXECUTE()

        ctk.CTkLabel(left, text="NODE TOOLBOX").pack(pady=10)
        ctk.CTkButton(left, text="AUDIO NODE", command=add_audio).pack(pady=5)
        ctk.CTkButton(left, text="PRINT NODE", command=add_print).pack(pady=5)
        ctk.CTkButton(left, text="RUN GRAPH", command=run_graph).pack(pady=20)

        app.mainloop()
