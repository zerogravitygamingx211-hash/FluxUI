# Test file for FluxUI.exe
APP "Test Executable" 300 200

LABEL title {
    TEXT: "FluxUI.exe Test"
    FONT_SIZE: 16
    X: 20
    Y: 20
}

LABEL status {
    TEXT: "Running from FluxUI.exe"
    FONT_SIZE: 12
    X: 20
    Y: 60
}

BUTTON test_btn {
    TEXT: "Test Button"
    X: 20
    Y: 100
    ONCLICK: {
        PRINT "Button clicked in FluxUI.exe!"
        SET_TEXT status "Button was clicked!"
    }
}

PRINT "Test file executed successfully by FluxUI.exe"
