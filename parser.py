"""
=============================================================================
FLUX LANGUAGE  —  MAIN PARSER PIPELINE                          parser.py
=============================================================================
Connects tokenizer → AST → engine execution.
Imports the new enum-based tokenizer correctly.
Expressions != Statements enforced throughout.
=============================================================================
"""
from __future__ import annotations
import re
from typing import List, Optional, Any, Dict

from tokenizer import (
    TT, Token, SourcePos, TokenStream,
    lex, make_stream, is_widget_kw, is_event_kw, is_graph_kw,
    WIDGET_KEYWORDS, EVENT_KEYWORDS, GRAPH_KEYWORDS,
)
from parser_ast import (
    # expressions
    ExprNode, NumberLiteralExpr, StringLiteralExpr, BoolLiteralExpr,
    NullLiteralExpr, IdentExpr, ListExpr, BinaryExpr, UnaryExpr,
    CallExpr, MemberExpr, IndexExpr,
    # statements
    StmtNode, ProgramNode, VarDeclStmt, AssignStmt, PrintStmt,
    AlertStmt, ErrorDialogStmt, ConfirmStmt, IfStmt, WhileStmt,
    ForStmt, BreakStmt, ContinueStmt, ReturnStmt, FuncDefStmt,
    ParamDef, CallStmt, ExprStmt, WaitStmt, AfterStmt, LoopStmt,
    AudioStmt, AudioStopStmt, VideoStmt, WriteFileStmt, ReadFileStmt,
    CopyStmt, PasteStmt, ImportStmt, LogStmt, TryCatchStmt, ThrowStmt,
    AssertStmt, DeleteStmt, TimerStmt, ScheduleStmt,
)


# =============================================================================
# PARSE ERROR
# =============================================================================

class ParseError(Exception):
    def __init__(self, msg: str, pos: SourcePos, filename: str = "<stdin>"):
        super().__init__(f"[PARSE] {filename} {pos}: {msg}")
        self.pos      = pos
        self.filename = filename


# =============================================================================
# EXPRESSION PARSER
# Expressions produce a value. They NEVER appear as standalone statements
# except when wrapped in ExprStmt.
# Precedence (low → high):
#   OR → AND → NOT → comparison → add/sub → mul/div → unary → postfix → primary
# =============================================================================

