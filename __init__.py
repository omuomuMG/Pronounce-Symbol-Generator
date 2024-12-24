from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from anki.hooks import addHook
from .config_manager import setting, get_field
from .phonetic_converter import  convert_word
import json


global source_field, target_field

def init():
    global source_field, target_field
    source_field = get_field()[0]
    target_field = get_field()[1]


# on button pressed
def onStrike(editor: Editor):
    global source_field, target_field
    source_field = get_field()[0]
    target_field = get_field()[1]
    convert_word(editor, source_field, target_field)


def addWeblioButton(buttons, editor):
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(addon_dir, 'SymbolIcon.png')

    editor._links['strike'] = onStrike

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


init()

addHook("setupEditorButtons", addWeblioButton)

action = QAction("Pronounce Generator Settings", mw)

# メニュー項目がクリックされたときに testFunction を呼び出すように設定
action.triggered.connect(lambda: setting(get_field()[0], get_field()[1]))

#action2.triggered.connect(lambda: convert_word(mw.editor))

# ツールメニューに追加
mw.form.menuTools.addAction(action)
