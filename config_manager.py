import json
import os
from aqt.qt import *
from pathlib import Path
from aqt import mw


def setting(source_field, target_field):

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

    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "pronounce_symbol_generator.json"

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        json_load['setting']['source_field'] = source_text.text()
        json_load['setting']['target_field'] = target_text.text()

        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()


def get_field():
    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "pronounce_symbol_generator.json"

    # If the config file does not exist, create it with default settings.
    if not json_path.exists():
        default_config = {"setting": {"source_field": "Front", "target_field": "Back"}}
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)

    with open(json_path, 'r+', encoding='utf-8') as json_open:
        content = json_open.read()
        if not content.strip():
            json_load = {"setting": {"source_field": "", "target_field": ""}}
        else:
            try:
                json_load = json.loads(content)
            except json.JSONDecodeError:
                json_load = {"setting": {"source_field": "", "target_field": ""}}

        # Ensure the 'setting' key exists.
        if 'setting' not in json_load:
            json_load['setting'] = {"source_field": "", "target_field": ""}

        source_field = json_load['setting'].get('source_field', '')
        target_field = json_load['setting'].get('target_field', '')

        # Move file pointer to the beginning of the file and dump updated data.
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
    return source_field, target_field