"""
=============================================================================
FLUX LANGUAGE  —  AST NODE DEFINITIONS                       parser_ast.py
=============================================================================
Every node in the FLUX Abstract Syntax Tree is defined here.
No parsing logic lives here — only data structures and the visitor base.

Rule enforced throughout:  Expressions != Statements
  • ExprNode  — produces a value, can appear on the right of =
  • StmtNode  — performs an action, cannot be used as a value
=============================================================================
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Tuple
from tokenizer import SourcePos


# =============================================================================
# BASE CLASSES
# =============================================================================

class ASTNode:
    """Root of every AST node."""
    pos: SourcePos = field(default_factory=SourcePos)

    def accept(self, visitor: "ASTVisitor") -> Any:
        method = "visit_" + type(self).__name__
        fn = getattr(visitor, method, visitor.generic_visit)
        return fn(self)

    def __repr__(self) -> str:
        fields = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        body   = ", ".join(f"{k}={v!r}" for k, v in fields.items())
        return f"{type(self).__name__}({body})"


@dataclass
class ExprNode(ASTNode):
    """Base for all expression nodes — nodes that produce a value."""
    pos: SourcePos = field(default_factory=SourcePos)


@dataclass
class StmtNode(ASTNode):
    """Base for all statement nodes — nodes that perform an action."""
    pos: SourcePos = field(default_factory=SourcePos)


# =============================================================================
# PROGRAM ROOT
# =============================================================================

@dataclass
class ProgramNode(ASTNode):
    """Root node of a parsed FLUX file."""
    body:     List[StmtNode] = field(default_factory=list)
    filename: str            = "<stdin>"
    pos:      SourcePos      = field(default_factory=SourcePos)


# =============================================================================
# ── EXPRESSION NODES ─────────────────────────────────────────────────────────
# =============================================================================

@dataclass
class NumberLiteralExpr(ExprNode):
    value: float = 0.0
    raw:   str   = "0"

@dataclass
class StringLiteralExpr(ExprNode):
    value:    str  = ""
    is_fstr:  bool = False

@dataclass
class BoolLiteralExpr(ExprNode):
    value: bool = True

@dataclass
class NullLiteralExpr(ExprNode):
    pass

@dataclass
class IdentExpr(ExprNode):
    """A bare identifier used as a value: myVar, counter, etc."""
    name: str = ""

@dataclass
class ListExpr(ExprNode):
    """[a, b, c]"""
    elements: List[ExprNode] = field(default_factory=list)

@dataclass
class DictExpr(ExprNode):
    """{key: value, ...}"""
    pairs: List[Tuple[ExprNode, ExprNode]] = field(default_factory=list)

@dataclass
class TupleExpr(ExprNode):
    """(a, b, c)"""
    elements: List[ExprNode] = field(default_factory=list)

@dataclass
class IndexExpr(ExprNode):
    """obj[index]"""
    obj:   ExprNode = field(default_factory=lambda: NullLiteralExpr())
    index: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class SliceExpr(ExprNode):
    """obj[start:stop:step]"""
    obj:   ExprNode          = field(default_factory=lambda: NullLiteralExpr())
    start: Optional[ExprNode] = None
    stop:  Optional[ExprNode] = None
    step:  Optional[ExprNode] = None

@dataclass
class MemberExpr(ExprNode):
    """obj.member"""
    obj:    ExprNode = field(default_factory=lambda: NullLiteralExpr())
    member: str      = ""

@dataclass
class CallExpr(ExprNode):
    """func(arg1, arg2, key=val)"""
    callee:   ExprNode              = field(default_factory=lambda: NullLiteralExpr())
    args:     List[ExprNode]        = field(default_factory=list)
    kwargs:   Dict[str, ExprNode]   = field(default_factory=dict)

@dataclass
class BinaryExpr(ExprNode):
    """left OP right"""
    left:  ExprNode = field(default_factory=lambda: NullLiteralExpr())
    op:    str      = "+"
    right: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class UnaryExpr(ExprNode):
    """OP operand  (NOT, -, ~)"""
    op:      str     = "-"
    operand: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class TernaryExpr(ExprNode):
    """condition ? then_expr : else_expr"""
    condition: ExprNode = field(default_factory=lambda: NullLiteralExpr())
    then_expr: ExprNode = field(default_factory=lambda: NullLiteralExpr())
    else_expr: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class LambdaExpr(ExprNode):
    """LAMBDA (params) => expr"""
    params: List[str]  = field(default_factory=list)
    body:   ExprNode   = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class AwaitExpr(ExprNode):
    """AWAIT expr"""
    expr: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class SpreadExpr(ExprNode):
    """...expr"""
    expr: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class TypeofExpr(ExprNode):
    """TYPEOF expr"""
    expr: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class RangeExpr(ExprNode):
    """RANGE(start, stop, step)"""
    start: ExprNode           = field(default_factory=lambda: NullLiteralExpr())
    stop:  ExprNode           = field(default_factory=lambda: NullLiteralExpr())
    step:  Optional[ExprNode] = None

@dataclass
class InterpolatedStringExpr(ExprNode):
    """f"Hello {name}" — parts are alternating str and ExprNode."""
    parts: List[Any] = field(default_factory=list)   # str | ExprNode


# =============================================================================
# ── STATEMENT NODES ──────────────────────────────────────────────────────────
# =============================================================================

# ── Variable declarations ────────────────────────────────────────────────────

@dataclass
class VarDeclStmt(StmtNode):
    """VAR / LET / CONST name = expr"""
    kind:  str            = "VAR"   # VAR | LET | CONST
    name:  str            = ""
    value: Optional[ExprNode] = None
    type_hint: Optional[str]  = None

@dataclass
class AssignStmt(StmtNode):
    """SET name = expr  or  name = expr  or  name += expr"""
    target: ExprNode = field(default_factory=lambda: NullLiteralExpr())
    op:     str      = "="
    value:  ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class DeleteStmt(StmtNode):
    """DEL name"""
    name: str = ""

# ── Control flow ─────────────────────────────────────────────────────────────

@dataclass
class IfStmt(StmtNode):
    """IF cond { body } ELIF cond { body } ELSE { body }"""
    condition:   ExprNode          = field(default_factory=lambda: NullLiteralExpr())
    body:        List[StmtNode]    = field(default_factory=list)
    elif_clauses: List[Tuple[ExprNode, List[StmtNode]]] = field(default_factory=list)
    else_body:   Optional[List[StmtNode]] = None

@dataclass
class WhileStmt(StmtNode):
    """WHILE cond { body }"""
    condition: ExprNode       = field(default_factory=lambda: NullLiteralExpr())
    body:      List[StmtNode] = field(default_factory=list)

@dataclass
class ForStmt(StmtNode):
    """FOR var IN iterable { body }"""
    var:      str             = ""
    iterable: ExprNode        = field(default_factory=lambda: NullLiteralExpr())
    body:     List[StmtNode]  = field(default_factory=list)

@dataclass
class BreakStmt(StmtNode):
    pass

@dataclass
class ContinueStmt(StmtNode):
    pass

@dataclass
class ReturnStmt(StmtNode):
    value: Optional[ExprNode] = None

@dataclass
class PassStmt(StmtNode):
    pass

@dataclass
class YieldStmt(StmtNode):
    value: Optional[ExprNode] = None

@dataclass
class MatchStmt(StmtNode):
    """MATCH expr { CASE val { body } ... DEFAULT { body } }"""
    subject: ExprNode = field(default_factory=lambda: NullLiteralExpr())
    cases:   List[Tuple[Optional[ExprNode], List[StmtNode]]] = field(default_factory=list)

@dataclass
class TryCatchStmt(StmtNode):
    """TRY { body } CATCH name { handler } FINALLY { cleanup }"""
    body:        List[StmtNode]           = field(default_factory=list)
    catch_var:   Optional[str]            = None
    catch_body:  Optional[List[StmtNode]] = None
    finally_body: Optional[List[StmtNode]] = None

@dataclass
class ThrowStmt(StmtNode):
    value: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class AssertStmt(StmtNode):
    condition: ExprNode           = field(default_factory=lambda: NullLiteralExpr())
    message:   Optional[ExprNode] = None

# ── Functions ────────────────────────────────────────────────────────────────

@dataclass
class ParamDef:
    """A single function parameter."""
    name:     str
    default:  Optional[ExprNode] = None
    type_hint: Optional[str]     = None
    variadic: bool               = False   # *args
    keyword:  bool               = False   # **kwargs

@dataclass
class FuncDefStmt(StmtNode):
    """FUNC name(params) { body }"""
    name:      str            = ""
    params:    List[ParamDef] = field(default_factory=list)
    body:      List[StmtNode] = field(default_factory=list)
    is_async:  bool           = False
    return_type: Optional[str] = None

@dataclass
class CallStmt(StmtNode):
    """CALL funcname(args)  — statement form of a call."""
    call_expr: CallExpr = field(default_factory=lambda: CallExpr())

@dataclass
class ExprStmt(StmtNode):
    """A bare expression used as a statement (e.g. function call)."""
    expr: ExprNode = field(default_factory=lambda: NullLiteralExpr())

# ── Output / dialogs ─────────────────────────────────────────────────────────

@dataclass
class PrintStmt(StmtNode):
    args: List[ExprNode] = field(default_factory=list)

@dataclass
class AlertStmt(StmtNode):
    title:   ExprNode = field(default_factory=lambda: NullLiteralExpr())
    message: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class ErrorDialogStmt(StmtNode):
    title:   ExprNode = field(default_factory=lambda: NullLiteralExpr())
    message: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class ConfirmStmt(StmtNode):
    title:   ExprNode = field(default_factory=lambda: NullLiteralExpr())
    message: ExprNode = field(default_factory=lambda: NullLiteralExpr())
    result_var: Optional[str] = None

@dataclass
class PromptStmt(StmtNode):
    message:    ExprNode      = field(default_factory=lambda: NullLiteralExpr())
    result_var: Optional[str] = None

@dataclass
class LogStmt(StmtNode):
    level: str            = "INFO"
    args:  List[ExprNode] = field(default_factory=list)

# ── Import / include ─────────────────────────────────────────────────────────

@dataclass
class ImportStmt(StmtNode):
    path:  str           = ""
    alias: Optional[str] = None

@dataclass
class IncludeStmt(StmtNode):
    path: str = ""

# ── Timing ───────────────────────────────────────────────────────────────────

@dataclass
class WaitStmt(StmtNode):
    seconds: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class AfterStmt(StmtNode):
    seconds: ExprNode       = field(default_factory=lambda: NullLiteralExpr())
    body:    List[StmtNode] = field(default_factory=list)

@dataclass
class LoopStmt(StmtNode):
    """LOOP { body } — infinite loop with optional delay."""
    body:  List[StmtNode]     = field(default_factory=list)
    delay: Optional[ExprNode] = None

@dataclass
class TimerStmt(StmtNode):
    name:     str             = ""
    interval: ExprNode        = field(default_factory=lambda: NullLiteralExpr())
    body:     List[StmtNode]  = field(default_factory=list)
    repeat:   bool            = False

@dataclass
class ScheduleStmt(StmtNode):
    hour:   ExprNode       = field(default_factory=lambda: NullLiteralExpr())
    minute: ExprNode       = field(default_factory=lambda: NullLiteralExpr())
    body:   List[StmtNode] = field(default_factory=list)

# ── File / IO ────────────────────────────────────────────────────────────────

@dataclass
class WriteFileStmt(StmtNode):
    path:    ExprNode = field(default_factory=lambda: NullLiteralExpr())
    content: ExprNode = field(default_factory=lambda: NullLiteralExpr())
    mode:    str      = "w"

@dataclass
class ReadFileStmt(StmtNode):
    path:       ExprNode      = field(default_factory=lambda: NullLiteralExpr())
    result_var: Optional[str] = None

@dataclass
class DeleteFileStmt(StmtNode):
    path: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class MakeDirStmt(StmtNode):
    path: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class OrganizeFolderStmt(StmtNode):
    path: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class WatchFileStmt(StmtNode):
    path: ExprNode       = field(default_factory=lambda: NullLiteralExpr())
    body: List[StmtNode] = field(default_factory=list)

# ── Audio ────────────────────────────────────────────────────────────────────

@dataclass
class AudioStmt(StmtNode):
    file:   ExprNode = field(default_factory=lambda: NullLiteralExpr())
    loop:   bool     = False
    volume: Optional[ExprNode] = None

@dataclass
class AudioStopStmt(StmtNode):
    pass

@dataclass
class AudioPauseStmt(StmtNode):
    pass

@dataclass
class AudioResumeStmt(StmtNode):
    pass

@dataclass
class AudioVolumeStmt(StmtNode):
    level: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class AudioSeekStmt(StmtNode):
    position: ExprNode = field(default_factory=lambda: NullLiteralExpr())

# ── Video ────────────────────────────────────────────────────────────────────

@dataclass
class VideoStmt(StmtNode):
    file:        ExprNode = field(default_factory=lambda: NullLiteralExpr())
    window_name: Optional[ExprNode] = None
    loop:        bool     = False

@dataclass
class VideoStopStmt(StmtNode):
    pass

@dataclass
class VideoPauseStmt(StmtNode):
    pass

@dataclass
class VideoResumeStmt(StmtNode):
    pass

@dataclass
class VideoSeekStmt(StmtNode):
    position: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class VideoVolumeStmt(StmtNode):
    level: ExprNode = field(default_factory=lambda: NullLiteralExpr())

# ── Clipboard ────────────────────────────────────────────────────────────────

@dataclass
class CopyStmt(StmtNode):
    value: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class PasteStmt(StmtNode):
    result_var: Optional[str] = None

# ── System ───────────────────────────────────────────────────────────────────

@dataclass
class SysExitStmt(StmtNode):
    code: Optional[ExprNode] = None

@dataclass
class SysExecStmt(StmtNode):
    command: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class SysNotifyStmt(StmtNode):
    title:   ExprNode = field(default_factory=lambda: NullLiteralExpr())
    message: ExprNode = field(default_factory=lambda: NullLiteralExpr())

# ── Network ──────────────────────────────────────────────────────────────────

@dataclass
class HttpRequestStmt(StmtNode):
    method:     str            = "GET"
    url:        ExprNode       = field(default_factory=lambda: NullLiteralExpr())
    headers:    Optional[ExprNode] = None
    body_data:  Optional[ExprNode] = None
    result_var: Optional[str]  = None

@dataclass
class DownloadStmt(StmtNode):
    url:  ExprNode = field(default_factory=lambda: NullLiteralExpr())
    dest: ExprNode = field(default_factory=lambda: NullLiteralExpr())

@dataclass
class UploadStmt(StmtNode):
    url:  ExprNode = field(default_factory=lambda: NullLiteralExpr())
    file: ExprNode = field(default_factory=lambda: NullLiteralExpr())
