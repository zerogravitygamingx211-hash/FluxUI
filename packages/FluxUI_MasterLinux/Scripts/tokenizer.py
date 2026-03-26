"""
=============================================================================
FLUX LANGUAGE  —  TOKENIZER / LEXER                          tokenizer.py
=============================================================================
Full character-level lexer.
Token types are a proper Enum — no string literals, no silent typos.
Produces a flat list of Token objects from raw FLUX source text.
Nothing from the parser, engine, or IDE lives here.
=============================================================================
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Dict, Tuple, Any


# =============================================================================
# TOKEN TYPE ENUM  — every type is a named constant, never a raw string
# =============================================================================

class TT(Enum):
    # ── Literals ──────────────────────────────────────────────────────────────
    IDENT        = auto()
    KEYWORD      = auto()
    STRING       = auto()
    FSTRING      = auto()
    NUMBER       = auto()
    FLOAT        = auto()
    BOOL         = auto()
    NULL         = auto()

    # ── Punctuation ───────────────────────────────────────────────────────────
    LBRACE       = auto()   # {
    RBRACE       = auto()   # }
    LPAREN       = auto()   # (
    RPAREN       = auto()   # )
    LBRACKET     = auto()   # [
    RBRACKET     = auto()   # ]
    COMMA        = auto()   # ,
    COLON        = auto()   # :
    SEMICOLON    = auto()   # ;
    DOT          = auto()   # .
    DOTDOT       = auto()   # ..
    DOTDOTDOT    = auto()   # ...
    AT           = auto()   # @
    QUESTION     = auto()   # ?

    # ── Assignment & comparison ───────────────────────────────────────────────
    EQUALS       = auto()   # =
    EQEQ         = auto()   # ==
    NEQ          = auto()   # !=
    LT           = auto()   # <
    GT           = auto()   # >
    LTE          = auto()   # <=
    GTE          = auto()   # >=

    # ── Arithmetic ────────────────────────────────────────────────────────────
    PLUS         = auto()   # +
    MINUS        = auto()   # -
    STAR         = auto()   # *
    SLASH        = auto()   # /
    PERCENT      = auto()   # %
    STARSTAR     = auto()   # **
    DOUBLESLASH  = auto()   # //

    # ── Compound assignment ───────────────────────────────────────────────────
    PLUS_EQ      = auto()   # +=
    MINUS_EQ     = auto()   # -=
    STAR_EQ      = auto()   # *=
    SLASH_EQ     = auto()   # /=
    PERCENT_EQ   = auto()   # %=

    # ── Bitwise ───────────────────────────────────────────────────────────────
    AMPERSAND    = auto()   # &
    PIPE         = auto()   # |
    CARET        = auto()   # ^
    TILDE        = auto()   # ~
    LSHIFT       = auto()   # <<
    RSHIFT       = auto()   # >>

    # ── Logical / unary ───────────────────────────────────────────────────────
    BANG         = auto()   # !
    ARROW        = auto()   # ->
    FAT_ARROW    = auto()   # =>

    # ── Structure ─────────────────────────────────────────────────────────────
    NEWLINE      = auto()
    COMMENT      = auto()
    MULTICOMMENT = auto()
    EOF          = auto()
    UNKNOWN      = auto()


# =============================================================================
# FLUX RESERVED KEYWORDS
# =============================================================================

FLUX_KEYWORDS: frozenset = frozenset({
    # Window / App lifecycle
    "APP","WINDOW","TITLE","SIZE","RESIZE","FULLSCREEN","ICONIFY",
    "MINIMIZE","MAXIMIZE","RESTORE","CLOSE","FOCUS","RAISE","LOWER",
    "OPACITY","TOPMOST","THEME","APPEARANCE","COLOR_THEME","ICON",
    "PROTOCOL","GEOMETRY","MINSIZE","MAXSIZE","RESIZABLE",
    # Layout containers
    "FRAME","SCROLLFRAME","TABVIEW","TAB","PANE","SPLITPANE",
    "ROW","COLUMN","GRID","STACK","OVERLAY","GROUP","PANEL","SECTION",
    # Basic widgets
    "BUTTON","LABEL","INPUT","TEXTBOX","SWITCH","SLIDER","PROGRESS",
    "DROPDOWN","COMBOBOX","RADIOBUTTON","CHECKBOX","LISTBOX","SPINBOX",
    "SEPARATOR","IMAGE","CANVAS","SCROLLBAR","TOOLTIP","LINK","BADGE",
    # Menu system
    "MENUBAR","MENU","MENUITEM","MENUSEPARATOR","CONTEXTMENU","SUBMENU",
    # Advanced widgets
    "TREEVIEW","TABLE","DATEPICKER","TIMEPICKER","COLORPICKER",
    "FILEPICKER","FOLDERPICKER","FONTPICKER","NOTIFICATION",
    "STATUSBAR","TOOLBAR","SIDEBAR","DIALOG","MODAL","DRAWER",
    "POPOVER","ACCORDION","CAROUSEL","STEPPER","RATING","AVATAR",
    "CHIP","TAG","CARD","DIVIDER","SPACER","ICON_BUTTON",
    # Widget property keywords
    "TEXT","PLACEHOLDER","VALUE","WIDTH","HEIGHT","X","Y",
    "BG","FG","FONT","FONT_SIZE","FONT_WEIGHT","FONT_FAMILY","FONT_STYLE",
    "BORDER","BORDER_COLOR","BORDER_WIDTH","RADIUS","PADDING","MARGIN",
    "SHADOW","CURSOR","ANCHOR","JUSTIFY","WRAP","TRUNCATE",
    "STATE","ENABLED","DISABLED","READONLY","HIDDEN","VISIBLE",
    "STICKY","EXPAND","FILL","SIDE","RELIEF","COMPOUND",
    # Placement
    "PLACE","PACK","GRID_PLACE","PLACE_CENTER","PLACE_FILL","PLACE_STRETCH",
    # Events
    "ONCLICK","ONDOUBLECLICK","ONRIGHTCLICK","ONCHANGE","ONINPUT",
    "ONHOVER","ONLEAVE","ONKEY","ONKEYDOWN","ONKEYUP","ONKEYPRESS",
    "ONFOCUS","ONBLUR","ONSCROLL","ONRESIZE","ONCLOSE","ONOPEN",
    "ONSUBMIT","ONDROP","ONDRAG","ONDRAGSTART","ONDRAGEND",
    "ONSELECT","ONCHECK","ONUNCHECK","ONTOGGLE","ONLOAD","ONUNLOAD",
    "ONMOUSEDOWN","ONMOUSEUP","ONMOUSEMOVE","ONMOUSEENTER","ONMOUSELEAVE",
    # Widget actions
    "SHOW","HIDE","ENABLE","DISABLE","UPDATE","CLEAR","REFRESH","REDRAW",
    "SET_TEXT","GET_TEXT","SET_VALUE","GET_VALUE","SET_COLOR","GET_COLOR",
    "SET_FONT","GET_FONT","SET_SIZE","GET_SIZE","SET_POS","GET_POS",
    "SET_STATE","GET_STATE","FOCUS_WIDGET","SCROLL_TO","SCROLL_TOP",
    "ADD_ITEM","REMOVE_ITEM","GET_ITEM","SELECT_ITEM","CLEAR_ITEMS",
    "ADD_TAB","REMOVE_TAB","SELECT_TAB","GET_TAB","GET_ACTIVE_TAB",
    "ADD_ROW","REMOVE_ROW","GET_ROW","ADD_COL","REMOVE_COL","GET_COL",
    "INSERT_TEXT","DELETE_TEXT","SELECT_ALL","DESELECT_ALL",
    "MOVE_WIDGET","RESIZE_WIDGET","DESTROY_WIDGET","CLONE_WIDGET",
    # Variables
    "VAR","LET","CONST","SET","GET","DEL","TYPEOF","INSTANCEOF",
    # Control flow
    "IF","ELSE","ELIF","WHILE","FOR","IN","RANGE","STEP",
    "BREAK","CONTINUE","RETURN","PASS","YIELD",
    "MATCH","CASE","DEFAULT","SWITCH_CASE",
    "TRY","CATCH","FINALLY","THROW","RAISE","ASSERT",
    # Functions
    "FUNC","LAMBDA","CALL","END","ASYNC","AWAIT","DEFER",
    # Operators / literals
    "AND","OR","NOT","IS","TRUE","FALSE","NULL","NONE",
    # Output / dialogs
    "PRINT","ALERT","ERROR","CONFIRM","PROMPT","LOG","WARN","DEBUG_PRINT",
    # Audio
    "AUDIO","AUDIO_STOP","AUDIO_PAUSE","AUDIO_RESUME",
    "AUDIO_VOLUME","AUDIO_SEEK","AUDIO_LOOP","AUDIO_DURATION",
    "AUDIO_POSITION","AUDIO_SPEED","AUDIO_FADE_IN","AUDIO_FADE_OUT",
    # Video
    "VIDEO","VIDEO_STOP","VIDEO_PAUSE","VIDEO_RESUME",
    "VIDEO_SEEK","VIDEO_VOLUME","VIDEO_FULLSCREEN","VIDEO_DURATION",
    "VIDEO_POSITION","VIDEO_SPEED","VIDEO_SNAPSHOT","VIDEO_LOOP",
    # Graph / chart
    "GRAPH","LINE_PLOT","BAR_CHART","PIE_CHART","SCATTER",
    "HISTOGRAM","MULTI_LINE","LIVE_PLOT","DASHBOARD",
    "AREA_CHART","BOX_PLOT","HEATMAP","VIOLIN_PLOT","BUBBLE_CHART",
    "CANDLESTICK","WATERFALL","FUNNEL","RADAR","POLAR",
    "GRAPH_TITLE","GRAPH_XLABEL","GRAPH_YLABEL","GRAPH_LEGEND",
    "GRAPH_GRID","GRAPH_STYLE","GRAPH_COLOR","GRAPH_MARKER",
    "GRAPH_LINE_STYLE","GRAPH_XLIM","GRAPH_YLIM","GRAPH_ZLIM",
    "GRAPH_XTICKS","GRAPH_YTICKS","GRAPH_ANNOTATE","GRAPH_TEXT",
    "GRAPH_SAVE","GRAPH_SHOW","GRAPH_CLOSE","GRAPH_CLEAR",
    "SUBPLOT","FIGURE","AXES","COLORBAR","LEGEND","TIGHT_LAYOUT",
    # File / IO
    "WRITE_FILE","READ_FILE","APPEND_FILE","DELETE_FILE",
    "COPY_FILE","MOVE_FILE","EXISTS_FILE","FILE_SIZE","FILE_INFO",
    "MAKE_DIR","LIST_DIR","DELETE_DIR","ORGANIZE_FOLDER","RENAME_FILE",
    "OPEN_FILE","SAVE_FILE","OPEN_FOLDER","WATCH_FILE",
    # Clipboard
    "COPY","PASTE","CLIPBOARD_CLEAR","CLIPBOARD_GET","CLIPBOARD_SET",
    # Timing
    "WAIT","LOOP","AFTER","TIMER","SCHEDULE","CANCEL_TIMER",
    "TIMESTAMP","DATE","TIME_NOW","STOPWATCH","INTERVAL","TIMEOUT",
    # Network
    "HTTP_GET","HTTP_POST","HTTP_PUT","HTTP_DELETE","HTTP_PATCH",
    "WEBSOCKET","SOCKET","DOWNLOAD","UPLOAD","FETCH","REQUEST",
    # Data
    "JSON_PARSE","JSON_STRINGIFY","CSV_READ","CSV_WRITE",
    "DB_CONNECT","DB_QUERY","DB_INSERT","DB_UPDATE","DB_DELETE",
    "XML_PARSE","XML_WRITE","YAML_PARSE","YAML_WRITE",
    # Build / run
    "RUN","BUILD","LIVE","IMPORT","EXPORT","INCLUDE","REQUIRE",
    # Style blocks
    "STYLE","THEME_DARK","THEME_LIGHT","THEME_SYSTEM",
    "ANIMATE","TRANSITION","KEYFRAME","EASING",
    # Math builtins
    "ABS","CEIL","FLOOR","ROUND","SQRT","POW","SIN","COS","TAN",
    "MIN","MAX","SUM","AVG","RANDOM","RANDINT","PI","E",
    # String builtins
    "STR_UPPER","STR_LOWER","STR_TRIM","STR_SPLIT","STR_JOIN",
    "STR_REPLACE","STR_CONTAINS","STR_STARTS","STR_ENDS",
    "STR_LEN","STR_SLICE","STR_FORMAT","STR_REPEAT","STR_REVERSE",
    # List builtins
    "LIST_APPEND","LIST_REMOVE","LIST_POP","LIST_INSERT","LIST_SORT",
    "LIST_REVERSE","LIST_FIND","LIST_FILTER","LIST_MAP","LIST_REDUCE",
    "LIST_LEN","LIST_SLICE","LIST_UNIQUE","LIST_FLATTEN","LIST_ZIP",
    # Dict builtins
    "DICT_GET","DICT_SET","DICT_DEL","DICT_KEYS","DICT_VALUES",
    "DICT_ITEMS","DICT_HAS","DICT_MERGE","DICT_COPY","DICT_CLEAR",
    # Type conversion
    "TO_INT","TO_FLOAT","TO_STR","TO_BOOL","TO_LIST","TO_DICT",
    # System
    "SYS_EXIT","SYS_ARGS","SYS_ENV","SYS_PLATFORM","SYS_CWD",
    "SYS_EXEC","SYS_OPEN","SYS_NOTIFY","SYS_TRAY",
})

# Keyword subsets used by parsers for fast dispatch
WIDGET_KEYWORDS: frozenset = frozenset({
    "BUTTON","LABEL","INPUT","TEXTBOX","SWITCH","SLIDER","PROGRESS",
    "DROPDOWN","COMBOBOX","RADIOBUTTON","CHECKBOX","LISTBOX","SPINBOX",
    "SEPARATOR","IMAGE","CANVAS","SCROLLBAR","TOOLTIP","LINK","BADGE",
    "FRAME","SCROLLFRAME","TABVIEW","TREEVIEW","TABLE","MENUBAR",
    "MENU","MENUITEM","STATUSBAR","TOOLBAR","SIDEBAR","DIALOG","MODAL",
    "DRAWER","POPOVER","ACCORDION","CAROUSEL","STEPPER","RATING",
    "AVATAR","CHIP","TAG","CARD","DIVIDER","SPACER","ICON_BUTTON",
    "DATEPICKER","TIMEPICKER","COLORPICKER","FILEPICKER","FOLDERPICKER",
    "FONTPICKER","NOTIFICATION","CONTEXTMENU","SUBMENU","MENUSEPARATOR",
    "SPLITPANE","PANE","OVERLAY","GROUP","PANEL","SECTION",
    "ROW","COLUMN","GRID","STACK","TAB",
})

EVENT_KEYWORDS: frozenset = frozenset({
    "ONCLICK","ONDOUBLECLICK","ONRIGHTCLICK","ONCHANGE","ONINPUT",
    "ONHOVER","ONLEAVE","ONKEY","ONKEYDOWN","ONKEYUP","ONKEYPRESS",
    "ONFOCUS","ONBLUR","ONSCROLL","ONRESIZE","ONCLOSE","ONOPEN",
    "ONSUBMIT","ONDROP","ONDRAG","ONDRAGSTART","ONDRAGEND",
    "ONSELECT","ONCHECK","ONUNCHECK","ONTOGGLE","ONLOAD","ONUNLOAD",
    "ONMOUSEDOWN","ONMOUSEUP","ONMOUSEMOVE","ONMOUSEENTER","ONMOUSELEAVE",
})

GRAPH_KEYWORDS: frozenset = frozenset({
    "GRAPH","LINE_PLOT","BAR_CHART","PIE_CHART","SCATTER",
    "HISTOGRAM","MULTI_LINE","LIVE_PLOT","DASHBOARD",
    "AREA_CHART","BOX_PLOT","HEATMAP","VIOLIN_PLOT","BUBBLE_CHART",
    "CANDLESTICK","WATERFALL","FUNNEL","RADAR","POLAR",
    "SUBPLOT","FIGURE","AXES",
})

CONTROL_FLOW_KEYWORDS: frozenset = frozenset({
    "IF","ELSE","ELIF","WHILE","FOR","BREAK","CONTINUE","RETURN",
    "PASS","YIELD","MATCH","CASE","DEFAULT","TRY","CATCH","FINALLY",
    "THROW","RAISE","ASSERT",
})

OPERATOR_KEYWORDS: frozenset = frozenset({"AND","OR","NOT","IS","IN"})
LITERAL_KEYWORDS:  frozenset = frozenset({"TRUE","FALSE","NULL","NONE"})

ARITHMETIC_TYPES: frozenset = frozenset({
    TT.PLUS, TT.MINUS, TT.STAR, TT.SLASH, TT.PERCENT,
    TT.STARSTAR, TT.DOUBLESLASH,
})
COMPARISON_TYPES: frozenset = frozenset({
    TT.EQEQ, TT.NEQ, TT.LT, TT.GT, TT.LTE, TT.GTE,
})
ASSIGN_COMPOUND: frozenset = frozenset({
    TT.PLUS_EQ, TT.MINUS_EQ, TT.STAR_EQ, TT.SLASH_EQ, TT.PERCENT_EQ,
})


# =============================================================================
# SOURCE POSITION  — immutable value object
# =============================================================================

@dataclass(frozen=True)
class SourcePos:
    line:   int = 1
    col:    int = 1
    offset: int = 0

    def __repr__(self) -> str:
        return f"L{self.line}:C{self.col}"

    def advance_col(self, n: int = 1) -> "SourcePos":
        return SourcePos(self.line, self.col + n, self.offset + n)

    def advance_line(self) -> "SourcePos":
        return SourcePos(self.line + 1, 1, self.offset + 1)


# =============================================================================
# TOKEN  — immutable, typed, positioned
# =============================================================================

@dataclass(frozen=True)
class Token:
    type:  TT
    value: str
    pos:   SourcePos = field(default_factory=SourcePos)

    # ── convenience predicates ───────────────────────────────────────────────

    def is_kw(self, *words: str) -> bool:
        """True if this is a KEYWORD token matching any of the given words."""
        return self.type is TT.KEYWORD and self.value.upper() in {w.upper() for w in words}

    def is_tt(self, *types: TT) -> bool:
        """True if this token's type is one of the given TT members."""
        return self.type in types

    def is_widget(self) -> bool:
        return self.type is TT.KEYWORD and self.value.upper() in WIDGET_KEYWORDS

    def is_event(self) -> bool:
        return self.type is TT.KEYWORD and self.value.upper() in EVENT_KEYWORDS

    def is_graph(self) -> bool:
        return self.type is TT.KEYWORD and self.value.upper() in GRAPH_KEYWORDS

    def is_control_flow(self) -> bool:
        return self.type is TT.KEYWORD and self.value.upper() in CONTROL_FLOW_KEYWORDS

    def is_literal(self) -> bool:
        return self.type in (TT.STRING, TT.FSTRING, TT.NUMBER, TT.FLOAT, TT.BOOL, TT.NULL)

    def is_operator(self) -> bool:
        return self.type in ARITHMETIC_TYPES | COMPARISON_TYPES or (
            self.type is TT.KEYWORD and self.value.upper() in OPERATOR_KEYWORDS
        )

    def is_assign_op(self) -> bool:
        return self.type is TT.EQUALS or self.type in ASSIGN_COMPOUND

    def is_eof(self) -> bool:
        return self.type is TT.EOF

    def is_newline(self) -> bool:
        return self.type is TT.NEWLINE

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.pos})"


