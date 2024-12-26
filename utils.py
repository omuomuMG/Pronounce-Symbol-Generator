from aqt.qt import *
from aqt.editor import Editor
from .config_manager import  get_field
from .phonetic_converter import  convert_word


def on_strike(editor: Editor):
    source_field = get_field()[0]
    target_field = get_field()[1]
    convert_word(editor, source_field, target_field)


def add_symbol_button(buttons, editor):
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(addon_dir, 'resources/SymbolIcon.png')

    editor._links['strike'] = on_strike

    button = editor._addButton(
        icon_path,  # Button icon
        "strike",  # Button name
        "strike"  # Button label
    )

    # Check if the returned object is a QPushButton
    if isinstance(button, QPushButton):
        # Set the style if the button is of the correct type
        button.setStyleSheet("""
            QPushButton {
                width: 40px;  # Set width
                height: 40px;  # Set height
                padding: 0px;  # Remove padding
            }
            QPushButton:pressed {
                background-color: #dddddd;  # Background color when pressed
            }
        """)
    else:
        print("Error: The returned button is not a QPushButton.")

    return buttons + [button]