import numpy as np
import json
import os
from verify import parse_args
from util import clean_text, clean_chinese_text, tokenize_english_word

def calculate_statistics(data, language):
    total_data = len(data)
    
    # Before cleaning
    content_lengths = [len(item['content']) for item in data]
    avg_content_length_before = np.mean(content_lengths)
    total_chars_before = sum(content_lengths)
    
    if language == 'english':
        all_words_before = [word for item in data for word in item['content'].split()]
        word_lengths_before = [len(word) for word in all_words_before]
        avg_word_length_before = np.mean(word_lengths_before)
    else:
        avg_word_length_before = 0
    
    # After cleaning
    if language == 'chinese':
        cleaned_contents = [clean_chinese_text(item['content']) for item in data]
    else:
        cleaned_contents = [clean_text(item['content']) for item in data]
    cleaned_content_lengths = [len(content) for content in cleaned_contents]
    avg_content_length_after = np.mean(cleaned_content_lengths)
    total_chars_after = sum(cleaned_content_lengths)
    
    if language == 'english':
        all_words_after = [word for content in cleaned_contents for word in tokenize_english_word(content)]
        word_lengths_after = [len(word) for word in all_words_after]
        avg_word_length_after = np.mean(word_lengths_after)
    else:
        avg_word_length_after = 0
    
    return (total_data, 
            avg_content_length_before, avg_word_length_before, total_chars_before,
            avg_content_length_after, avg_word_length_after, total_chars_after)

def load_crawl_data(crawl_data_path, language):
    corpus = ""
    with open(crawl_data_path, 'r') as f:
        data = json.load(f)
        stats = calculate_statistics(data, language)
        print(f"Total data: {stats[0]}")
        print(f"Before cleaning:")
        print(f"  Average content length: {stats[1]:.2f} characters")
        print(f"  Average word length: {stats[2]:.2f} characters")
        print(f"  Total characters: {stats[3]/1000000:.2f} M")
        print(f"After cleaning:")
        print(f"  Average content length: {stats[4]:.2f} characters")
        print(f"  Average word length: {stats[5]:.2f} characters")
        print(f"  Total characters: {stats[6]/1000000:.2f} M")
        for item in data:
            corpus += clean_text(item['content']) + " "
    return corpus.lower()

if __name__ == '__main__':
    args = parse_args()
    crawl_data_path = args.crawl_data_path
    language = args.language
    if not os.path.exists(crawl_data_path):
        raise ValueError(f'File not found: {crawl_data_path}')
    corpus = load_crawl_data(crawl_data_path, language)