# =============================================================================
# LEXER ERRORS
# =============================================================================

class LexerError(Exception):
    def __init__(self, msg: str, pos: SourcePos, filename: str = "<stdin>"):
        super().__init__(f"[LEXER] {filename} {pos}: {msg}")
        self.pos      = pos
        self.filename = filename


# =============================================================================
# FLUX LEXER  — full character-level, zero regex
# =============================================================================

class FLUXLexer:
    """
    Converts raw FLUX source text into a flat list of Token objects.
    Every character is handled explicitly — no regex, no shortcuts.
    """

    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source:   str         = source
        self.filename: str         = filename
        self._len:     int         = len(source)
        self._pos:     int         = 0
        self._line:    int         = 1
        self._col:     int         = 1
        self._tokens:  list[Token] = []

    # ── low-level character access ───────────────────────────────────────────

    def _ch(self, offset: int = 0) -> str:
        idx = self._pos + offset
        return self.source[idx] if idx < self._len else ""

    def _advance(self) -> str:
        ch = self.source[self._pos]
        self._pos += 1
        if ch == "\n":
            self._line += 1
            self._col   = 1
        else:
            self._col += 1
        return ch

    def _here(self) -> SourcePos:
        return SourcePos(self._line, self._col, self._pos)

    def _tok(self, tt: TT, value: str, pos: SourcePos) -> Token:
        return Token(tt, value, pos)

    def _emit(self, tt: TT, value: str, pos: SourcePos):
        self._tokens.append(Token(tt, value, pos))

    # ── whitespace (spaces/tabs only — newlines are tokens) ─────────────────

    def _skip_spaces(self):
        while self._pos < self._len and self._ch() in (" ", "\t", "\r"):
            self._advance()

    # ── string literals ──────────────────────────────────────────────────────

    def _read_string(self) -> Token:
        pos   = self._here()
        quote = self._advance()
        buf   = []
        is_f  = (self._tokens and
                 self._tokens[-1].type is TT.IDENT and
                 self._tokens[-1].value.lower() == "f")
        if is_f:
            self._tokens.pop()

        while self._pos < self._len:
            ch = self._ch()
            if ch == "\\":
                self._advance()
                esc = self._advance()
                mapping = {
                    "n": "\n", "t": "\t", "r": "\r", "0": "\0",
                    "\\": "\\", "'": "'", '"': '"',
                    "a": "\a", "b": "\b", "f": "\f", "v": "\v",
                }
                buf.append(mapping.get(esc, esc))
            elif ch == quote:
                self._advance()
                break
            elif ch == "\n":
                raise LexerError("Unterminated string literal", pos, self.filename)
            else:
                buf.append(self._advance())

        tt = TT.FSTRING if is_f else TT.STRING
        return Token(tt, "".join(buf), pos)

    def _read_triple_string(self, quote: str) -> Token:
        pos = self._here()
        for _ in range(3):
            self._advance()
        buf = []
        while self._pos < self._len:
            if (self._ch(0) == quote and
                    self._ch(1) == quote and
                    self._ch(2) == quote):
                for _ in range(3):
                    self._advance()
                break
            buf.append(self._advance())
        return Token(TT.STRING, "".join(buf), pos)

    # ── numbers ──────────────────────────────────────────────────────────────

    def _read_number(self) -> Token:
        pos      = self._here()
        buf      = []
        is_float = False

        # hex / bin / oct
        if self._ch() == "0":
            buf.append(self._advance())
            nxt = self._ch().lower()
            if nxt == "x":
                buf.append(self._advance())
                while self._ch() and self._ch() in "0123456789abcdefABCDEF_":
                    buf.append(self._advance())
                return Token(TT.NUMBER, "".join(buf), pos)
            elif nxt == "b":
                buf.append(self._advance())
                while self._ch() in "01_":
                    buf.append(self._advance())
                return Token(TT.NUMBER, "".join(buf), pos)
            elif nxt == "o":
                buf.append(self._advance())
                while self._ch() in "01234567_":
                    buf.append(self._advance())
                return Token(TT.NUMBER, "".join(buf), pos)

        while self._ch() and (self._ch().isdigit() or self._ch() == "_"):
            buf.append(self._advance())

        if self._ch() == "." and self._ch(1).isdigit():
            is_float = True
            buf.append(self._advance())
            while self._ch() and (self._ch().isdigit() or self._ch() == "_"):
                buf.append(self._advance())

        if self._ch().lower() == "e":
            is_float = True
            buf.append(self._advance())
            if self._ch() in ("+", "-"):
                buf.append(self._advance())
            while self._ch() and self._ch().isdigit():
                buf.append(self._advance())

        tt = TT.FLOAT if is_float else TT.NUMBER
        return Token(tt, "".join(buf), pos)

    # ── identifiers / keywords ───────────────────────────────────────────────

    def _read_ident(self) -> Token:
        pos = self._here()
        buf = []
        while self._ch() and (self._ch().isalnum() or self._ch() == "_"):
            buf.append(self._advance())
        word  = "".join(buf)
        upper = word.upper()

        # Keywords are UPPERCASE only — mixed/lowercase words are identifiers.
        # This lets users have variables named 'pi', 'e', 'min', etc.
        if word == word.upper() or word.upper() in ("TRUE","FALSE","NULL","NONE","AND","OR","NOT","IS","IN"):
            if upper == "TRUE":
                return Token(TT.BOOL, "True", pos)
            if upper == "FALSE":
                return Token(TT.BOOL, "False", pos)
            if upper in ("NULL", "NONE"):
                return Token(TT.NULL, "null", pos)
            if upper in FLUX_KEYWORDS:
                return Token(TT.KEYWORD, upper, pos)
        return Token(TT.IDENT, word, pos)

    # ── comments ─────────────────────────────────────────────────────────────

    def _read_line_comment(self) -> Token:
        pos = self._here()
        self._advance()   # consume '#'
        buf = []
        while self._pos < self._len and self._ch() != "\n":
            buf.append(self._advance())
        return Token(TT.COMMENT, "".join(buf).strip(), pos)

    def _read_block_comment(self) -> Token:
        pos = self._here()
        self._advance(); self._advance()   # consume /*
        buf = []
        while self._pos < self._len:
            if self._ch() == "*" and self._ch(1) == "/":
                self._advance(); self._advance()
                break
            buf.append(self._advance())
        return Token(TT.MULTICOMMENT, "".join(buf).strip(), pos)

    # ── main tokenise loop ───────────────────────────────────────────────────

    def tokenize(self) -> list[Token]:
        while self._pos < self._len:
            self._skip_spaces()
            if self._pos >= self._len:
                break

            pos = self._here()
            ch  = self._ch()

            # newline
            if ch == "\n":
                self._emit(TT.NEWLINE, "\\n", pos)
                self._advance()
                continue

            # line comment
            if ch == "#":
                self._tokens.append(self._read_line_comment())
                continue

            # block comment  /* ... */
            if ch == "/" and self._ch(1) == "*":
                self._tokens.append(self._read_block_comment())
                continue

            # string literals
            if ch in ('"', "'"):
                if self._ch(1) == ch and self._ch(2) == ch:
                    self._tokens.append(self._read_triple_string(ch))
                else:
                    self._tokens.append(self._read_string())
                continue

            # numbers
            if ch.isdigit():
                self._tokens.append(self._read_number())
                continue

            # identifiers / keywords
            if ch.isalpha() or ch == "_":
                self._tokens.append(self._read_ident())
                continue

            # two-char operators (checked before single-char)
            two = ch + self._ch(1)

            _two_map: dict[str, TT] = {
                "->": TT.ARROW,       "=>": TT.FAT_ARROW,
                "==": TT.EQEQ,        "!=": TT.NEQ,
                "<=": TT.LTE,         ">=": TT.GTE,
                "+=": TT.PLUS_EQ,     "-=": TT.MINUS_EQ,
                "*=": TT.STAR_EQ,     "/=": TT.SLASH_EQ,
                "%=": TT.PERCENT_EQ,  "**": TT.STARSTAR,
                "//": TT.DOUBLESLASH, "<<": TT.LSHIFT,
                ">>": TT.RSHIFT,
            }
            if two in _two_map:
                self._emit(_two_map[two], two, pos)
                self._advance(); self._advance()
                continue

            # triple dot
            if ch == "." and self._ch(1) == "." and self._ch(2) == ".":
                self._emit(TT.DOTDOTDOT, "...", pos)
                self._advance(); self._advance(); self._advance()
                continue

            # double dot
            if ch == "." and self._ch(1) == ".":
                self._emit(TT.DOTDOT, "..", pos)
                self._advance(); self._advance()
                continue

            # single-char tokens
            _single_map: dict[str, TT] = {
                "{": TT.LBRACE,    "}": TT.RBRACE,
                "(": TT.LPAREN,    ")": TT.RPAREN,
                "[": TT.LBRACKET,  "]": TT.RBRACKET,
                ",": TT.COMMA,     ":": TT.COLON,
                ";": TT.SEMICOLON, ".": TT.DOT,
                "=": TT.EQUALS,    "<": TT.LT,
                ">": TT.GT,        "+": TT.PLUS,
                "-": TT.MINUS,     "*": TT.STAR,
                "/": TT.SLASH,     "%": TT.PERCENT,
                "&": TT.AMPERSAND, "|": TT.PIPE,
                "^": TT.CARET,     "~": TT.TILDE,
                "!": TT.BANG,      "?": TT.QUESTION,
                "@": TT.AT,
            }
            if ch in _single_map:
                self._emit(_single_map[ch], ch, pos)
                self._advance()
                continue

            raise LexerError(f"Unexpected character: {ch!r}", pos, self.filename)

        self._emit(TT.EOF, "", self._here())
        return self._tokens


