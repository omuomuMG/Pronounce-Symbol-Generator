import json
from aqt.qt import *


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


def get_field():
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        source_field = json_load['setting']['source_field']
        target_field = json_load['setting']['target_field']

        # Move file pointer to the beginning of the file and dump updated data
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
    return  source_field, target_field