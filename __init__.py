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
        for word in  note[source_field].split(' '):
            word = word.upper()
            if word in dic:
                if len(symbol_text) != 0:
                    symbol_text += ' '
                symbol_text += dic[word]
            else:
                showInfo(f"pronunciation: {word} wasn't found")
                break

        note[target_field] = symbol_text

        # 変更をデータベースに保存
        note.flush()
        # UIの更新を強制的に行うために少し待機してからエディタをリロード
        QTimer.singleShot(500, lambda: editor.loadNote())


class Madoka(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('空っぽな窓')  # ウィンドウのタイトル
        self.setGeometry(100, 100, 200, 150)  # ウィンドウの位置と大きさ

def setting():
    # QDialog を使ってダイアログを表示
    dialog = QDialog()
    dialog.setWindowTitle('サンプルダイアログ')
    dialog.resize(250, 150)

    button = QPushButton('閉じる', dialog)
    button.clicked.connect(dialog.accept)

    dialog.exec()


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
