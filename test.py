with open("./data/Emilia_ZH_EN_pinyin/vocab.txt", "r", encoding="utf-8") as f:
    vocab_emilia = f.readlines()
    
with open("./data/VietNam_char/vocab.txt", "r", encoding="utf-8") as f:
    vocab_vn = f.readlines()

vocab_extend = set() 

for item in vocab_vn:
    if item not in vocab_emilia:
        vocab_extend.add(item[:-1])
        
print(vocab_extend)   
text = ""
for char in vocab_extend:
    text += ',' + char
print(text)