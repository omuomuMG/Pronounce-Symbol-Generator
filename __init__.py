from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from anki.hooks import addHook
from aqt.utils import showInfo

from .test import dic


source_field = "表面"
target_field = "表面"


def testFunction(editor: Editor):
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


# エディタのボタンに関連付ける関数
def onStrike(editor: Editor):
    testFunction(editor)


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
action.triggered.connect(lambda: testFunction(mw.editor))
action2.triggered.connect(lambda: testFunction(mw.editor))

# ツールメニューに追加
mw.form.menuTools.addAction(action)
mw.form.menuTools.addAction(action2)