# =============================================================================
# TOKEN STREAM  — cursor-based wrapper used by ALL parser files
# =============================================================================

class TokenStream:
    """
    Wraps a flat token list and provides cursor-based navigation.
    All parser files import and use this — never index raw lists directly.
    Comments are stripped by default; newlines are kept for statement parsing.
    """

    def __init__(self, tokens: list[Token], skip_comments: bool = True):
        if skip_comments:
            self._tokens = [t for t in tokens
                            if t.type not in (TT.COMMENT, TT.MULTICOMMENT)]
        else:
            self._tokens = list(tokens)
        self._pos = 0

    # ── navigation ──────────────────────────────────────────────────────────

    def peek(self, offset: int = 0) -> Token:
        """Look ahead without consuming. Returns EOF if past end."""
        idx = self._pos + offset
        if idx < len(self._tokens):
            return self._tokens[idx]
        return self._tokens[-1]   # always EOF

    def current(self) -> Token:
        return self.peek(0)

    def advance(self) -> Token:
        """Consume and return current token."""
        tok = self._tokens[self._pos]
        if self._pos < len(self._tokens) - 1:
            self._pos += 1
        return tok

    # ── expect / match helpers ───────────────────────────────────────────────

    def expect(self, tt: TT, value: str = None) -> Token:
        """
        Consume current token.
        Raises ParseError (imported lazily) on type or value mismatch.
        """
        tok = self.current()
        if tok.type is not tt:
            from parser import ParseError
            raise ParseError(
                f"Expected {tt.name} but got {tok.type.name}({tok.value!r})",
                tok.pos
            )
        if value is not None and tok.value.upper() != value.upper():
            from parser import ParseError
            raise ParseError(
                f"Expected value {value!r} but got {tok.value!r}",
                tok.pos
            )
        return self.advance()

    def expect_kw(self, *words: str) -> Token:
        """Consume a KEYWORD token matching one of the given words."""
        tok = self.current()
        if tok.type is not TT.KEYWORD or tok.value.upper() not in {w.upper() for w in words}:
            from parser import ParseError
            raise ParseError(
                f"Expected keyword {words} but got {tok.type.name}({tok.value!r})",
                tok.pos
            )
        return self.advance()

    def expect_ident(self) -> Token:
        """Consume an IDENT token."""
        return self.expect(TT.IDENT)

    def expect_string(self) -> Token:
        """Consume a STRING or FSTRING token."""
        tok = self.current()
        if tok.type not in (TT.STRING, TT.FSTRING):
            from parser_core import ParseError
            raise ParseError(
                f"Expected string literal but got {tok.type.name}({tok.value!r})",
                tok.pos
            )
        return self.advance()

    def match(self, tt: TT, value: str = None) -> bool:
        """Return True and consume if current token matches type (and optional value)."""
        tok = self.current()
        if tok.type is not tt:
            return False
        if value is not None and tok.value.upper() != value.upper():
            return False
        self.advance()
        return True

    def match_kw(self, *words: str) -> bool:
        """Return True and consume if current is a KEYWORD matching any word."""
        tok = self.current()
        if tok.type is TT.KEYWORD and tok.value.upper() in {w.upper() for w in words}:
            self.advance()
            return True
        return False

    def match_any(self, *types: TT) -> Optional[Token]:
        """Return and consume current token if its type is in types, else None."""
        if self.current().type in types:
            return self.advance()
        return None

    # ── newline handling ─────────────────────────────────────────────────────

    def skip_newlines(self):
        """Consume all consecutive NEWLINE tokens."""
        while self.current().type is TT.NEWLINE:
            self.advance()

    def skip_newlines_and_semis(self):
        """Consume NEWLINEs and SEMICOLONs (statement terminators)."""
        while self.current().type in (TT.NEWLINE, TT.SEMICOLON):
            self.advance()

    # ── state management ────────────────────────────────────────────────────

    def save(self) -> int:
        """Save cursor position for backtracking."""
        return self._pos

    def restore(self, pos: int):
        """Restore cursor to a previously saved position."""
        self._pos = pos

    def is_eof(self) -> bool:
        return self.current().type is TT.EOF

    def remaining_count(self) -> int:
        return len(self._tokens) - self._pos

    def remaining_tokens(self) -> list[Token]:
        return self._tokens[self._pos:]

    def all_tokens(self) -> list[Token]:
        return list(self._tokens)

    def __len__(self) -> int:
        return len(self._tokens)

    def __repr__(self) -> str:
        return (f"TokenStream(pos={self._pos}/{len(self._tokens)}, "
                f"current={self.current()!r})")


