import matplotlib.pyplot as plt
import numpy as np
import threading
import os

# =========================================================
# FLUX RENDERER
# Handles: DOM rendering, graph output, result vault,
#          save-as export, and the FLUX IDE window
# =========================================================


# =========================================================
# DOM RENDERER (used by FLUXDOM.run)
# =========================================================

def render_dom_node(engine, dom, node):
    """Recursively render a parsed DOM tree node into engine UI calls."""

    t = node["type"]

    if t == "ROOT":
        for c in node["children"]:
            render_dom_node(engine, dom, c)

    elif t in ["COLUMN", "ROW", "FRAME"]:
        for c in node["children"]:
            render_dom_node(engine, dom, c)

    elif t == "BUTTON":
        engine.CTK_CTkButton(node["name"], text=node["text"])
        for c in node.get("children", []):
            if c["type"] == "EVENT":
                engine.BIND_CLICK(node["name"], lambda a=c["action"]: dom.wrap_action(a)())

    elif t == "TEXT":
        engine.CTK_CTkLabel(f"text_{node['text'][:5]}", text=node["text"])

    elif t == "INPUT":
        engine.CTK_CTkEntry(node["name"])

    elif t == "EVENT":
        engine.ONCLICK(node["target"], dom.wrap_action(node["action"]))


# =========================================================
# FLUX GRAPH ENGINE
# =========================================================

class FLUXGraphEngine:

    def __init__(self):
        self.figures = {}
        self.counter = 0

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

    def MULTI_LINE(self, datasets, labels=None, title="Multi Line"):
        plt.figure()
        for i, data in enumerate(datasets):
            plt.plot(data, label=(labels[i] if labels else f"Line {i+1}"))
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()

    def BAR_CHART(self, categories, values, title="Bar Chart"):
        plt.figure()
        plt.bar(categories, values)
        plt.title(title)
        plt.show()

    def PIE_CHART(self, labels, values, title="Pie Chart"):
        plt.figure()
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title(title)
        plt.show()

    def SCATTER(self, x, y, title="Scatter Plot"):
        plt.figure()
        plt.scatter(x, y)
        plt.title(title)
        plt.grid(True)
        plt.show()

    def HISTOGRAM(self, data, bins=10, title="Histogram"):
        plt.figure()
        plt.hist(data, bins=bins)
        plt.title(title)
        plt.show()

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

    def DASHBOARD(self, plots):
        plt.figure()
        for i, p in enumerate(plots):
            plt.subplot(len(plots), 1, i + 1)
            p()
        plt.show()

    def SAVE(self, filename="graph.png"):
        plt.savefig(filename)


# =========================================================
# FLUX RESULT VAULT
# =========================================================

class FLUXResultVault:

    def __init__(self):
        self.store = {}
        self.last_id = None

    def SAVE(self, name, data_type, data):
        self.store[name] = {"type": data_type, "data": data}
        self.last_id = name
        print(f"[FLUX] Saved -> {name} ({data_type})")

    def GET(self, name):
        return self.store.get(name, None)

    def GET_DATA(self, name):
        item = self.store.get(name)
        if item:
            return item["data"]
        return None

    def AUTO_NAME(self, prefix="graph"):
        import time
        return f"{prefix}_{int(time.time()*1000)}"

    def SAVE_GRAPH(self, plt, name=None):
        if name is None:
            name = self.AUTO_NAME("graph")
        plt.savefig(f"{name}.png")
        self.SAVE(name, "graph", f"{name}.png")
        return name

    def LIST(self):
        return list(self.store.keys())

    def DELETE(self, name):
        if name in self.store:
            del self.store[name]
            print(f"[FLUX] Deleted -> {name}")

    def CLEAR(self):
        self.store.clear()
        print("[FLUX] Vault cleared")

    def EXPORT(self):
        return self.store


# =========================================================
# FLUX SAVE AS ENGINE
# =========================================================

