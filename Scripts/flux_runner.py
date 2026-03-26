"""
flux_runner.py — headless FLUX runner (no GUI window needed for logic tests)
Usage:  python flux_runner.py Test.flux
"""
import sys
import os

# Minimal engine stub for headless testing (no CTK required)
class HeadlessEngine:
    def __init__(self):
        self.vars   = {}
        self.widgets = {}
    def APP(self, title, w, h):
        print(f"[APP] {title!r} {w}x{h}")
    def AUDIO(self, file, loop=False):
        print(f"[AUDIO] {file!r} loop={loop}")
    def AUDIO_STOP(self):
        print("[AUDIO_STOP]")
    def VIDEO(self, file, window_name="FLUX VIDEO"):
        print(f"[VIDEO] {file!r}")

def run(filepath: str):
    from parser import FLUXParser
    engine = HeadlessEngine()
    p      = FLUXParser(engine)
    ok     = p.compile(filepath)
    if p.errors:
        print("\n[ERRORS]")
        for e in p.errors:
            print(" ", e)
    return ok

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "Test.flux"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)
    success = run(path)
    sys.exit(0 if success else 1)