# =============================================================================
# KEYWORD CLASSIFICATION HELPERS  (used by all parser files)
# =============================================================================

def is_widget_kw(tok: Token) -> bool:
    return tok.type is TT.KEYWORD and tok.value.upper() in WIDGET_KEYWORDS

def is_event_kw(tok: Token) -> bool:
    return tok.type is TT.KEYWORD and tok.value.upper() in EVENT_KEYWORDS

def is_graph_kw(tok: Token) -> bool:
    return tok.type is TT.KEYWORD and tok.value.upper() in GRAPH_KEYWORDS

def is_control_flow_kw(tok: Token) -> bool:
    return tok.type is TT.KEYWORD and tok.value.upper() in CONTROL_FLOW_KEYWORDS

def is_literal_tok(tok: Token) -> bool:
    return tok.type in (TT.STRING, TT.FSTRING, TT.NUMBER, TT.FLOAT, TT.BOOL, TT.NULL)

def is_operator_tok(tok: Token) -> bool:
    return (tok.type in ARITHMETIC_TYPES | COMPARISON_TYPES or
            (tok.type is TT.KEYWORD and tok.value.upper() in OPERATOR_KEYWORDS))

def is_assign_tok(tok: Token) -> bool:
    return tok.type is TT.EQUALS or tok.type in ASSIGN_COMPOUND


