# ============================================================
# Test.flux  —  FLUX Language Integration Test
# Tests: variables, arithmetic, control flow, functions,
#        loops, try/catch, file IO, lists
# ============================================================

# ── 1. Variables ─────────────────────────────────────────────
VAR name    = "FLUX"
VAR version = 1
VAR pi      = 3.14159
VAR active  = TRUE

PRINT "=== FLUX Language Test ==="
PRINT "Language:" name
PRINT "Version:" version

# ── 2. Arithmetic & expressions ──────────────────────────────
VAR a = 10
VAR b = 3
VAR sum     = a + b
VAR product = a * b
VAR power   = a ** b
VAR modulo  = a % b

PRINT "--- Arithmetic ---"
PRINT "10 + 3 =" sum
PRINT "10 * 3 =" product
PRINT "10 ** 3 =" power
PRINT "10 % 3 =" modulo

# ── 3. Compound assignment ────────────────────────────────────
VAR counter = 0
SET counter += 5
SET counter *= 2
PRINT "Counter after +=5 *=2:" counter

# ── 4. IF / ELIF / ELSE ───────────────────────────────────────
PRINT "--- Conditionals ---"
VAR score = 85

IF score >= 90 {
    PRINT "Grade: A"
} ELIF score >= 80 {
    PRINT "Grade: B"
} ELIF score >= 70 {
    PRINT "Grade: C"
} ELSE {
    PRINT "Grade: F"
}

# ── 5. WHILE loop ─────────────────────────────────────────────
PRINT "--- While Loop ---"
VAR i = 1
VAR total = 0
WHILE i <= 5 {
    SET total += i
    SET i += 1
}
PRINT "Sum 1..5 =" total

# ── 6. FOR loop ───────────────────────────────────────────────
PRINT "--- For Loop ---"
VAR fruits = ["apple", "banana", "cherry"]
FOR fruit IN fruits {
    PRINT "Fruit:" fruit
}

# ── 7. Functions ──────────────────────────────────────────────
PRINT "--- Functions ---"

FUNC greet(person) {
    PRINT "Hello," person
}

FUNC factorial(n) {
    IF n <= 1 {
        RETURN 1
    }
    RETURN n * factorial(n - 1)
}

FUNC clamp(val, lo, hi) {
    IF val < lo { RETURN lo }
    IF val > hi { RETURN hi }
    RETURN val
}

CALL greet("World")
PRINT "5! =" factorial(5)
PRINT "clamp(15,0,10) =" clamp(15, 0, 10)

# ── 8. Nested IF inside function ─────────────────────────────
FUNC classify(n) {
    IF n < 0 {
        PRINT n "is negative"
    } ELIF n == 0 {
        PRINT n "is zero"
    } ELSE {
        PRINT n "is positive"
    }
}

CALL classify(-5)
CALL classify(0)
CALL classify(42)

# ── 9. TRY / CATCH ────────────────────────────────────────────
PRINT "--- Try/Catch ---"
TRY {
    ASSERT 1 == 1, "math is broken"
    PRINT "Assert passed"
} CATCH err {
    PRINT "Caught:" err
}

TRY {
    THROW "deliberate error"
} CATCH err {
    PRINT "Caught throw:" err
}

# ── 10. File IO ───────────────────────────────────────────────
PRINT "--- File IO ---"
WRITE_FILE "flux_test_output.txt" "Hello from FLUX!\nVersion 1"
READ_FILE "flux_test_output.txt" INTO filedata
PRINT "File contents:" filedata

# ── 11. Boolean logic ─────────────────────────────────────────
PRINT "--- Boolean Logic ---"
VAR x = TRUE
VAR y = FALSE

IF x AND NOT y {
    PRINT "x=TRUE y=FALSE: AND NOT correct"
}
IF x OR y {
    PRINT "x OR y: correct"
}

# ── 12. String in expressions ─────────────────────────────────
PRINT "--- String Concat ---"
VAR first = "Hello"
VAR second = " World"
VAR joined = first + second
PRINT joined

# ── 13. Nested loops ──────────────────────────────────────────
PRINT "--- Nested Loops ---"
VAR row = 1
WHILE row <= 3 {
    VAR col = 1
    WHILE col <= 3 {
        SET col += 1
    }
    PRINT "Row" row "done"
    SET row += 1
}

# ── 14. DEL variable ──────────────────────────────────────────
VAR temp = 999
DEL temp
PRINT "temp after DEL:" temp

PRINT "=== All Tests Complete ==="