class ExpressionParser:
    """
    Recursive-descent expression parser.
    Receives a TokenStream already positioned at the start of an expression.
    """

    def __init__(self, stream: TokenStream, filename: str = "<stdin>"):
        self.s        = stream
        self.filename = filename

    def _err(self, msg: str) -> ParseError:
        return ParseError(msg, self.s.current().pos, self.filename)

    # ── entry point ─────────────────────────────────────────────────────────

    def parse(self) -> ExprNode:
        return self._or_expr()

    # ── OR ──────────────────────────────────────────────────────────────────

    def _or_expr(self) -> ExprNode:
        left = self._and_expr()
        while self.s.current().is_kw("OR"):
            pos = self.s.current().pos
            self.s.advance()
            right = self._and_expr()
            left  = BinaryExpr(pos=pos, left=left, op="OR", right=right)
        return left

    # ── AND ─────────────────────────────────────────────────────────────────

    def _and_expr(self) -> ExprNode:
        left = self._not_expr()
        while self.s.current().is_kw("AND"):
            pos = self.s.current().pos
            self.s.advance()
            right = self._not_expr()
            left  = BinaryExpr(pos=pos, left=left, op="AND", right=right)
        return left

    # ── NOT ─────────────────────────────────────────────────────────────────

    def _not_expr(self) -> ExprNode:
        if self.s.current().is_kw("NOT"):
            pos = self.s.current().pos
            self.s.advance()
            return UnaryExpr(pos=pos, op="NOT", operand=self._not_expr())
        return self._comparison()

    # ── COMPARISON ──────────────────────────────────────────────────────────

    _CMP_OPS = {TT.EQEQ, TT.NEQ, TT.LT, TT.GT, TT.LTE, TT.GTE}

    def _comparison(self) -> ExprNode:
        left = self._add_sub()
        while self.s.current().type in self._CMP_OPS or \
              self.s.current().is_kw("IS", "IN"):
            pos = self.s.current().pos
            op  = self.s.advance().value
            right = self._add_sub()
            left  = BinaryExpr(pos=pos, left=left, op=op, right=right)
        return left

    # ── ADD / SUB ───────────────────────────────────────────────────────────

    def _add_sub(self) -> ExprNode:
        left = self._mul_div()
        while self.s.current().type in (TT.PLUS, TT.MINUS):
            pos = self.s.current().pos
            op  = self.s.advance().value
            right = self._mul_div()
            left  = BinaryExpr(pos=pos, left=left, op=op, right=right)
        return left

    # ── MUL / DIV / MOD ─────────────────────────────────────────────────────

    def _mul_div(self) -> ExprNode:
        left = self._unary()
        while self.s.current().type in (TT.STAR, TT.SLASH,
                                         TT.PERCENT, TT.STARSTAR,
                                         TT.DOUBLESLASH):
            pos = self.s.current().pos
            op  = self.s.advance().value
            right = self._unary()
            left  = BinaryExpr(pos=pos, left=left, op=op, right=right)
        return left

    # ── UNARY ────────────────────────────────────────────────────────────────

    def _unary(self) -> ExprNode:
        tok = self.s.current()
        if tok.type is TT.MINUS:
            pos = tok.pos; self.s.advance()
            return UnaryExpr(pos=pos, op="-", operand=self._unary())
        if tok.type is TT.BANG:
            pos = tok.pos; self.s.advance()
            return UnaryExpr(pos=pos, op="!", operand=self._unary())
        if tok.type is TT.TILDE:
            pos = tok.pos; self.s.advance()
            return UnaryExpr(pos=pos, op="~", operand=self._unary())
        return self._postfix()

    # ── POSTFIX  (call, index, member) ───────────────────────────────────────

    def _postfix(self) -> ExprNode:
        expr = self._primary()
        while True:
            tok = self.s.current()
            # function call  expr(...)
            if tok.type is TT.LPAREN:
                pos = tok.pos
                self.s.advance()
                args, kwargs = self._parse_call_args()
                self.s.expect(TT.RPAREN)
                expr = CallExpr(pos=pos, callee=expr, args=args, kwargs=kwargs)
            # index  expr[...]
            elif tok.type is TT.LBRACKET:
                pos = tok.pos
                self.s.advance()
                idx = self.parse()
                self.s.expect(TT.RBRACKET)
                expr = IndexExpr(pos=pos, obj=expr, index=idx)
            # member  expr.name
            elif tok.type is TT.DOT:
                pos = tok.pos
                self.s.advance()
                member = self.s.expect(TT.IDENT).value
                expr = MemberExpr(pos=pos, obj=expr, member=member)
            else:
                break
        return expr

    def _parse_call_args(self):
        args   = []
        kwargs = {}
        self.s.skip_newlines()
        while not self.s.current().is_tt(TT.RPAREN, TT.EOF):
            # keyword arg:  name = expr
            if (self.s.current().type is TT.IDENT and
                    self.s.peek(1).type is TT.EQUALS):
                key = self.s.advance().value
                self.s.advance()   # consume =
                kwargs[key] = self.parse()
            else:
                args.append(self.parse())
            self.s.skip_newlines()
            if not self.s.match(TT.COMMA):
                break
            self.s.skip_newlines()
        return args, kwargs

    # ── PRIMARY ──────────────────────────────────────────────────────────────

    def _primary(self) -> ExprNode:
        tok = self.s.current()
        pos = tok.pos

        # number
        if tok.type is TT.NUMBER:
            self.s.advance()
            return NumberLiteralExpr(pos=pos, value=int(tok.value, 0), raw=tok.value)

        # float
        if tok.type is TT.FLOAT:
            self.s.advance()
            return NumberLiteralExpr(pos=pos, value=float(tok.value), raw=tok.value)

        # string / fstring
        if tok.type in (TT.STRING, TT.FSTRING):
            self.s.advance()
            return StringLiteralExpr(pos=pos, value=tok.value,
                                     is_fstr=(tok.type is TT.FSTRING))

        # bool
        if tok.type is TT.BOOL:
            self.s.advance()
            return BoolLiteralExpr(pos=pos, value=(tok.value == "True"))

        # null
        if tok.type is TT.NULL:
            self.s.advance()
            return NullLiteralExpr(pos=pos)

        # identifier
        if tok.type is TT.IDENT:
            self.s.advance()
            return IdentExpr(pos=pos, name=tok.value)

        # keyword used as identifier (e.g. GET, SET used in expressions)
        if tok.type is TT.KEYWORD and tok.value.upper() in (
                "GET", "TRUE", "FALSE", "NULL"):
            self.s.advance()
            if tok.value.upper() == "GET":
                return IdentExpr(pos=pos, name=tok.value)
            if tok.value.upper() == "TRUE":
                return BoolLiteralExpr(pos=pos, value=True)
            if tok.value.upper() == "FALSE":
                return BoolLiteralExpr(pos=pos, value=False)
            return NullLiteralExpr(pos=pos)

        # parenthesised expression
        if tok.type is TT.LPAREN:
            self.s.advance()
            self.s.skip_newlines()
            expr = self.parse()
            self.s.skip_newlines()
            self.s.expect(TT.RPAREN)
            return expr

        # list literal  [a, b, c]
        if tok.type is TT.LBRACKET:
            self.s.advance()
            elements = []
            self.s.skip_newlines()
            while not self.s.current().is_tt(TT.RBRACKET, TT.EOF):
                elements.append(self.parse())
                self.s.skip_newlines()
                if not self.s.match(TT.COMMA):
                    break
                self.s.skip_newlines()
            self.s.expect(TT.RBRACKET)
            return ListExpr(pos=pos, elements=elements)

        raise ParseError(
            f"Unexpected token in expression: {tok.type.name}({tok.value!r})",
            pos, self.filename
        )


# =============================================================================
# STATEMENT PARSER
# Statements perform actions. They never produce a value.
# Dispatches on the leading keyword of each line.
# =============================================================================

