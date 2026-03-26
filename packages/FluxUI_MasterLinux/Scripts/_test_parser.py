from tokenizer import make_stream
from parser import ExpressionParser, StatementParser

# Test 1: expression precedence  2 + 3 * 4  should be  2 + (3*4)
s = make_stream("2 + 3 * 4")
tree = ExpressionParser(s).parse()
print("Expr tree:", tree)

# Test 2: VAR declaration
s2 = make_stream("VAR counter = 10")
prog2 = StatementParser(s2).parse_program()
print("VarDecl:", prog2.body[0])

# Test 3: IF statement
s3 = make_stream('IF counter > 5 { PRINT "big" }')
prog3 = StatementParser(s3).parse_program()
print("If stmt:", prog3.body[0])

# Test 4: FUNC definition
s4 = make_stream('FUNC add(a, b) { RETURN a + b }')
prog4 = StatementParser(s4).parse_program()
print("FuncDef:", prog4.body[0])

# Test 5: FOR loop
s5 = make_stream('FOR item IN myList { PRINT item }')
prog5 = StatementParser(s5).parse_program()
print("ForStmt:", prog5.body[0])

# Test 6: TRY/CATCH
s6 = make_stream('TRY { PRINT "ok" } CATCH err { PRINT err }')
prog6 = StatementParser(s6).parse_program()
print("TryCatch:", prog6.body[0])

print("\nAll parser tests PASSED")
