# FluxUI Programming Language Reference

## Table of Contents

1. [Language Overview](#language-overview)
2. [Syntax Reference](#syntax-reference)
3. [Built-in Functions](#built-in-functions)
4. [UI Components](#ui-components)
5. [Event Handling](#event-handling)
6. [Data Types](#data-types)
7. [Control Flow](#control-flow)
8. [File Operations](#file-operations)
9. [Examples](#examples)

## Language Overview

FluxUI is a modern programming language designed for creating user interfaces with ease. It combines simple syntax with powerful UI capabilities.

### Key Features
- Event-driven programming
- Rich UI component library
- Modern, readable syntax
- Cross-platform support

## Syntax Reference

### Basic Structure
```flux
APP "Application Title" width height

# UI components and logic here
```

### Variable Declaration
```flux
VAR variable_name = value
LET variable_name = value
CONST variable_name = value
```

### UI Components
```flux
LABEL component_name {
    property: value
    property: value
}
```

## Built-in Functions

### System Functions
- `PRINT expression` - Output to console
- `INPUT prompt` - Get user input
- `SYS_EXEC command` - Execute system command
- `SYS_OPEN path` - Open file/application

### UI Functions
- `SHOW component` - Show UI component
- `HIDE component` - Hide UI component
- `SET_TEXT component text` - Set component text
- `GET_TEXT component` - Get component text

## UI Components

### Layout Components
- `WINDOW` - Main application window
- `FRAME` - Container for other components
- `ROW` - Horizontal layout
- `COLUMN` - Vertical layout
- `GRID` - Grid layout

### Basic Components
- `LABEL` - Text display
- `BUTTON` - Clickable button
- `INPUT` - Text input field
- `TEXTBOX` - Multi-line text input
- `SWITCH` - Toggle switch
- `SLIDER` - Numeric slider
- `PROGRESS` - Progress bar

### Advanced Components
- `DROPDOWN` - Selection dropdown
- `LISTBOX` - Item list
- `TREEVIEW` - Tree structure
- `TABLE` - Data table
- `CANVAS` - Drawing area

## Event Handling

### Event Types
```flux
BUTTON btn {
    TEXT: "Click Me"
    ONCLICK: {
        # Handle click event
        PRINT "Button clicked!"
    }
    ONCHANGE: {
        # Handle value change
    }
    ONHOVER: {
        # Handle mouse hover
    }
}
```

### Common Events
- `ONCLICK` - Click event
- `ONCHANGE` - Value change
- `ONHOVER` - Mouse hover
- `ONKEY` - Key press
- `ONFOCUS` - Focus gained
- `ONBLUR` - Focus lost

## Data Types

### Primitive Types
- `STRING` - Text values
- `NUMBER` - Numeric values
- `BOOLEAN` - True/False values
- `NULL` - Null/empty value

### Collections
- `LIST` - Ordered collection
- `DICT` - Key-value pairs

## Control Flow

### Conditional Statements
```flux
IF condition {
    # Code to execute
} ELSE {
    # Alternative code
}
```

### Loops
```flux
WHILE condition {
    # Loop code
}

FOR variable IN collection {
    # Loop code
}
```

### Functions
```flux
FUNC function_name(param1, param2) {
    # Function body
    RETURN result
}
```

## File Operations

### Reading Files
```flux
VAR content = READ_FILE "path/to/file.txt"
```

### Writing Files
```flux
WRITE_FILE "path/to/file.txt" content
```

### File System
```flux
IF FILE_EXISTS "path/to/file.txt" {
    PRINT "File exists"
}
```

## Examples

### Hello World
```flux
APP "Hello World" 400 300

LABEL greeting {
    TEXT: "Hello, FluxUI!"
    FONT_SIZE: 16
    X: 20
    Y: 20
}
```

### Interactive Counter
```flux
APP "Counter" 300 200

VAR count = 0

LABEL title {
    TEXT: "Counter Application"
    FONT_SIZE: 18
    X: 20
    Y: 20
}

LABEL count_label {
    TEXT: "Count: 0"
    FONT_SIZE: 14
    X: 20
    Y: 60
}

BUTTON increment {
    TEXT: "+"
    X: 20
    Y: 100
    ONCLICK: {
        SET count += 1
        SET_TEXT count_label "Count: " + count
    }
}
```

### Form Example
```flux
APP "User Form" 400 500

FRAME form {
    WIDTH: 380
    HEIGHT: 480
    PADDING: 10
    
    LABEL title {
        TEXT: "User Information"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }
    
    LABEL name_label {
        TEXT: "Name:"
        X: 10
        Y: 50
    }
    
    INPUT name_input {
        WIDTH: 200
        X: 10
        Y: 70
    }
    
    BUTTON submit {
        TEXT: "Submit"
        X: 10
        Y: 100
        ONCLICK: {
            VAR name = GET_TEXT name_input
            PRINT "Submitted: " + name
        }
    }
}
```

## Component Properties

### Common Properties
- `TEXT` - Display text
- `WIDTH` - Component width
- `HEIGHT` - Component height
- `X` - X position
- `Y` - Y position
- `BG` - Background color
- `FG` - Foreground color
- `FONT_SIZE` - Text size
- `FONT_FAMILY` - Font family

### Layout Properties
- `PADDING` - Internal spacing
- `MARGIN` - External spacing
- `ANCHOR` - Position anchor
- `EXPAND` - Expand to fill space

## Color Values

Colors can be specified as:
- Hex: `#RRGGBB` (e.g., `#FF0000` for red)
- Names: `RED`, `BLUE`, `GREEN`, etc.
- RGB: `RGB(255, 0, 0)`

## Best Practices

1. **Use meaningful variable names**
2. **Organize UI with frames and layouts**
3. **Handle events properly**
4. **Test components individually**
5. **Use comments for complex logic**

## Error Handling

```flux
TRY {
    # Code that might fail
    VAR result = RISKY_OPERATION()
} CATCH error {
    PRINT "Error: " + error
}
```

## Advanced Topics

### Custom Components
You can create reusable UI components by defining templates and reusing them.

### Data Binding
FluxUI supports data binding between UI components and variables.

### Animations
Basic animations can be created using timers and property updates.

---

## Additional Resources

- **GitHub Repository**: https://github.com/zerogravitygamingx211-hash/FluxUI
- **Main Documentation**: FluxUI_Language_Reference.md
- **Sample Code**: samples/ directory
- **Templates**: templates/ directory

---

*FluxUI Version Beta 1.0 - Comprehensive Reference*
*Author: ZeroGravityGamingX211*
*License: MIT License*