# =============================================================================
# PUBLIC API
# =============================================================================

def lex(source: str, filename: str = "<stdin>") -> list[Token]:
    """Lex source text and return raw token list."""
    return FLUXLexer(source, filename).tokenize()


def lex_file(path: str) -> list[Token]:
    """Read a .flux file from disk and lex it."""
    with open(path, "r", encoding="utf-8") as fh:
        source = fh.read()
    return lex(source, path)


def make_stream(source: str, filename: str = "<stdin>",
                skip_comments: bool = True) -> TokenStream:
    """Lex source and return a TokenStream ready for parsing."""
    return TokenStream(lex(source, filename), skip_comments=skip_comments)


def make_stream_from_tokens(tokens: list[Token],
                             skip_comments: bool = True) -> TokenStream:
    """Wrap an already-lexed token list in a TokenStream."""
    return TokenStream(tokens, skip_comments=skip_comments)


def tokens_to_lines(tokens: list[Token]) -> list[list[Token]]:
    """Split flat token list into logical lines on NEWLINE boundaries."""
    lines: list[list[Token]] = []
    current: list[Token] = []
    for tok in tokens:
        if tok.type is TT.NEWLINE:
            if current:
                lines.append(current)
                current = []
        elif tok.type is not TT.EOF:
            current.append(tok)
    if current:
        lines.append(current)
    return lines


