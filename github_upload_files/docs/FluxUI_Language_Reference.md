# FluxUI Language Reference

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Basic Syntax](#basic-syntax)
4. [Data Types](#data-types)
5. [Variables](#variables)
6. [Operators](#operators)
7. [Control Flow](#control-flow)
8. [Functions](#functions)
9. [Error Handling](#error-handling)
10. [File I/O](#file-io)
11. [UI Widgets](#ui-widgets)
12. [Events](#events)
13. [Layout Management](#layout-management)
14. [Graphics and Charts](#graphics-and-charts)
15. [System Operations](#system-operations)
16. [Built-in Functions](#built-in-functions)
17. [Examples](#examples)

---

## Overview

FluxUI is a high-level programming language designed for creating user interfaces with ease. It combines traditional programming constructs with a rich set of UI widgets and event handling capabilities.

### Key Features
- **Simple Syntax**: Clean, readable syntax inspired by modern languages
- **Rich UI Components**: Extensive widget library for modern interfaces
- **Event-Driven**: Comprehensive event handling system
- **Cross-Platform**: Built on Python with CustomTkinter
- **Graphics Support**: Built-in charting and visualization capabilities
- **File Operations**: Native file I/O support
- **Error Handling**: Robust try/catch exception handling

---

## Installation

### Requirements
- Python 3.7 or higher
- CustomTkinter
- PyInstaller (for building executables)

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install customtkinter pyinstaller
   ```

2. **Build Executable**
   ```bash
   python build_exe.py
   ```

3. **Install File Association**
   ```bash
   # Run as Administrator
   install_flux_extension.bat
   ```

4. **Install Executable System-wide**
   ```bash
   # Run as Administrator
   install_exe.bat
   ```

### Usage
```bash
# Execute a FluxUI file
fluxui program.flux

# Execute with GUI interface
fluxui program.flux --gui

# Show version
fluxui --version
```

---

## Basic Syntax

### Comments
```flux
# Single line comment
# Multi-line comments
# are supported
# with multiple lines
```

### Statements
Statements in FluxUI are terminated by newlines. Blocks are defined using curly braces `{}`.

```flux
VAR x = 10
PRINT "Hello World"

IF condition {
    # Block of code
}
```

### Case Sensitivity
- **Keywords**: UPPERCASE only (VAR, IF, WHILE, etc.)
- **Variables**: Case-sensitive (myVar, MyVar, myvar are different)
- **Functions**: Case-sensitive
- **Strings**: Case-sensitive

---

## Data Types

### Primitive Types

#### Numbers
```flux
VAR integer = 42
VAR float_num = 3.14159
VAR scientific = 1.23e-4
```

#### Strings
```flux
VAR string = "Hello World"
VAR empty = ""
VAR with_quotes = "He said \"Hello\""
```

#### Booleans
```flux
VAR true_val = TRUE
VAR false_val = FALSE
```

#### Null
```flux
VAR null_val = NULL
```

### Collections

#### Lists
```flux
VAR numbers = [1, 2, 3, 4, 5]
VAR mixed = [1, "hello", TRUE, NULL]
VAR nested = [[1, 2], [3, 4]]
```

---

## Variables

### Declaration
```flux
VAR name = "FluxUI"
VAR version = 1.0
VAR active = TRUE
```

### Assignment
```flux
VAR x = 10
SET x = 20
```

### Compound Assignment
```flux
VAR counter = 0
SET counter += 5    # counter = counter + 5
SET counter *= 2    # counter = counter * 2
SET counter -= 1    # counter = counter - 1
SET counter /= 2    # counter = counter / 2
```

### Deletion
```flux
VAR temp = 999
DEL temp
```

---

## Operators

### Arithmetic Operators
```flux
VAR a = 10, b = 3
VAR sum = a + b          # Addition: 13
VAR diff = a - b         # Subtraction: 7
VAR prod = a * b         # Multiplication: 30
VAR quot = a / b         # Division: 3.333...
VAR mod = a % b          # Modulus: 1
VAR power = a ** b       # Exponentiation: 1000
```

### Comparison Operators
```flux
VAR x = 10, y = 20
VAR eq = x == y          # Equal: FALSE
VAR ne = x != y          # Not equal: TRUE
VAR lt = x < y           # Less than: TRUE
VAR le = x <= y          # Less than or equal: TRUE
VAR gt = x > y           # Greater than: FALSE
VAR ge = x >= y          # Greater than or equal: FALSE
```

### Logical Operators
```flux
VAR a = TRUE, b = FALSE
VAR and_result = a AND b     # FALSE
VAR or_result = a OR b       # TRUE
VAR not_result = NOT a       # FALSE
```

### String Concatenation
```flux
VAR first = "Hello"
VAR second = " World"
VAR joined = first + second  # "Hello World"
```

---

## Control Flow

### IF Statements
```flux
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
```

### WHILE Loops
```flux
VAR i = 1
VAR total = 0

WHILE i <= 5 {
    SET total += i
    SET i += 1
}
PRINT "Sum 1..5 =" total  # Output: 15
```

### FOR Loops
```flux
VAR fruits = ["apple", "banana", "cherry"]

FOR fruit IN fruits {
    PRINT "Fruit:" fruit
}

# Range-style loop
FOR i FROM 1 TO 5 {
    PRINT i
}
```

### Break and Continue
```flux
VAR i = 0
WHILE i < 10 {
    SET i += 1
    IF i == 5 {
        BREAK
    }
    IF i % 2 == 0 {
        CONTINUE
    }
    PRINT i  # Prints: 1, 3
}
```

---

## Functions

### Function Definition
```flux
FUNC greet(name) {
    PRINT "Hello," name
}

FUNC factorial(n) {
    IF n <= 1 {
        RETURN 1
    }
    RETURN n * factorial(n - 1)
}
```

### Function Calls
```flux
CALL greet("World")
VAR result = factorial(5)
PRINT "5! =" result  # Output: 120
```

### Parameters and Return Values
```flux
FUNC add(a, b) {
    RETURN a + b
}

FUNC divide(a, b) {
    IF b == 0 {
        THROW "Division by zero"
    }
    RETURN a / b
}
```

### Recursive Functions
```flux
FUNC fibonacci(n) {
    IF n <= 1 {
        RETURN n
    }
    RETURN fibonacci(n - 1) + fibonacci(n - 2)
}
```

---

## Error Handling

### TRY-CATCH Blocks
```flux
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
```

### Assertions
```flux
VAR x = 10
ASSERT x > 0, "x must be positive"
ASSERT x < 100, "x must be less than 100"
```

---

## File I/O

### Writing Files
```flux
WRITE_FILE "output.txt" "Hello from FluxUI!"
WRITE_FILE "data.csv" "Name,Age\nJohn,25\nJane,30"
```

### Reading Files
```flux
READ_FILE "input.txt" INTO content
PRINT "File contents:" content

READ_FILE "config.json" INTO config
```

### File Operations
```flux
COPY "source.txt" "destination.txt"
PASTE "clipboard_content" INTO file
```

---

## UI Widgets

### Basic Widgets

#### Button
```flux
BUTTON btn1 {
    TEXT: "Click Me"
    WIDTH: 100
    HEIGHT: 30
    ONCLICK: {
        PRINT "Button clicked!"
    }
}
```

#### Label
```flux
LABEL label1 {
    TEXT: "Hello World"
    FONT: "Arial"
    FONT_SIZE: 16
    FG: "#000000"
}
```

#### Input Field
```flux
INPUT input1 {
    PLACEHOLDER: "Enter text..."
    WIDTH: 200
    ONCHANGE: {
        PRINT "Input changed:" GET_VALUE(input1)
    }
}
```

#### Textbox
```flux
TEXTBOX textbox1 {
    WIDTH: 300
    HEIGHT: 150
    TEXT: "Multiline text content"
    ONINPUT: {
        PRINT "Text updated"
    }
}
```

#### Switch
```flux
SWITCH switch1 {
    VALUE: FALSE
    ONTOGGLE: {
        PRINT "Switch state:" GET_STATE(switch1)
    }
}
```

#### Slider
```flux
SLIDER slider1 {
    MIN: 0
    MAX: 100
    VALUE: 50
    WIDTH: 200
    ONCHANGE: {
        PRINT "Slider value:" GET_VALUE(slider1)
    }
}
```

#### Progress Bar
```flux
PROGRESS progress1 {
    VALUE: 75
    WIDTH: 200
    HEIGHT: 20
}
```

#### Dropdown
```flux
DROPDOWN dropdown1 {
    ITEMS: ["Option 1", "Option 2", "Option 3"]
    VALUE: "Option 1"
    ONCHANGE: {
        PRINT "Selected:" GET_VALUE(dropdown1)
    }
}
```

---

## Events

### Mouse Events
```flux
BUTTON btn {
    TEXT: "Click Me"
    ONCLICK: { PRINT "Single click" }
    ONDOUBLECLICK: { PRINT "Double click" }
    ONRIGHTCLICK: { PRINT "Right click" }
    ONHOVER: { PRINT "Mouse entered" }
    ONLEAVE: { PRINT "Mouse left" }
}
```

### Keyboard Events
```flux
INPUT input1 {
    ONKEYDOWN: { PRINT "Key pressed" }
    ONKEYUP: { PRINT "Key released" }
    ONKEYPRESS: { PRINT "Key typed" }
}
```

### Focus Events
```flux
INPUT input1 {
    ONFOCUS: { PRINT "Input focused" }
    ONBLUR: { PRINT "Input lost focus" }
}
```

### Window Events
```flux
WINDOW main {
    ONRESIZE: { PRINT "Window resized" }
    ONCLOSE: { PRINT "Window closing" }
    ONFOCUS: { PRINT "Window focused" }
}
```

---

## Layout Management

### Frame Layout
```flux
FRAME frame1 {
    WIDTH: 400
    HEIGHT: 300
    PADDING: 10
    
    LABEL label1 {
        TEXT: "Inside Frame"
        X: 10
        Y: 10
    }
}
```

### Grid Layout
```flux
GRID grid1 {
    ROWS: 3
    COLS: 2
    PADDING: 5
    
    BUTTON btn1 {
        TEXT: "Button 1"
        ROW: 0
        COL: 0
    }
    
    BUTTON btn2 {
        TEXT: "Button 2"
        ROW: 0
        COL: 1
    }
}
```

### Row and Column Layout
```flux
ROW row1 {
    SPACING: 10
    PADDING: 5
    
    BUTTON btn1 { TEXT: "Button 1" }
    BUTTON btn2 { TEXT: "Button 2" }
    BUTTON btn3 { TEXT: "Button 3" }
}

COLUMN col1 {
    SPACING: 5
    PADDING: 10
    
    LABEL label1 { TEXT: "Label 1" }
    INPUT input1 { PLACEHOLDER: "Input 1" }
    BUTTON btn1 { TEXT: "Submit" }
}
```

---

## Graphics and Charts

### Line Plot
```flux
LINE_PLOT plot1 {
    WIDTH: 400
    HEIGHT: 300
    TITLE: "Sales Over Time"
    X_LABEL: "Month"
    Y_LABEL: "Sales"
    
    DATA: [
        [1, 100], [2, 150], [3, 120],
        [4, 200], [5, 180], [6, 250]
    ]
}
```

### Bar Chart
```flux
BAR_CHART chart1 {
    WIDTH: 400
    HEIGHT: 300
    TITLE: "Product Sales"
    
    CATEGORIES: ["Product A", "Product B", "Product C"]
    VALUES: [100, 150, 75]
}
```

### Pie Chart
```flux
PIE_CHART pie1 {
    WIDTH: 300
    HEIGHT: 300
    TITLE: "Market Share"
    
    DATA: [
        ["Company A", 40],
        ["Company B", 30],
        ["Company C", 20],
        ["Others", 10]
    ]
}
```

---

## System Operations

### System Commands
```flux
SYS_EXEC "notepad.exe"
SYS_OPEN "https://www.example.com"
SYS_NOTIFY "Task completed!"
```

### File System Operations
```flux
SYS_EXEC "dir"
SYS_EXEC "copy file.txt backup.txt"
```

---

## Built-in Functions

### Mathematical Functions
```flux
VAR result = ABS(-5)        # 5
VAR rounded = ROUND(3.7)    # 4
VAR floored = FLOOR(3.7)    # 3
VAR ceiled = CEIL(3.2)      # 4
VAR sqrt_val = SQRT(16)     # 4
```

### String Functions
```flux
VAR text = "Hello World"
VAR upper = UPPER(text)     # "HELLO WORLD"
VAR lower = LOWER(text)     # "hello world"
VAR length = LEN(text)      # 11
```

### List Functions
```flux
VAR numbers = [1, 2, 3, 4, 5]
VAR first = FIRST(numbers)  # 1
VAR last = LAST(numbers)    # 5
VAR size = SIZE(numbers)    # 5
```

### Type Functions
```flux
VAR x = 42
VAR type = TYPEOF(x)        # "number"
VAR is_num = INSTANCEOF(x, "number")  # TRUE
```

---

## Examples

### Complete Application Example
```flux
# Simple Calculator App
APP "Calculator" 300 400

VAR display = "0"
VAR first_num = 0
VAR operation = ""
VAR new_input = TRUE

FRAME main_frame {
    WIDTH: 280
    HEIGHT: 380
    PADDING: 10
    
    TEXTBOX display_box {
        TEXT: display
        WIDTH: 260
        HEIGHT: 40
        FONT_SIZE: 18
        READONLY: TRUE
        X: 10
        Y: 10
    }
    
    ROW button_row1 {
        Y: 60
        SPACING: 5
        
        BUTTON btn7 { TEXT: "7" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("7") } }
        BUTTON btn8 { TEXT: "8" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("8") } }
        BUTTON btn9 { TEXT: "9" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("9") } }
        BUTTON btn_div { TEXT: "/" WIDTH: 60 HEIGHT: 50 
                       ONCLICK: { set_op("/") } }
    }
    
    ROW button_row2 {
        Y: 120
        SPACING: 5
        
        BUTTON btn4 { TEXT: "4" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("4") } }
        BUTTON btn5 { TEXT: "5" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("5") } }
        BUTTON btn6 { TEXT: "6" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("6") } }
        BUTTON btn_mul { TEXT: "*" WIDTH: 60 HEIGHT: 50 
                       ONCLICK: { set_op("*") } }
    }
    
    ROW button_row3 {
        Y: 180
        SPACING: 5
        
        BUTTON btn1 { TEXT: "1" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("1") } }
        BUTTON btn2 { TEXT: "2" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("2") } }
        BUTTON btn3 { TEXT: "3" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("3") } }
        BUTTON btn_sub { TEXT: "-" WIDTH: 60 HEIGHT: 50 
                       ONCLICK: { set_op("-") } }
    }
    
    ROW button_row4 {
        Y: 240
        SPACING: 5
        
        BUTTON btn0 { TEXT: "0" WIDTH: 60 HEIGHT: 50 
                     ONCLICK: { append_digit("0") } }
        BUTTON btn_dot { TEXT: "." WIDTH: 60 HEIGHT: 50 
                       ONCLICK: { append_digit(".") } }
        BUTTON btn_eq { TEXT: "=" WIDTH: 60 HEIGHT: 50 
                      ONCLICK: { calculate() } }
        BUTTON btn_add { TEXT: "+" WIDTH: 60 HEIGHT: 50 
                       ONCLICK: { set_op("+") } }
    }
    
    BUTTON btn_clear {
        TEXT: "C"
        WIDTH: 260
        HEIGHT: 40
        Y: 300
        ONCLICK: { clear_display() }
    }
}

FUNC append_digit(digit) {
    IF new_input {
        SET display = digit
        SET new_input = FALSE
    } ELSE {
        SET display = display + digit
    }
    SET_TEXT display_box display
}

FUNC set_op(op) {
    SET first_num = TO_NUMBER(display)
    SET operation = op
    SET new_input = TRUE
}

FUNC calculate() {
    VAR second_num = TO_NUMBER(display)
    VAR result = 0
    
    IF operation == "+" {
        SET result = first_num + second_num
    } ELIF operation == "-" {
        SET result = first_num - second_num
    } ELIF operation == "*" {
        SET result = first_num * second_num
    } ELIF operation == "/" {
        SET result = first_num / second_num
    }
    
    SET display = TO_STRING(result)
    SET_TEXT display_box display
    SET new_input = TRUE
}

FUNC clear_display() {
    SET display = "0"
    SET first_num = 0
    SET operation = ""
    SET new_input = TRUE
    SET_TEXT display_box display
}
```

### Data Processing Example
```flux
# Data analysis with charts
APP "Data Analyzer" 800 600

VAR sales_data = [
    ["Jan", 100], ["Feb", 150], ["Mar", 120],
    ["Apr", 200], ["May", 180], ["Jun", 250]
]

VAR categories = []
VAR values = []

FOR item IN sales_data {
    ADD_ITEM categories item[0]
    ADD_ITEM values item[1]
}

FRAME main {
    WIDTH: 780
    HEIGHT: 580
    PADDING: 10
    
    LABEL title {
        TEXT: "Monthly Sales Analysis"
        FONT_SIZE: 20
        FONT_WEIGHT: "bold"
        X: 10
        Y: 10
    }
    
    LINE_PLOT sales_plot {
        WIDTH: 400
        HEIGHT: 300
        TITLE: "Sales Trend"
        X_LABEL: "Month"
        Y_LABEL: "Sales ($)"
        X: 10
        Y: 50
        DATA: sales_data
    }
    
    BAR_CHART sales_bar {
        WIDTH: 350
        HEIGHT: 300
        TITLE: "Sales by Month"
        X: 420
        Y: 50
        CATEGORIES: categories
        VALUES: values
    }
    
    TEXTBOX summary {
        WIDTH: 760
        HEIGHT: 200
        X: 10
        Y: 370
        READONLY: TRUE
    }
}

# Calculate statistics
VAR total = 0
VAR count = SIZE(values)

FOR val IN values {
    SET total += val
}

VAR average = total / count
VAR max_val = MAX(values)
VAR min_val = MIN(values)

SET_TEXT summary "Sales Summary:\n\n" +
    "Total Sales: $" + TO_STRING(total) + "\n" +
    "Average: $" + TO_STRING(average) + "\n" +
    "Maximum: $" + TO_STRING(max_val) + "\n" +
    "Minimum: $" + TO_STRING(min_val) + "\n" +
    "Months: " + TO_STRING(count)
```

---

## Language Reference Summary

### Keywords
- **Variables**: VAR, SET, DEL, TYPEOF, INSTANCEOF
- **Control Flow**: IF, ELIF, ELSE, WHILE, FOR, BREAK, CONTINUE
- **Functions**: FUNC, CALL, RETURN, YIELD
- **Error Handling**: TRY, CATCH, THROW, ASSERT
- **File I/O**: READ_FILE, WRITE_FILE, COPY, PASTE
- **UI Widgets**: BUTTON, LABEL, INPUT, TEXTBOX, SWITCH, SLIDER, etc.
- **Layout**: FRAME, GRID, ROW, COLUMN, PANE, etc.
- **Events**: ONCLICK, ONCHANGE, ONKEY, ONFOCUS, etc.
- **Graphics**: LINE_PLOT, BAR_CHART, PIE_CHART, etc.
- **System**: SYS_EXEC, SYS_OPEN, SYS_NOTIFY

### Data Types
- Numbers (integers, floats)
- Strings
- Booleans (TRUE, FALSE)
- Null (NULL)
- Lists

### Operators
- Arithmetic: +, -, *, /, %, **
- Comparison: ==, !=, <, <=, >, >=
- Logical: AND, OR, NOT
- Assignment: =, +=, -=, *=, /=

---

## Tips and Best Practices

1. **Use meaningful variable names**
2. **Organize code with proper indentation**
3. **Add comments for complex logic**
4. **Handle errors with TRY-CATCH blocks**
5. **Use functions to reuse code**
6. **Test UI components incrementally**
7. **Validate user input**
8. **Use appropriate widget types for data**

---

## Troubleshooting

### Common Issues

1. **Syntax Errors**
   - Check keyword casing (must be UPPERCASE)
   - Verify balanced braces and parentheses
   - Ensure proper statement termination

2. **Runtime Errors**
   - Check variable declarations before use
   - Verify file paths exist
   - Handle division by zero

3. **UI Issues**
   - Ensure widget dimensions are positive
   - Check event handler syntax
   - Verify layout constraints

### Debugging Tips

- Use PRINT statements to trace execution
- Check variable values with assertions
- Test functions independently
- Use TRY-CATCH to catch errors

---

## Conclusion

FluxUI provides a powerful yet simple way to create user interfaces and applications. With its rich widget library, event handling system, and modern syntax, it's ideal for rapid application development and prototyping.

For more examples and advanced features, refer to the test files and sample applications included with the FluxUI distribution.

## Resources

- **GitHub Repository**: https://github.com/zerogravitygamingx211-hash/FluxUI
- **Documentation**: https://fluxui-lang.org
- **Community**: https://discord.gg/fluxui

---

*FluxUI Version 1.0 - Language Reference Manual*