class StatementParser:

    def __init__(self, stream: TokenStream, filename: str = "<stdin>"):
        self.s        = stream
        self.filename = filename
        self._ep      = ExpressionParser(stream, filename)

    def _err(self, msg: str) -> ParseError:
        return ParseError(msg, self.s.current().pos, self.filename)

    def _expr(self) -> ExprNode:
        return self._ep.parse()

    # ── program root ────────────────────────────────────────────────────────

    def parse_program(self) -> ProgramNode:
        pos  = self.s.current().pos
        body = []
        self.s.skip_newlines()
        while not self.s.is_eof():
            stmt = self._parse_stmt()
            if stmt:
                body.append(stmt)
            self.s.skip_newlines_and_semis()
        return ProgramNode(pos=pos, body=body, filename=self.filename)

    # ── block  { stmts } ────────────────────────────────────────────────────

    def _parse_block(self) -> List[StmtNode]:
        self.s.expect(TT.LBRACE)
        self.s.skip_newlines()
        stmts = []
        while not self.s.current().is_tt(TT.RBRACE, TT.EOF):
            stmt = self._parse_stmt()
            if stmt:
                stmts.append(stmt)
            self.s.skip_newlines_and_semis()
        self.s.expect(TT.RBRACE)
        return stmts

    # ── main dispatch ────────────────────────────────────────────────────────

    def _parse_stmt(self) -> Optional[StmtNode]:
        self.s.skip_newlines()
        tok = self.s.current()

        if tok.type is TT.EOF:
            return None

        if tok.type is TT.KEYWORD:
            kw = tok.value.upper()

            # ── variable declarations ────────────────────────────────────────
            if kw in ("VAR", "LET", "CONST"):
                return self._parse_var_decl()

            # ── assignment ───────────────────────────────────────────────────
            if kw == "SET":
                return self._parse_set()

            # ── delete ───────────────────────────────────────────────────────
            if kw == "DEL":
                return self._parse_del()

            # ── control flow ─────────────────────────────────────────────────
            if kw == "IF":
                return self._parse_if()
            if kw == "WHILE":
                return self._parse_while()
            if kw == "FOR":
                return self._parse_for()
            if kw == "BREAK":
                self.s.advance()
                return BreakStmt(pos=tok.pos)
            if kw == "CONTINUE":
                self.s.advance()
                return ContinueStmt(pos=tok.pos)
            if kw == "RETURN":
                return self._parse_return()
            if kw == "PASS":
                self.s.advance()
                return None

            # ── functions ────────────────────────────────────────────────────
            if kw in ("FUNC", "ASYNC"):
                return self._parse_func()
            if kw == "CALL":
                return self._parse_call_stmt()

            # ── try/catch ────────────────────────────────────────────────────
            if kw == "TRY":
                return self._parse_try()
            if kw in ("THROW", "RAISE"):
                return self._parse_throw()
            if kw == "ASSERT":
                return self._parse_assert()

            # ── output / dialogs ─────────────────────────────────────────────
            if kw == "PRINT":
                return self._parse_print()
            if kw == "LOG":
                return self._parse_log()
            if kw == "ALERT":
                return self._parse_alert()
            if kw == "ERROR":
                return self._parse_error_dialog()
            if kw == "CONFIRM":
                return self._parse_confirm()

            # ── timing ───────────────────────────────────────────────────────
            if kw == "WAIT":
                return self._parse_wait()
            if kw == "AFTER":
                return self._parse_after()
            if kw == "LOOP":
                return self._parse_loop()
            if kw == "TIMER":
                return self._parse_timer()
            if kw == "SCHEDULE":
                return self._parse_schedule()

            # ── audio ────────────────────────────────────────────────────────
            if kw == "AUDIO":
                return self._parse_audio()
            if kw == "AUDIO_STOP":
                self.s.advance()
                return AudioStopStmt(pos=tok.pos)

            # ── video ────────────────────────────────────────────────────────
            if kw == "VIDEO":
                return self._parse_video()

            # ── file IO ──────────────────────────────────────────────────────
            if kw == "WRITE_FILE":
                return self._parse_write_file()
            if kw == "READ_FILE":
                return self._parse_read_file()

            # ── clipboard ────────────────────────────────────────────────────
            if kw == "COPY":
                return self._parse_copy()
            if kw == "PASTE":
                return self._parse_paste()

            # ── import ───────────────────────────────────────────────────────
            if kw in ("IMPORT", "INCLUDE"):
                return self._parse_import()

            # ── widgets (UI statements) ──────────────────────────────────────
            if kw in WIDGET_KEYWORDS:
                return self._parse_widget()

            # ── app / window ─────────────────────────────────────────────────
            if kw == "APP":
                return self._parse_app()

        # ── bare identifier assignment  name = expr ──────────────────────────
        if tok.type is TT.IDENT and self.s.peek(1).type in (
                TT.EQUALS, TT.PLUS_EQ, TT.MINUS_EQ,
                TT.STAR_EQ, TT.SLASH_EQ, TT.PERCENT_EQ):
            return self._parse_bare_assign()

        # ── bare expression statement (function call etc.) ───────────────────
        expr = self._expr()
        return ExprStmt(pos=expr.pos, expr=expr)

    # =========================================================================
    # INDIVIDUAL STATEMENT PARSERS
    # =========================================================================

    # ── VAR / LET / CONST name = expr ────────────────────────────────────────
    def _parse_var_decl(self) -> VarDeclStmt:
        pos  = self.s.current().pos
        kind = self.s.advance().value.upper()
        name = self.s.expect(TT.IDENT).value
        val  = None
        if self.s.match(TT.EQUALS):
            val = self._expr()
        return VarDeclStmt(pos=pos, kind=kind, name=name, value=val)

    # ── SET name op expr ─────────────────────────────────────────────────────
    def _parse_set(self) -> AssignStmt:
        pos = self.s.current().pos
        self.s.advance()   # consume SET
        target = self._expr()
        op_tok = self.s.current()
        if op_tok.type not in (TT.EQUALS, TT.PLUS_EQ, TT.MINUS_EQ,
                                TT.STAR_EQ, TT.SLASH_EQ, TT.PERCENT_EQ):
            raise self._err(f"Expected assignment operator, got {op_tok.value!r}")
        op = self.s.advance().value
        value = self._expr()
        return AssignStmt(pos=pos, target=target, op=op, value=value)

    # ── bare  name = expr ────────────────────────────────────────────────────
    def _parse_bare_assign(self) -> AssignStmt:
        pos    = self.s.current().pos
        target = IdentExpr(pos=pos, name=self.s.advance().value)
        op     = self.s.advance().value
        value  = self._expr()
        return AssignStmt(pos=pos, target=target, op=op, value=value)

    # ── DEL name ─────────────────────────────────────────────────────────────
    def _parse_del(self) -> DeleteStmt:
        pos = self.s.current().pos
        self.s.advance()
        name = self.s.expect(TT.IDENT).value
        return DeleteStmt(pos=pos, name=name)

    # ── IF cond { } ELIF cond { } ELSE { } ───────────────────────────────────
    def _parse_if(self) -> IfStmt:
        pos = self.s.current().pos
        self.s.advance()   # consume IF
        cond = self._expr()
        body = self._parse_block()
        elif_clauses = []
        else_body    = None
        self.s.skip_newlines()
        while self.s.current().is_kw("ELIF"):
            self.s.advance()
            ec   = self._expr()
            eb   = self._parse_block()
            elif_clauses.append((ec, eb))
            self.s.skip_newlines()
        if self.s.current().is_kw("ELSE"):
            self.s.advance()
            else_body = self._parse_block()
        return IfStmt(pos=pos, condition=cond, body=body,
                      elif_clauses=elif_clauses, else_body=else_body)

    # ── WHILE cond { } ───────────────────────────────────────────────────────
    def _parse_while(self) -> WhileStmt:
        pos = self.s.current().pos
        self.s.advance()
        cond = self._expr()
        body = self._parse_block()
        return WhileStmt(pos=pos, condition=cond, body=body)

    # ── FOR var IN iterable { } ──────────────────────────────────────────────
    def _parse_for(self) -> ForStmt:
        pos = self.s.current().pos
        self.s.advance()
        var = self.s.expect(TT.IDENT).value
        self.s.expect_kw("IN")
        iterable = self._expr()
        body     = self._parse_block()
        return ForStmt(pos=pos, var=var, iterable=iterable, body=body)

    # ── RETURN expr ──────────────────────────────────────────────────────────
    def _parse_return(self) -> ReturnStmt:
        pos = self.s.current().pos
        self.s.advance()
        val = None
        if not self.s.current().is_tt(TT.NEWLINE, TT.RBRACE, TT.EOF, TT.SEMICOLON):
            val = self._expr()
        return ReturnStmt(pos=pos, value=val)

    # ── FUNC name(params) { } ────────────────────────────────────────────────
    def _parse_func(self) -> FuncDefStmt:
        pos      = self.s.current().pos
        is_async = self.s.current().is_kw("ASYNC")
        if is_async:
            self.s.advance()
        self.s.expect_kw("FUNC")
        name   = self.s.expect(TT.IDENT).value
        params = self._parse_params()
        body   = self._parse_block()
        return FuncDefStmt(pos=pos, name=name, params=params,
                           body=body, is_async=is_async)

    def _parse_params(self) -> List[ParamDef]:
        self.s.expect(TT.LPAREN)
        params = []
        self.s.skip_newlines()
        while not self.s.current().is_tt(TT.RPAREN, TT.EOF):
            pname   = self.s.expect(TT.IDENT).value
            default = None
            if self.s.match(TT.EQUALS):
                default = self._expr()
            params.append(ParamDef(name=pname, default=default))
            self.s.skip_newlines()
            if not self.s.match(TT.COMMA):
                break
            self.s.skip_newlines()
        self.s.expect(TT.RPAREN)
        return params

    # ── CALL name(args) ──────────────────────────────────────────────────────
    def _parse_call_stmt(self) -> CallStmt:
        pos = self.s.current().pos
        self.s.advance()   # consume CALL
        expr = self._expr()
        if not isinstance(expr, CallExpr):
            raise self._err("CALL must be followed by a function call expression")
        return CallStmt(pos=pos, call_expr=expr)

    # ── TRY { } CATCH e { } FINALLY { } ─────────────────────────────────────
    def _parse_try(self) -> TryCatchStmt:
        pos = self.s.current().pos
        self.s.advance()
        body         = self._parse_block()
        catch_var    = None
        catch_body   = None
        finally_body = None
        self.s.skip_newlines()
        if self.s.current().is_kw("CATCH"):
            self.s.advance()
            if self.s.current().type is TT.IDENT:
                catch_var = self.s.advance().value
            catch_body = self._parse_block()
            self.s.skip_newlines()
        if self.s.current().is_kw("FINALLY"):
            self.s.advance()
            finally_body = self._parse_block()
        return TryCatchStmt(pos=pos, body=body, catch_var=catch_var,
                            catch_body=catch_body, finally_body=finally_body)

    # ── THROW expr ───────────────────────────────────────────────────────────
    def _parse_throw(self) -> ThrowStmt:
        pos = self.s.current().pos
        self.s.advance()
        return ThrowStmt(pos=pos, value=self._expr())

    # ── ASSERT expr ──────────────────────────────────────────────────────────
    def _parse_assert(self) -> AssertStmt:
        pos = self.s.current().pos
        self.s.advance()
        cond = self._expr()
        msg  = None
        if self.s.match(TT.COMMA):
            msg = self._expr()
        return AssertStmt(pos=pos, condition=cond, message=msg)

    # ── PRINT expr, expr, ... ────────────────────────────────────────────────
    def _parse_print(self) -> PrintStmt:
        pos = self.s.current().pos
        self.s.advance()
        args = []
        while not self.s.current().is_tt(TT.NEWLINE, TT.SEMICOLON,
                                          TT.RBRACE, TT.EOF):
            args.append(self._expr())
            # Continue parsing expressions without requiring commas
            # Only break if we hit a terminator
        return PrintStmt(pos=pos, args=args)

    # ── LOG level expr ───────────────────────────────────────────────────────
    def _parse_log(self) -> LogStmt:
        pos = self.s.current().pos
        self.s.advance()
        level = "INFO"
        if self.s.current().type is TT.IDENT:
            level = self.s.advance().value.upper()
        args = [self._expr()]
        return LogStmt(pos=pos, level=level, args=args)

    # ── ALERT "title" "message" ──────────────────────────────────────────────
    def _parse_alert(self) -> AlertStmt:
        pos = self.s.current().pos
        self.s.advance()
        title   = self._expr()
        message = self._expr()
        return AlertStmt(pos=pos, title=title, message=message)

    # ── ERROR "title" "message" ──────────────────────────────────────────────
    def _parse_error_dialog(self) -> ErrorDialogStmt:
        pos = self.s.current().pos
        self.s.advance()
        title   = self._expr()
        message = self._expr()
        return ErrorDialogStmt(pos=pos, title=title, message=message)

    # ── CONFIRM "title" "message" ────────────────────────────────────────────
    def _parse_confirm(self) -> ConfirmStmt:
        pos = self.s.current().pos
        self.s.advance()
        title   = self._expr()
        message = self._expr()
        return ConfirmStmt(pos=pos, title=title, message=message)

    # ── WAIT expr ────────────────────────────────────────────────────────────
    def _parse_wait(self) -> WaitStmt:
        pos = self.s.current().pos
        self.s.advance()
        return WaitStmt(pos=pos, seconds=self._expr())

    # ── AFTER expr { } ───────────────────────────────────────────────────────
    def _parse_after(self) -> AfterStmt:
        pos = self.s.current().pos
        self.s.advance()
        seconds = self._expr()
        body    = self._parse_block()
        return AfterStmt(pos=pos, seconds=seconds, body=body)

    # ── LOOP { } ─────────────────────────────────────────────────────────────
    def _parse_loop(self) -> LoopStmt:
        pos = self.s.current().pos
        self.s.advance()
        delay = None
        if self.s.current().is_kw("DELAY"):
            self.s.advance()
            delay = self._expr()
        body = self._parse_block()
        return LoopStmt(pos=pos, body=body, delay=delay)

    # ── TIMER name interval { } ──────────────────────────────────────────────
    def _parse_timer(self) -> TimerStmt:
        pos = self.s.current().pos
        self.s.advance()
        name     = self.s.expect(TT.IDENT).value
        interval = self._expr()
        body     = self._parse_block()
        return TimerStmt(pos=pos, name=name, interval=interval, body=body)

    # ── SCHEDULE hour minute { } ─────────────────────────────────────────────
    def _parse_schedule(self) -> ScheduleStmt:
        pos = self.s.current().pos
        self.s.advance()
        hour   = self._expr()
        minute = self._expr()
        body   = self._parse_block()
        return ScheduleStmt(pos=pos, hour=hour, minute=minute, body=body)

    # ── AUDIO "file" ─────────────────────────────────────────────────────────
    def _parse_audio(self) -> AudioStmt:
        pos  = self.s.current().pos
        self.s.advance()
        file = self._expr()
        loop = False
        if self.s.current().is_kw("LOOP"):
            self.s.advance(); loop = True
        return AudioStmt(pos=pos, file=file, loop=loop)

    # ── VIDEO "file" ─────────────────────────────────────────────────────────
    def _parse_video(self) -> VideoStmt:
        pos  = self.s.current().pos
        self.s.advance()
        file = self._expr()
        return VideoStmt(pos=pos, file=file)

    # ── WRITE_FILE "path" "content" ──────────────────────────────────────────
    def _parse_write_file(self) -> WriteFileStmt:
        pos = self.s.current().pos
        self.s.advance()
        path    = self._expr()
        content = self._expr()
        return WriteFileStmt(pos=pos, path=path, content=content)

    # ── READ_FILE "path" ─────────────────────────────────────────────────────
    def _parse_read_file(self) -> ReadFileStmt:
        pos = self.s.current().pos
        self.s.advance()
        path       = self._expr()
        result_var = None
        if self.s.current().is_kw("INTO"):
            self.s.advance()
            result_var = self.s.expect(TT.IDENT).value
        return ReadFileStmt(pos=pos, path=path, result_var=result_var)

    # ── COPY expr ────────────────────────────────────────────────────────────
    def _parse_copy(self) -> CopyStmt:
        pos = self.s.current().pos
        self.s.advance()
        return CopyStmt(pos=pos, value=self._expr())

    # ── PASTE ────────────────────────────────────────────────────────────────
    def _parse_paste(self) -> PasteStmt:
        pos = self.s.current().pos
        self.s.advance()
        result_var = None
        if self.s.current().type is TT.IDENT:
            result_var = self.s.advance().value
        return PasteStmt(pos=pos, result_var=result_var)

    # ── IMPORT "path" ────────────────────────────────────────────────────────
    def _parse_import(self) -> ImportStmt:
        pos = self.s.current().pos
        self.s.advance()
        path  = self.s.expect(TT.STRING).value
        alias = None
        if self.s.current().is_kw("AS"):
            self.s.advance()
            alias = self.s.expect(TT.IDENT).value
        return ImportStmt(pos=pos, path=path, alias=alias)

    # ── APP "title" SIZE w h ─────────────────────────────────────────────────
    def _parse_app(self) -> ExprStmt:
        from parser_ast import StringLiteralExpr as SLE, NumberLiteralExpr as NLE
        pos = self.s.current().pos
        self.s.advance()
        title = self._expr()
        w, h  = NumberLiteralExpr(pos=pos, value=800, raw="800"), \
                NumberLiteralExpr(pos=pos, value=600, raw="600")
        if self.s.current().is_kw("SIZE"):
            self.s.advance()
            w = self._expr()
            h = self._expr()
        callee = IdentExpr(pos=pos, name="APP")
        return ExprStmt(pos=pos,
                        expr=CallExpr(pos=pos, callee=callee,
                                      args=[title, w, h], kwargs={}))

    # ── WIDGET name "text" props { events } ──────────────────────────────────
    def _parse_widget(self) -> ExprStmt:
        pos     = self.s.current().pos
        kind    = self.s.advance().value.upper()
        name    = self.s.expect(TT.IDENT).value if self.s.current().type is TT.IDENT else ""
        props   = {}
        events  = []

        # collect inline keyword=value props
        while self.s.current().type is TT.KEYWORD and \
              self.s.current().value.upper() not in (
                  "ONCLICK","ONCHANGE","ONHOVER","ONKEY","ONFOCUS","ONBLUR") and \
              not self.s.current().is_tt(TT.LBRACE, TT.NEWLINE,
                                          TT.SEMICOLON, TT.EOF, TT.RBRACE):
            prop_key = self.s.advance().value.upper()
            prop_val = self._expr()
            props[prop_key] = prop_val

        # optional block for events / nested props
        if self.s.current().type is TT.LBRACE:
            self.s.advance()
            self.s.skip_newlines()
            while not self.s.current().is_tt(TT.RBRACE, TT.EOF):
                stmt = self._parse_stmt()
                if stmt:
                    events.append(stmt)
                self.s.skip_newlines_and_semis()
            self.s.expect(TT.RBRACE)

        callee = IdentExpr(pos=pos, name=f"WIDGET_{kind}")
        args   = [StringLiteralExpr(pos=pos, value=name)]
        return ExprStmt(pos=pos,
                        expr=CallExpr(pos=pos, callee=callee,
                                      args=args, kwargs={}))