def strip_comments(tokens: list[Token]) -> list[Token]:
    return [t for t in tokens if t.type not in (TT.COMMENT, TT.MULTICOMMENT)]


def strip_newlines(tokens: list[Token]) -> list[Token]:
    return [t for t in tokens if t.type is not TT.NEWLINE]


def token_summary(tokens: list[Token], limit: int = 60) -> str:
    """Compact human-readable summary of a token list (for debugging)."""
    parts = []
    for t in tokens[:limit]:
        if t.type is TT.EOF:
            parts.append("EOF")
        elif t.type is TT.NEWLINE:
            parts.append("NL")
        else:
            parts.append(f"{t.type.name}({t.value!r})")
    if len(tokens) > limit:
        parts.append(f"...+{len(tokens)-limit}")
    return " ".join(parts)


# =============================================================================
# SELF-TEST
# =============================================================================
if __name__ == "__main__":
    _sample = '''
# FLUX self-test
APP "My App" SIZE 800 600

BUTTON btn1 "Click Me" X 100 Y 200 WIDTH 120 HEIGHT 35 {
    ONCLICK -> PRINT "Hello World"
    STYLE BG "#1a1a2e" RADIUS 8
}

VAR counter = 0
FUNC increment() {
    SET counter = counter + 1
    IF counter > 10 {
        ALERT "Title" "Limit reached"
    }
}

LINE_PLOT [1,2,3,4,5] [10,20,15,30,25] TITLE "Sales"
'''
    try:
        toks = lex(_sample, "test.flux")
        print(f"OK — {len(toks)} tokens")
        for t in toks[:40]:
            print(f"  {t}")
        if len(toks) > 40:
            print(f"  ... +{len(toks)-40} more")

        # verify enum safety — this would be a NameError with string constants
        assert TT.PLUS is TT.PLUS
        assert TT.PLUS is not TT.MINUS
        print("Enum identity checks passed.")

        stream = make_stream(_sample, "test.flux")
        print(f"Stream: {stream}")
    except LexerError as e:
        print(f"LEXER ERROR: {e}")
