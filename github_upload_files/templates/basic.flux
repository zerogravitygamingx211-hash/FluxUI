# Basic FluxUI Application
APP "{{project_name}}" 400 300

VAR message = "Hello, FluxUI!"

LABEL title {
    TEXT: message
    FONT_SIZE: 16
    X: 20
    Y: 20
}

BUTTON btn {
    TEXT: "Click Me"
    X: 20
    Y: 60
    ONCLICK: {
        PRINT "Button clicked!"
        SET message = "Button was clicked!"
        SET_TEXT title message
    }
}
