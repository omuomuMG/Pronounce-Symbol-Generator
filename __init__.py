from xmlrpc.client import boolean

from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from anki.hooks import addHook
from aqt.utils import showInfo
from .test import dic
import sys
import json


global source_field, target_field

def init():
    global source_field, target_field
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')
    json_open = open(json_path, 'r')
    json_load = json.load(json_open)
    source_field = json_load['setting']['source_field']
    target_field = json_load['setting']['target_field']
    json_open.close()


def convert_word(editor: Editor):
    if editor.note:
        note = editor.note
        symbol_text = ""
        succeeded = True
        for word in  note[source_field].split(' '):
            word = word.upper()
            if word in dic:
                if len(symbol_text) != 0:
                    symbol_text += ' '
                symbol_text += dic[word]
            else:
                succeeded = False
                showInfo(f"pronunciation: {word} wasn't found")
                break
        if succeeded:
            note[target_field] = symbol_text

        note.flush()
        QTimer.singleShot(500, lambda: editor.loadNote())


def setting():
    global source_field, target_field

    dialog = QDialog()
    dialog.setWindowTitle('Setting')
    dialog.resize(300, 200)

    layout = QVBoxLayout()

    # about source field
    source_label = QLabel("Source Field:")
    source_text = QLineEdit(f"{source_field}")
    layout.addWidget(source_label)
    layout.addWidget(source_text)

    # about target field
    target_label = QLabel("Target Field:")
    target_text = QLineEdit(f"{target_field}")
    layout.addWidget(target_label)
    layout.addWidget(target_text)


    button = QPushButton('Save')
    button.clicked.connect(dialog.accept)
    layout.addWidget(button)

    dialog.setLayout(layout)
    dialog.exec()

    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        json_load['setting']['source_field'] = source_text.text()
        json_load['setting']['target_field'] = target_text.text()

        # Move file pointer to the beginning of the file and dump updated data
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)  # Adding indent for better readability
        json_open.truncate()  # Ensure we truncate the file after writing

        source_field = source_text.text()
        target_field = target_text.text()


# on button pressed
def onStrike(editor: Editor):
    convert_word(editor)


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
action.triggered.connect(lambda: setting())
#action2.triggered.connect(lambda: convert_word(mw.editor))

# ツールメニューに追加
mw.form.menuTools.addAction(action)
