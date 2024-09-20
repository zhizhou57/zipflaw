import re

def clean_text(text):
    return re.sub(r'[^a-zA-Z]+', ' ', text)

def clean_chinese_text(text):
    return re.sub(r'[^\u4e00-\u9fff]+', ' ', text)

def tokenize_english_word(text):
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    return words

def tokenize_char(text, language):
    if language == 'english':
        cleaned_text = clean_text(text)
    elif language == 'chinese':
        cleaned_text = clean_chinese_text(text)
    else:
        raise ValueError(f"Unsupported language: {language}")
    return cleaned_text

def traditional_to_simplified(text):
    from opencc import OpenCC
    cc = OpenCC('t2s')
    simplified_text = cc.convert(text)
    return simplified_text

