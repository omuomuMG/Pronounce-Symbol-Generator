from xmlrpc.client import boolean

from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from anki.hooks import addHook
from aqt.utils import showInfo
from .test import dic
import sys

source_field = "表面"
target_field = "表面"




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

        # 変更をデータベースに保存
        note.flush()
        # UIの更新を強制的に行うために少し待機してからエディタをリロード

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


    button = QPushButton('Close')
    button.clicked.connect(dialog.accept)
    layout.addWidget(button)

    dialog.setLayout(layout)
    dialog.exec()

    source_field = source_text.text()
    target_field= target_text.text()


# エディタのボタンに関連付ける関数
def onStrike(editor: Editor):
    convert_word(editor)


# カスタムボタンをエディタに追加する関数
def addWeblioButton(buttons, editor):
    # エディタに「ストライク」ボタンを追加
    editor._links['strike'] = onStrike
    return buttons + [editor._addButton(
        "image.png",  # ボタンの画像ファイル（適宜変更）
        "strike",  # ボタンの名前
        "weblio"  # ボタンのラベル
    )]


# エディタにボタンを追加するフック
addHook("setupEditorButtons", addWeblioButton)

# 新しいメニュー項目 "test" を作成
action = QAction("test", mw)
action2 = QAction("test2", mw)

# メニュー項目がクリックされたときに testFunction を呼び出すように設定
action.triggered.connect(lambda: setting())
action2.triggered.connect(lambda: convert_word(mw.editor))

# ツールメニューに追加
mw.form.menuTools.addAction(action)
mw.form.menuTools.addAction(action2)