class FLUXSaveAsEngine:

    def __init__(self, vault):
        self.vault = vault

    def SAVE_AS(self, plt_object, filename):
        if "." not in filename:
            filename += ".png"

        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        plt_object.savefig(filename)
        self.vault.SAVE(name=filename, data_type="graph", data=filename)
        print(f"[FLUX] SAVE_AS -> {filename}")
        return filename

    def SAVE_AS_IMAGE(self, plt_object, name, format="png"):
        filename = f"{name}.{format}"
        plt_object.savefig(filename)
        self.vault.SAVE(name, "image", filename)
        print(f"[FLUX] Image saved -> {filename}")
        return filename

    def SAVE_AS_DATA(self, name, data, format="txt"):
        filename = f"{name}.{format}"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(data))
        self.vault.SAVE(name, "data", filename)
        print(f"[FLUX] Data saved -> {filename}")
        return filename

    def OVERWRITE(self, plt_object, filename):
        if os.path.exists(filename):
            os.remove(filename)
        plt_object.savefig(filename)
        self.vault.SAVE(filename, "graph", filename)
        print(f"[FLUX] Overwritten -> {filename}")
        return filename

    def EXPORT_ALL(self, plt_object, name):
        png = f"{name}.png"
        jpg = f"{name}.jpg"
        plt_object.savefig(png)
        plt_object.savefig(jpg)
        self.vault.SAVE(name + "_png", "graph", png)
        self.vault.SAVE(name + "_jpg", "graph", jpg)
        print(f"[FLUX] Exported -> {png}, {jpg}")
        return [png, jpg]

    def QUICK_SAVE(self, plt_object, name="output"):
        filename = f"{name}.png"
        plt_object.savefig(filename)
        self.vault.SAVE(name, "graph", filename)
        return filename


# =========================================================
# FLUX IDE WINDOW
# =========================================================

import customtkinter as ctk
import time as _time


class FLUXIDE:

    def __init__(self, engine, compiler, debugger, builder):
        self.engine = engine
        self.compiler = compiler
        self.debugger = debugger
        self.builder = builder
        self.file_path = None
        self.running = False

    def LAUNCH(self):
        self.app = ctk.CTk()
        self.app.title("FLUX IDE PRO")
        self.app.geometry("1000x600")

        self.left = ctk.CTkFrame(self.app, width=200)
        self.left.pack(side="left", fill="y")

        ctk.CTkLabel(self.left, text="FLUX IDE", font=("Arial", 20)).pack(pady=10)
        ctk.CTkButton(self.left, text="RUN", command=self.RUN_FILE).pack(pady=5)
        ctk.CTkButton(self.left, text="BUILD EXE", command=self.BUILD).pack(pady=5)
        ctk.CTkButton(self.left, text="DEBUG MODE", command=self.DEBUG).pack(pady=5)
        ctk.CTkButton(self.left, text="LIVE RELOAD", command=self.LIVE).pack(pady=5)

        self.editor = ctk.CTkTextbox(self.app, width=600)
        self.editor.pack(side="left", fill="both", expand=True)

        self.right = ctk.CTkFrame(self.app, width=200)
        self.right.pack(side="right", fill="y")

        ctk.CTkLabel(self.right, text="OUTPUT").pack()

        self.output = ctk.CTkTextbox(self.right, height=300)
        self.output.pack(fill="both", expand=True)

        self.app.mainloop()

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

    def DEBUG(self):
        self.output.insert("end", "\n[DEBUG MODE ENABLED]\n")
        self.debugger.launch_ide()

    def BUILD(self):
        self.output.insert("end", "\n[BUILDING EXE]\n")
        try:
            self.builder.BUILD_EXE()
            self.output.insert("end", "[BUILD COMPLETE]\n")
        except Exception as e:
            self.output.insert("end", f"[BUILD ERROR] {e}\n")

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
                    _time.sleep(1)
                except Exception as e:
                    self.output.insert("end", f"[LIVE ERROR] {e}\n")

        threading.Thread(target=watcher, daemon=True).start()