# =============================================================================
# FLUX EXECUTOR  — walks the AST and calls the engine
# =============================================================================

class FLUXExecutor:
    """
    Tree-walk interpreter.
    Receives a ProgramNode and executes it against a FLUX engine instance.
    """

    def __init__(self, engine):
        self.engine = engine
        self._vars: Dict[str, Any] = {}
        self._funcs: Dict[str, FuncDefStmt] = {}

    # ── entry ────────────────────────────────────────────────────────────────

    def execute(self, program: ProgramNode):
        for stmt in program.body:
            self._exec_stmt(stmt)

    # ── expression evaluator ─────────────────────────────────────────────────

    def _eval(self, expr: ExprNode) -> Any:
        if isinstance(expr, NumberLiteralExpr):
            return expr.value
        if isinstance(expr, StringLiteralExpr):
            return expr.value
        if isinstance(expr, BoolLiteralExpr):
            return expr.value
        if isinstance(expr, NullLiteralExpr):
            return None
        if isinstance(expr, IdentExpr):
            return self._vars.get(expr.name)
        if isinstance(expr, ListExpr):
            return [self._eval(e) for e in expr.elements]
        if isinstance(expr, BinaryExpr):
            return self._eval_binary(expr)
        if isinstance(expr, UnaryExpr):
            return self._eval_unary(expr)
        if isinstance(expr, CallExpr):
            return self._eval_call(expr)
        if isinstance(expr, IndexExpr):
            obj = self._eval(expr.obj)
            idx = self._eval(expr.index)
            try:
                return obj[idx]
            except Exception:
                return None
        if isinstance(expr, MemberExpr):
            obj = self._eval(expr.obj)
            try:
                return getattr(obj, expr.member, None)
            except Exception:
                return None
        return None

    def _eval_binary(self, expr: BinaryExpr) -> Any:
        op = expr.op
        # short-circuit logical
        if op == "AND":
            return self._eval(expr.left) and self._eval(expr.right)
        if op == "OR":
            return self._eval(expr.left) or self._eval(expr.right)
        L = self._eval(expr.left)
        R = self._eval(expr.right)
        ops = {
            "+": lambda a,b: a+b,  "-": lambda a,b: a-b,
            "*": lambda a,b: a*b,  "/": lambda a,b: a/b,
            "%": lambda a,b: a%b,  "**": lambda a,b: a**b,
            "//": lambda a,b: a//b,
            "==": lambda a,b: a==b, "!=": lambda a,b: a!=b,
            "<":  lambda a,b: a<b,  ">":  lambda a,b: a>b,
            "<=": lambda a,b: a<=b, ">=": lambda a,b: a>=b,
            "IN": lambda a,b: a in b,
        }
        fn = ops.get(op)
        if fn:
            try:
                return fn(L, R)
            except Exception:
                return None
        return None

    def _eval_unary(self, expr: UnaryExpr) -> Any:
        v = self._eval(expr.operand)
        if expr.op == "-":   return -v
        if expr.op == "NOT": return not v
        if expr.op == "!":   return not v
        if expr.op == "~":   return ~v
        return v

    def _eval_call(self, expr: CallExpr) -> Any:
        if isinstance(expr.callee, IdentExpr):
            name = expr.callee.name.upper()
            args = [self._eval(a) for a in expr.args]
            # engine dispatch
            if name == "APP":
                self.engine.APP(args[0], int(args[1]), int(args[2]))
                return None
            if name.startswith("WIDGET_"):
                return None   # handled by statement parser
            # user-defined function
            if name.lower() in self._funcs:
                return self._call_user_func(self._funcs[name.lower()], args)
        return None

    def _call_user_func(self, func: FuncDefStmt, args: list) -> Any:
        saved = dict(self._vars)
        for i, param in enumerate(func.params):
            self._vars[param.name] = args[i] if i < len(args) else None
        result = None
        try:
            for stmt in func.body:
                self._exec_stmt(stmt)
        except _ReturnSignal as ret:
            result = ret.value
        finally:
            self._vars = saved
        return result

    # ── statement executor ───────────────────────────────────────────────────

    def _exec_stmt(self, stmt: StmtNode) -> Any:
        if isinstance(stmt, VarDeclStmt):
            self._vars[stmt.name] = self._eval(stmt.value) if stmt.value else None

        elif isinstance(stmt, AssignStmt):
            val = self._eval(stmt.value)
            if isinstance(stmt.target, IdentExpr):
                name = stmt.target.name
                if stmt.op == "=":   self._vars[name] = val
                elif stmt.op == "+=": self._vars[name] = (self._vars.get(name, 0) + val)
                elif stmt.op == "-=": self._vars[name] = (self._vars.get(name, 0) - val)
                elif stmt.op == "*=": self._vars[name] = (self._vars.get(name, 0) * val)
                elif stmt.op == "/=": self._vars[name] = (self._vars.get(name, 0) / val)
                elif stmt.op == "%=": self._vars[name] = (self._vars.get(name, 0) % val)

        elif isinstance(stmt, DeleteStmt):
            self._vars.pop(stmt.name, None)

        elif isinstance(stmt, PrintStmt):
            parts = [str(self._eval(a)) for a in stmt.args]
            print(" ".join(parts))

        elif isinstance(stmt, LogStmt):
            parts = [str(self._eval(a)) for a in stmt.args]
            print(f"[{stmt.level}]", " ".join(parts))

        elif isinstance(stmt, AlertStmt):
            from tkinter import messagebox
            messagebox.showinfo(str(self._eval(stmt.title)),
                                str(self._eval(stmt.message)))

        elif isinstance(stmt, ErrorDialogStmt):
            from tkinter import messagebox
            messagebox.showerror(str(self._eval(stmt.title)),
                                 str(self._eval(stmt.message)))

        elif isinstance(stmt, ConfirmStmt):
            from tkinter import messagebox
            messagebox.askyesno(str(self._eval(stmt.title)),
                                str(self._eval(stmt.message)))

        elif isinstance(stmt, IfStmt):
            if self._eval(stmt.condition):
                for s in stmt.body: self._exec_stmt(s)
            else:
                done = False
                for cond, body in stmt.elif_clauses:
                    if self._eval(cond):
                        for s in body: self._exec_stmt(s)
                        done = True; break
                if not done and stmt.else_body:
                    for s in stmt.else_body: self._exec_stmt(s)

        elif isinstance(stmt, WhileStmt):
            while self._eval(stmt.condition):
                try:
                    for s in stmt.body: self._exec_stmt(s)
                except _BreakSignal:
                    break
                except _ContinueSignal:
                    continue

        elif isinstance(stmt, ForStmt):
            iterable = self._eval(stmt.iterable)
            if iterable is None: iterable = []
            for item in iterable:
                self._vars[stmt.var] = item
                try:
                    for s in stmt.body: self._exec_stmt(s)
                except _BreakSignal:
                    break
                except _ContinueSignal:
                    continue

        elif isinstance(stmt, BreakStmt):
            raise _BreakSignal()

        elif isinstance(stmt, ContinueStmt):
            raise _ContinueSignal()

        elif isinstance(stmt, ReturnStmt):
            raise _ReturnSignal(self._eval(stmt.value) if stmt.value else None)

        elif isinstance(stmt, FuncDefStmt):
            self._funcs[stmt.name.lower()] = stmt

        elif isinstance(stmt, CallStmt):
            self._eval_call(stmt.call_expr)

        elif isinstance(stmt, ExprStmt):
            self._eval(stmt.expr)

        elif isinstance(stmt, WaitStmt):
            import time
            time.sleep(float(self._eval(stmt.seconds)))

        elif isinstance(stmt, AudioStmt):
            self.engine.AUDIO(str(self._eval(stmt.file)), loop=stmt.loop)

        elif isinstance(stmt, AudioStopStmt):
            self.engine.AUDIO_STOP()

        elif isinstance(stmt, VideoStmt):
            self.engine.VIDEO(str(self._eval(stmt.file)))

        elif isinstance(stmt, WriteFileStmt):
            path    = str(self._eval(stmt.path))
            content = str(self._eval(stmt.content))
            with open(path, stmt.mode, encoding="utf-8") as f:
                f.write(content)

        elif isinstance(stmt, ReadFileStmt):
            path = str(self._eval(stmt.path))
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = f.read()
            except Exception:
                data = None
            if stmt.result_var:
                self._vars[stmt.result_var] = data

        elif isinstance(stmt, CopyStmt):
            self.engine.vars["__clipboard__"] = self._eval(stmt.value)

        elif isinstance(stmt, TryCatchStmt):
            try:
                for s in stmt.body: self._exec_stmt(s)
            except Exception as e:
                if stmt.catch_var:
                    self._vars[stmt.catch_var] = str(e)
                if stmt.catch_body:
                    for s in stmt.catch_body: self._exec_stmt(s)
            finally:
                if stmt.finally_body:
                    for s in stmt.finally_body: self._exec_stmt(s)

        elif isinstance(stmt, ThrowStmt):
            raise RuntimeError(str(self._eval(stmt.value)))

        elif isinstance(stmt, AssertStmt):
            if not self._eval(stmt.condition):
                msg = str(self._eval(stmt.message)) if stmt.message else "Assertion failed"
                raise AssertionError(msg)

        return None


