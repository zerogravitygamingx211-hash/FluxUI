# UI Application
APP "{{project_name}}" 800 600

VAR counter = 0

FRAME main_frame {
    WIDTH: 780
    HEIGHT: 580
    PADDING: 10
    
    LABEL title {
        TEXT: "{{project_name}}"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }
    
    ROW controls {
        Y: 50
        SPACING: 10
        
        BUTTON increment_btn {
            TEXT: "Increment"
            ONCLICK: {
                SET counter += 1
                SET_TEXT counter_label "Count: " + counter
            }
        }
        
        BUTTON decrement_btn {
            TEXT: "Decrement"
            ONCLICK: {
                SET counter -= 1
                SET_TEXT counter_label "Count: " + counter
            }
        }
    }
    
    LABEL counter_label {
        TEXT: "Count: 0"
        FONT_SIZE: 14
        X: 10
        Y: 100
    }
}
