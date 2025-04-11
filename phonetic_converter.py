import os
from PyQt6.QtCore import QTimer
from aqt.utils import showInfo, tooltip
from aqt.editor import Editor
from .config_manager import  get_field
import re

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


def convert_token(token: str) -> str:
    # Match leading punctuation, the core word (letters and apostrophes), and trailing punctuation.
    m = re.match(r"(^[^A-Z']*)([A-Z']+)([^A-Z']*$)", token.upper())
    if m:
        prefix, core, suffix = m.groups()
        # If the core word exists in our dictionary, convert it.
        if core in dic:
            return prefix + dic[core] + suffix
    # If not matched or conversion not found, return the original token.
    return token

def convert_word(editor: Editor):
    source_field, target_field = get_field()

    if not editor.note:
        showInfo("No note selected.")
        return

    note = editor.note

    if source_field not in note:
        showInfo("Source field not found. Check settings in Tools > Pronounce Symbol Generator Settings.")
        return

    if target_field not in note:
        showInfo(f"Target field '{target_field}' does not exist in the current note.")
        return

    source_text = note[source_field]
    # Split text into tokens (words and space/punctuation separators)
    tokens = re.split(r'(\s+|[.,/()])', source_text)
    converted_tokens = []
    succeeded = True
    failed_tokens = []

    for token in tokens:
        if re.fullmatch(r'(\s+|[.,/()])', token):
            converted_tokens.append(token)
        else:
            converted = convert_token(token)
            # If conversion did not change the token and token isn't empty, mark conversion as partial failure.
            if converted == token and token.strip() != "":
                succeeded = False
                failed_tokens.append(token)
            converted_tokens.append(converted)

    symbol_text = ''.join(converted_tokens)

    if not symbol_text.strip():
        showInfo("Converted symbol text is empty.")
        return

    if not succeeded:
        tooltip(f"Some tokens could not be converted: {', '.join(failed_tokens)}", period = 3000)

    note[target_field] = symbol_text
    QTimer.singleShot(500, lambda: editor.loadNote())
    
def convert_words(note):
    source_field, target_field = get_field()

    if source_field not in note:
        showInfo("Please make sure the field is set in Tools > Pronounce Symbol Generator Settings")
        return

    source_text = note[source_field]
    tokens = re.split(r'(\s+|[.,/()])', source_text)
    converted_tokens = []
    
    for token in tokens:
        if re.fullmatch(r'(\s+|[.,/()])', token):
            converted_tokens.append(token)
        else:
            converted_tokens.append(convert_token(token))
            
    symbol_text = ''.join(converted_tokens)
    note[target_field] = symbol_text
    note.flush()
    QTimer.singleShot(500, lambda: note.load())
    return True




