import jieba
from pypinyin import lazy_pinyin, Style

import os
import os 
os.makedirs("/content/F5-TTS-Finetune/ckpts/VietNam", exist_ok=True)

def convert_char_to_pinyin(text_list, polyphone=True):
    final_text_list = []
    god_knows_why_en_testset_contains_zh_quote = str.maketrans(
        {"“": '"', "”": '"', "‘": "'", "’": "'"}
    )  # in case librispeech (orig no-pc) test-clean
    custom_trans = str.maketrans({";": ","})  # add custom trans here, to address oov
    for text in text_list:
        char_list = []
        text = text.translate(god_knows_why_en_testset_contains_zh_quote)
        text = text.translate(custom_trans)
        for seg in jieba.cut(text):
            seg_byte_len = len(bytes(seg, "UTF-8"))
            if seg_byte_len == len(seg):  # if pure alphabets and symbols
                if char_list and seg_byte_len > 1 and char_list[-1] not in " :'\"":
                    char_list.append(" ")
                char_list.extend(seg)
            elif polyphone and seg_byte_len == 3 * len(seg):  # if pure chinese characters
                seg = lazy_pinyin(seg, style=Style.TONE3, tone_sandhi=True)
                for c in seg:
                    if c not in "。，、；：？！《》【】—…":
                        char_list.append(" ")
                    char_list.append(c)
            else:  # if mixed chinese characters, alphabets and symbols
                for c in seg:
                    if ord(c) < 256:
                        char_list.extend(c)
                    else:
                        if c not in "。，、；：？！《》【】—…":
                            char_list.append(" ")
                            char_list.extend(lazy_pinyin(c, style=Style.TONE3, tone_sandhi=True))
                        else:  # if is zh punc
                            char_list.append(c)
        final_text_list.append(char_list)

    return final_text_list


with open("../data/VietNam_char/metadata.txt", "r", encoding="utf-8") as f:
    list_meta = f.readlines()
    
vocab_set = set()

for meta in list_meta:
    try:
        text = meta.split("|")[1].strip()
        text = convert_char_to_pinyin([text], polyphone=True)[0]
        if "ẳs" in text:
            print(meta)
        vocab_set.update(list(text))
    except:
        print(meta)

with open("vocab_set.txt", "w+", encoding="utf-8") as f:
    for v in vocab_set:
        f.write(v + "\n")

    
