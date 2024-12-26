from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from .utils import add_symbol_button
from .config_manager import setting, get_field


addHook("setupEditorButtons", add_symbol_button)

action = QAction("Pronounce Generator Settings", mw)


action.triggered.connect(lambda: setting(get_field()[0], get_field()[1]))


mw.form.menuTools.addAction(action)
