import os
from PyQt6.QtCore import QTimer
from aqt.utils import showInfo
from aqt.editor import Editor
from .config_manager import  get_field

converter = {
    "AO": "ɔ",
    "AO0": "ɔ",
    "AO1": "ɔ",
    "AO2": "ɔ",
    "AA": "ɑ",
    "AA0": "ɑ",
    "AA1": "ɑ",
    "AA2": "ɑ",
    "IY": "i",
    "IY0": "i",
    "IY1": "i",
    "IY2": "i",
    "UW": "u",
    "UW0": "u",
    "UW1": "u",
    "UW2": "u",
    "EH": "e",
    "EH0": "e",
    "EH1": "e",
    "EH2": "e",
    "IH": "ɪ",
    "IH0": "ɪ",
    "IH1": "ɪ",
    "IH2": "ɪ",
    "UH": "ʊ",
    "UH0": "ʊ",
    "UH1": "ʊ",
    "UH2": "ʊ",
    "AH": "ʌ",
    "AH0": "ə",
    "AH1": "ʌ",
    "AH2": "ʌ",
    "AE": "æ",
    "AE0": "æ",
    "AE1": "æ",
    "AE2": "æ",
    "AX": "ə",
    "AX0": "ə",
    "AX1": "ə",
    "AX2": "ə",
    "EY": "eɪ",
    "EY0": "eɪ",
    "EY1": "eɪ",
    "EY2": "eɪ",
    "AY": "aɪ",
    "AY0": "aɪ",
    "AY1": "aɪ",
    "AY2": "aɪ",
    "OW": "oʊ",
    "OW0": "oʊ",
    "OW1": "oʊ",
    "OW2": "oʊ",
    "AW": "aʊ",
    "AW0": "aʊ",
    "AW1": "aʊ",
    "AW2": "aʊ",
    "OY": "ɔɪ",
    "OY0": "ɔɪ",
    "OY1": "ɔɪ",
    "OY2": "ɔɪ",
    "P": "p",
    "B": "b",
    "T": "t",
    "D": "d",
    "K": "k",
    "G": "ɡ",
    "CH": "tʃ",
    "JH": "dʒ",
    "F": "f",
    "V": "v",
    "TH": "θ",
    "DH": "ð",
    "S": "s",
    "Z": "z",
    "SH": "ʃ",
    "ZH": "ʒ",
    "HH": "h",
    "M": "m",
    "N": "n",
    "NG": "ŋ",
    "L": "l",
    "R": "r",
    "ER": "ɜr",
    "ER0": "ɜr",
    "ER1": "ɜr",
    "ER2": "ɜr",
    "AXR": "ər",
    "AXR0": "ər",
    "AXR1": "ər",
    "AXR2": "ər",
    "AW R": "aʊr",
    "EH R": "ɛr",
    "UH R": "ʊr",
    "AO R": "ɔr",
    "AA R": "ɑr",
    "IY R": "ɪr",
    "W": "w",
    "Y": "j",
    "T_flap": "ɾ",
    "D_flap": "ɾ",
    "?": "ʔ",
    "IY1_long": "iː",
    "IY0_long": "iː",
    "UW1_long": "uː",
    "UW0_long": "uː",
    "IY~": "ĩ",
    "EH~": "ẽ"
}


addon_dir = os.path.dirname(os.path.realpath(__file__))

dictionary_path = os.path.join(addon_dir, 'resources/COMDictionary.txt')
print(dictionary_path)

dic ={str:str}
fileName = dictionary_path


with open(fileName,"r", encoding="utf-8") as file:
    for line in file.read().splitlines():
        elements:list = line.split(' ')
        i = 0
        word = ""
        symbol = ""
        for element in elements:
            if element=='':
                continue
            if i == 0:
                word = element
            elif i != 0:
                symbol += converter[element]
            i += 1
        dic[word] = symbol


def convert_word(editor: Editor):
    source_field = get_field()[0]
    target_field = get_field()[1]

    if editor.note:
        note = editor.note
        symbol_text = ""
        succeeded = True

        if source_field not in note:
            showInfo("Please make sure the field in the settings\n Tools > Pronounce Symbol Generator Setting")
            return

        for word in note[source_field].split(' '):
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
            if note.id == 0:
                editor.mw.col.addNote(note)
            else:
                note.flush()

        QTimer.singleShot(500, lambda: editor.loadNote())







def convert_words(note):
    source_field = get_field()[0]
    target_field = get_field()[1]

    if source_field not in note:
        showInfo("Please make sure the field in the settings\n Tools > Pronounce Symbol Generator Setting")
        return

    symbol_text = ""
    for word in note[source_field].split(' '):
        word = word.upper()
        if word in dic:
            if len(symbol_text) != 0:
                symbol_text += ' '
            symbol_text += dic[word]
        else:
            return False
    note[target_field] = symbol_text

    note.flush()
    QTimer.singleShot(500, lambda: note.load())
    return True




