# FluxUI Programming Language
## Complete Instruction Book

---

# 📚 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Installation](#installation)
4. [Language Basics](#language-basics)
5. [UI Components](#ui-components)
6. [Events and Interactions](#events-and-interactions)
7. [Advanced Features](#advanced-features)
8. [Project Structure](#project-structure)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)

---

# 🌟 Introduction

## What is FluxUI?

FluxUI is a modern programming language designed specifically for creating beautiful user interfaces with ease. It combines the simplicity of declarative UI design with the power of event-driven programming.

## Key Features

- ✅ **Simple, readable syntax** - Easy to learn and use
- ✅ **Rich component library** - Pre-built UI elements
- ✅ **Event-driven programming** - Responsive and interactive
- ✅ **Built-in graphics** - Charts, graphs, and visualizations
- ✅ **Cross-platform** - Works on Windows, macOS, and Linux
- ✅ **Modern IDE** - Syntax highlighting and tools
- ✅ **Global tools** - Command-line utilities

## Why FluxUI?

Traditional UI programming often requires:
- Complex boilerplate code
- Steep learning curves
- Verbose syntax
- Multiple files and configurations

FluxUI eliminates these problems with:
- **Single-file applications** - Everything in one .flux file
- **Declarative syntax** - Describe what you want, not how
- **Built-in components** - No need to import external libraries
- **Automatic layout** - Smart positioning and sizing

---

# 🚀 Getting Started

## Your First Program

Create a file called `hello.flux`:

```flux
# Hello World Program
APP "Hello World" 400 300

LABEL greeting {
    TEXT: "Hello, FluxUI!"
    FONT_SIZE: 16
    X: 20
    Y: 20
}

BUTTON exit_btn {
    TEXT: "Exit"
    X: 20
    Y: 60
    ONCLICK: {
        EXIT
    }
}
```

Run it:
```bash
fluxui hello.flux
```

## Understanding the Structure

Every FluxUI program has these parts:

1. **APP Declaration** - Window title and size
2. **Components** - UI elements
3. **Events** - User interactions
4. **Logic** - Program behavior

---

# 📦 Installation

## Method 1: Simple Installer (Recommended)

1. Download: https://github.com/zerogravitygamingx211-hash/FluxUI
2. Get `FluxUI_Installer.exe` from repository
3. Double-click to run
4. Follow simple installation steps

## Method 2: Online Installer

1. Download: https://github.com/zerogravitygamingx211-hash/FluxUI/releases
2. Get `FluxUI_Online_Installer.exe`
3. Run as administrator
4. Follow 5-step wizard

## Method 3: Complete Installer

1. Download: https://github.com/zerogravitygamingx211-hash/FluxUI/releases
2. Get `FluxUI_Installer.exe` (complete version)
3. Run as administrator
4. Complete installation

## Method 4: Manual Installation

1. Clone repository:
   ```bash
   git clone https://github.com/zerogravitygamingx211-hash/FluxUI.git
   cd FluxUI
   ```
2. Install Python dependencies
3. Add to PATH or run directly

## Verification

Test installation:
```bash
fluxui --ver
```

Should output: `FluxUI Beta 1.0`

---

# 📖 Language Basics

## Basic Syntax

FluxUI uses a clean, readable syntax inspired by modern programming languages:

```flux
# Comments start with #
COMPONENT_NAME {
    PROPERTY: value
    ANOTHER_PROPERTY: value
    EVENT_HANDLER: {
        # Code here
    }
}
```

## Data Types

### Strings
```flux
TEXT: "Hello, World!"
TITLE: "My Application"
```

### Numbers
```flux
WIDTH: 400
HEIGHT: 300
FONT_SIZE: 16
OPACITY: 0.8
```

### Booleans
```flux
VISIBLE: true
ENABLED: false
```

### Colors
```flux
COLOR: "#FF0000"    # Red
BACKGROUND: "#FFFFFF" # White
BORDER_COLOR: "#000000" # Black
```

## Variables

```flux
# Global variables
VAR title = "My App"
VAR width = 400
VAR height = 300

# Use variables in components
APP title width height

LABEL header {
    TEXT: title
    WIDTH: width
}
```

## Expressions

### Arithmetic
```flux
WIDTH: 400 + 50
HEIGHT: 300 * 2
OPACITY: 1.0 - 0.2
```

### String Operations
```flux
TEXT: "Hello, " + "World!"
TITLE: "App v" + "1.0"
```

---

# 🎨 UI Components

## APP (Window)

The main application window:

```flux
APP "Window Title" width height
```

**Properties:**
- First parameter: Window title (string)
- Second parameter: Width (number)
- Third parameter: Height (number)

## LABEL

Text display component:

```flux
LABEL name {
    TEXT: "Hello, World!"
    X: 20
    Y: 20
    WIDTH: 200
    HEIGHT: 30
    FONT_SIZE: 16
    COLOR: "#000000"
    BACKGROUND: "#FFFFFF"
    ALIGN: "center"
}
```

**Properties:**
- `TEXT` - Text content
- `X`, `Y` - Position
- `WIDTH`, `HEIGHT` - Size
- `FONT_SIZE` - Text size
- `COLOR` - Text color
- `BACKGROUND` - Background color
- `ALIGN` - Text alignment ("left", "center", "right")

## BUTTON

Clickable button:

```flux
BUTTON name {
    TEXT: "Click Me"
    X: 20
    Y: 60
    WIDTH: 100
    HEIGHT: 40
    ONCLICK: {
        PRINT "Button clicked!"
    }
}
```

**Properties:**
- `TEXT` - Button text
- `X`, `Y` - Position
- `WIDTH`, `HEIGHT` - Size
- `ONCLICK` - Click event handler

## INPUT

Text input field:

```flux
INPUT name {
    PLACEHOLDER: "Enter text here"
    X: 20
    Y: 120
    WIDTH: 200
    HEIGHT: 30
    ONCHANGE: {
        PRINT "Text changed: " + VALUE
    }
}
```

**Properties:**
- `PLACEHOLDER` - Placeholder text
- `VALUE` - Current text value
- `X`, `Y` - Position
- `WIDTH`, `HEIGHT` - Size
- `ONCHANGE` - Change event handler

## CHECKBOX

Toggle checkbox:

```flux
CHECKBOX name {
    TEXT: "Enable feature"
    X: 20
    Y: 160
    CHECKED: false
    ONTOGGLE: {
        PRINT "Checkbox state: " + CHECKED
    }
}
```

## RADIO

Radio button group:

```flux
RADIO name {
    OPTIONS: ["Option 1", "Option 2", "Option 3"]
    SELECTED: 0
    X: 20
    Y: 200
    ONCHANGE: {
        PRINT "Selected: " + SELECTED
    }
}
```

## IMAGE

Image display:

```flux
IMAGE name {
    SOURCE: "logo.png"
    X: 20
    Y: 240
    WIDTH: 100
    HEIGHT: 100
}
```

## PROGRESS

Progress bar:

```flux
PROGRESS name {
    VALUE: 50
    MAX: 100
    X: 20
    Y: 360
    WIDTH: 200
    HEIGHT: 20
}
```

---

# ⚡ Events and Interactions

## Event Types

### Mouse Events
```flux
ONCLICK: {
    # Mouse click
}

ONHOVER: {
    # Mouse enters component
}

ONLEAVE: {
    # Mouse leaves component
}
```

### Keyboard Events
```flux
ONKEYPRESS: {
    # Key pressed
    PRINT "Key: " + KEY
}

ONKEYDOWN: {
    # Key down
}

ONKEYUP: {
    # Key up
}
```

### Change Events
```flux
ONCHANGE: {
    # Value changed
}

ONTOGGLE: {
    # Checkbox toggled
}

ONSELECT: {
    # Selection changed
}
```

## Event Handlers

Event handlers contain FluxUI code:

```flux
BUTTON calculate {
    TEXT: "Calculate"
    ONCLICK: {
        VAR result = 10 + 5
        PRINT "Result: " + result
        
        # Update UI
        result_label.TEXT = "Result: " + result
    }
}

LABEL result_label {
    TEXT: "Result: "
    X: 20
    Y: 60
}
```

## Built-in Functions

### Output Functions
```flux
PRINT "Hello, World!"        # Print to console
ALERT "Message"               # Show alert dialog
LOG "Debug info"              # Log to file
```

### UI Functions
```flux
EXIT                         # Close application
SHOW component_name          # Show component
HIDE component_name          # Hide component
ENABLE component_name        # Enable component
DISABLE component_name       # Disable component
```

### Math Functions
```flux
ABS(-5)                      # Absolute value: 5
MIN(10, 5)                   # Minimum: 5
MAX(10, 5)                   # Maximum: 10
SQRT(16)                     # Square root: 4
POW(2, 3)                    # Power: 8
```

---

# 🔧 Advanced Features

## Layout Management

### Automatic Layout
```flux
# Components auto-arrange
CONTAINER {
    LAYOUT: "vertical"
    SPACING: 10
    
    LABEL { TEXT: "Item 1" }
    LABEL { TEXT: "Item 2" }
    LABEL { TEXT: "Item 3" }
}
```

### Grid Layout
```flux
CONTAINER {
    LAYOUT: "grid"
    COLUMNS: 2
    ROWS: 2
    
    LABEL { TEXT: "Cell 1" }
    LABEL { TEXT: "Cell 2" }
    LABEL { TEXT: "Cell 3" }
    LABEL { TEXT: "Cell 4" }
}
```

## Styling and Themes

### CSS-like Styling
```flux
BUTTON {
    BACKGROUND: "#007ACC"
    COLOR: "#FFFFFF"
    BORDER_RADIUS: 5
    PADDING: 10
}

.special_button {
    BACKGROUND: "#28A745"
    FONT_SIZE: 18
}
```

### Dark Mode
```flux
THEME: "dark"

# Or custom theme
THEME {
    BACKGROUND: "#1E1E1E"
    TEXT: "#FFFFFF"
    ACCENT: "#007ACC"
}
```

## Animations

### Basic Animation
```flux
BUTTON {
    ONHOVER: {
        ANIMATE {
            PROPERTY: "OPACITY"
            FROM: 1.0
            TO: 0.8
            DURATION: 200
        }
    }
    
    ONLEAVE: {
        ANIMATE {
            PROPERTY: "OPACITY"
            FROM: 0.8
            TO: 1.0
            DURATION: 200
        }
    }
}
```

## Data Binding

### Two-way Binding
```flux
INPUT name_input {
    PLACEHOLDER: "Enter name"
    BIND: "user_name"
}

LABEL greeting {
    TEXT: "Hello, " + user_name
}
```

---

# 📁 Project Structure

## Single File Structure

Simple applications can be in one file:

```
myapp.flux
├── APP declaration
├── Components
├── Events
└── Logic
```

## Multi-file Structure

For larger projects:

```
myproject/
├── main.flux          # Main application
├── components/
│   ├── header.flux
│   ├── sidebar.flux
│   └── footer.flux
├── data/
│   ├── config.json
│   └── users.json
└── assets/
    ├── images/
    ├── icons/
    └── fonts/
```

## Including Files

```flux
# Include other .flux files
INCLUDE "components/header.flux"
INCLUDE "components/sidebar.flux"

# Include data
LOAD "data/config.json"
```

---

# 💡 Examples

## Example 1: Calculator

```flux
# Calculator App
APP "Calculator" 300 400

# Display
LABEL display {
    TEXT: "0"
    X: 20
    Y: 20
    WIDTH: 260
    HEIGHT: 50
    FONT_SIZE: 24
    ALIGN: "right"
    BACKGROUND: "#F0F0F0"
}

# Number buttons
BUTTON btn7 { TEXT: "7" X: 20 Y: 90 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("7") } }
BUTTON btn8 { TEXT: "8" X: 90 Y: 90 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("8") } }
BUTTON btn9 { TEXT: "9" X: 160 Y: 90 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("9") } }
BUTTON btn_div { TEXT: "/" X: 220 Y: 90 WIDTH: 60 HEIGHT: 60 ONCLICK: { set_operation("/") } }

BUTTON btn4 { TEXT: "4" X: 20 Y: 160 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("4") } }
BUTTON btn5 { TEXT: "5" X: 90 Y: 160 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("5") } }
BUTTON btn6 { TEXT: "6" X: 160 Y: 160 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("6") } }
BUTTON btn_mul { TEXT: "*" X: 220 Y: 160 WIDTH: 60 HEIGHT: 60 ONCLICK: { set_operation("*") } }

BUTTON btn1 { TEXT: "1" X: 20 Y: 230 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("1") } }
BUTTON btn2 { TEXT: "2" X: 90 Y: 230 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("2") } }
BUTTON btn3 { TEXT: "3" X: 160 Y: 230 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("3") } }
BUTTON btn_sub { TEXT: "-" X: 220 Y: 230 WIDTH: 60 HEIGHT: 60 ONCLICK: { set_operation("-") } }

BUTTON btn0 { TEXT: "0" X: 20 Y: 300 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number("0") } }
BUTTON btn_dot { TEXT: "." X: 90 Y: 300 WIDTH: 60 HEIGHT: 60 ONCLICK: { append_number(".") } }
BUTTON btn_eq { TEXT: "=" X: 160 Y: 300 WIDTH: 60 HEIGHT: 60 ONCLICK: { calculate() } }
BUTTON btn_add { TEXT: "+" X: 220 Y: 300 WIDTH: 60 HEIGHT: 60 ONCLICK: { set_operation("+") } }

# Variables
VAR current_value = "0"
VAR operation = ""
VAR previous_value = ""

# Functions
FUNCTION append_number(num) {
    IF current_value == "0" {
        current_value = num
    } ELSE {
        current_value = current_value + num
    }
    display.TEXT = current_value
}

FUNCTION set_operation(op) {
    previous_value = current_value
    operation = op
    current_value = "0"
}

FUNCTION calculate() {
    VAR result = 0
    VAR prev = NUMBER(previous_value)
    VAR curr = NUMBER(current_value)
    
    IF operation == "+" { result = prev + curr }
    IF operation == "-" { result = prev - curr }
    IF operation == "*" { result = prev * curr }
    IF operation == "/" { result = prev / curr }
    
    display.TEXT = STRING(result)
    current_value = STRING(result)
    operation = ""
}
```

## Example 2: Todo List

```flux
# Todo List App
APP "Todo List" 400 500

# Input section
LABEL title {
    TEXT: "My Todo List"
    X: 20
    Y: 20
    FONT_SIZE: 20
    FONT_WEIGHT: "bold"
}

INPUT new_todo {
    PLACEHOLDER: "Add new todo..."
    X: 20
    Y: 60
    WIDTH: 280
    HEIGHT: 40
    ONKEYPRESS: {
        IF KEY == "Enter" {
            add_todo()
        }
    }
}

BUTTON add_btn {
    TEXT: "Add"
    X: 310
    Y: 60
    WIDTH: 70
    HEIGHT: 40
    ONCLICK: { add_todo() }
}

# Todo list
CONTAINER todo_list {
    X: 20
    Y: 120
    WIDTH: 360
    HEIGHT: 350
    LAYOUT: "vertical"
    SPACING: 5
}

# Data
VAR todos = []
VAR todo_id = 0

# Functions
FUNCTION add_todo() {
    VAR text = new_todo.VALUE
    IF text != "" {
        VAR id = todo_id
        todo_id = todo_id + 1
        
        # Add to array
        todos = todos + [{id: id, text: text, done: false}]
        
        # Create UI
        create_todo_item(id, text)
        
        # Clear input
        new_todo.VALUE = ""
    }
}

FUNCTION create_todo_item(id, text) {
    CONTAINER {
        ID: "todo_" + id
        LAYOUT: "horizontal"
        SPACING: 10
        
        CHECKBOX {
            ID: "check_" + id
            ONTOGGLE: { toggle_todo(id) }
        }
        
        LABEL {
            TEXT: text
            WIDTH: 250
        }
        
        BUTTON {
            TEXT: "Delete"
            ONCLICK: { delete_todo(id) }
        }
    }
}

FUNCTION toggle_todo(id) {
    # Find and update todo
    FOR i IN 0 TO LENGTH(todos) - 1 {
        IF todos[i].id == id {
            todos[i].done = NOT todos[i].done
            BREAK
        }
    }
}

FUNCTION delete_todo(id) {
    # Remove from array
    VAR new_todos = []
    FOR todo IN todos {
        IF todo.id != id {
            new_todos = new_todos + [todo]
        }
    }
    todos = new_todos
    
    # Remove from UI
    REMOVE "todo_" + id
}
```

## Example 3: Weather App

```flux
# Weather App
APP "Weather" 350 500

# Location input
LABEL location_label {
    TEXT: "Enter city:"
    X: 20
    Y: 20
}

INPUT location_input {
    PLACEHOLDER: "New York"
    X: 20
    Y: 50
    WIDTH: 200
    HEIGHT: 40
}

BUTTON get_weather {
    TEXT: "Get Weather"
    X: 230
    Y: 50
    WIDTH: 100
    HEIGHT: 40
    ONCLICK: { fetch_weather() }
}

# Weather display
CONTAINER weather_display {
    X: 20
    Y: 110
    WIDTH: 310
    HEIGHT: 370
    VISIBLE: false
    
    LABEL city_name {
        TEXT: ""
        FONT_SIZE: 24
        FONT_WEIGHT: "bold"
        X: 0
        Y: 0
    }
    
    LABEL temperature {
        TEXT: ""
        FONT_SIZE: 48
        X: 0
        Y: 40
    }
    
    LABEL description {
        TEXT: ""
        FONT_SIZE: 16
        X: 0
        Y: 100
    }
    
    LABEL humidity {
        TEXT: ""
        X: 0
        Y: 140
    }
    
    LABEL wind {
        TEXT: ""
        X: 0
        Y: 170
    }
}

# Functions
FUNCTION fetch_weather() {
    VAR city = location_input.VALUE
    IF city == "" {
        ALERT "Please enter a city name"
        RETURN
    }
    
    # Simulate API call
    weather_display.VISIBLE = true
    city_name.TEXT = city
    temperature.TEXT = "72°F"
    description.TEXT = "Partly Cloudy"
    humidity.TEXT = "Humidity: 65%"
    wind.TEXT = "Wind: 10 mph"
}
```

---

# 🔧 Troubleshooting

## Common Issues

### Installation Problems

**Issue:** `fluxui: command not found`
**Solution:** 
1. Restart command prompt
2. Check PATH: `echo %PATH%`
3. Manual PATH: `set PATH=%PATH%;C:\Program Files\FluxUI\bin`

**Issue:** "Administrator privileges required"
**Solution:** Right-click installer and "Run as administrator"

### Runtime Errors

**Issue:** "File not found"
**Solution:** Check file path and extension (.flux)

**Issue:** "Syntax error"
**Solution:** Check brackets, quotes, and commas

**Issue:** "Component not found"
**Solution:** Ensure component names are unique

### Performance Issues

**Issue:** Slow startup
**Solution:** Check for large images or complex layouts

**Issue:** Memory usage
**Solution:** Limit number of components and images

## Debug Tips

### Console Output
```flux
# Use PRINT for debugging
PRINT "Debug: Variable value = " + variable
PRINT "Debug: Function called"
```

### Component Inspection
```flux
# Check component properties
PRINT "Button width: " + my_button.WIDTH
PRINT "Label text: " + my_label.TEXT
```

### Error Handling
```flux
TRY {
    # Code that might fail
    result = risky_operation()
} CATCH error {
    PRINT "Error: " + error
}
```

## Getting Help

### Resources
- **GitHub:** https://github.com/zerogravitygamingx211-hash/FluxUI
- **Documentation:** FluxUI_Language_Reference.md
- **Examples:** samples/ folder

### Community
- **Issues:** Report bugs on GitHub
- **Discussions:** Ask questions on GitHub Discussions
- **Updates:** Check repository for new versions

---

# 🎯 Conclusion

FluxUI makes UI programming simple and enjoyable. With its clean syntax, rich components, and powerful features, you can create beautiful applications quickly.

## Next Steps

1. **Build your first app** - Start with a simple calculator
2. **Explore components** - Try different UI elements
3. **Add interactivity** - Implement events and logic
4. **Style your app** - Use themes and animations
5. **Share your work** - Publish your applications

## Remember

- **Start simple** - Don't try to build everything at once
- **Test often** - Run your code frequently to catch errors
- **Use examples** - Learn from existing code
- **Ask for help** - Join the community

Happy coding with FluxUI! 🚀

---

**FluxUI vBeta 1.0**  
**Author:** ZeroGravityGamingX211  
**License:** MIT License  
**Repository:** https://github.com/zerogravitygamingx211-hash/FluxUI