# ── control flow signals ─────────────────────────────────────────────────────

class _BreakSignal(Exception):    pass
class _ContinueSignal(Exception): pass
class _ReturnSignal(Exception):
    def __init__(self, value): self.value = value


# =============================================================================
# FLUX PARSER  — public entry point
# =============================================================================

class FLUXParser:
    """
    Public API. Load a .flux file, parse it, execute against an engine.
    """

    def __init__(self, engine):
        self.engine   = engine
        self.errors:  List[str] = []
        self.warnings: List[str] = []

    def compile(self, filepath: str):
        """Full pipeline: file → tokens → AST → execution."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
        except OSError as e:
            self.errors.append(f"Cannot open file: {e}")
            return False

        return self.compile_source(source, filepath)

    def compile_source(self, source: str, filename: str = "<stdin>") -> bool:
        """Parse and execute a source string."""
        try:
            stream  = make_stream(source, filename)
            program = StatementParser(stream, filename).parse_program()
            FLUXExecutor(self.engine).execute(program)
            return True
        except ParseError as e:
            self.errors.append(str(e))
            print(str(e))
            return False
        except Exception as e:
            import traceback
            msg = f"[RUNTIME] {filename}: {e}\n{traceback.format_exc()}"
            self.errors.append(msg)
            print(msg)
            return False

    def parse_only(self, source: str, filename: str = "<stdin>") -> Optional[ProgramNode]:
        """Parse without executing — returns AST or None on error."""
        try:
            stream = make_stream(source, filename)
            return StatementParser(stream, filename).parse_program()
        except ParseError as e:
            self.errors.append(str(e))
            return None
