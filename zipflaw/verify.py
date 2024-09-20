# -*- coding: utf-8 -*-
# @Time    : 2024/9/18 14:39
# @Author  : yesliu
# @File    : preprocess.py

import argparse
import json
import math
import os
from util import tokenize_english_word, tokenize_char, traditional_to_simplified
from collections import Counter
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--crawl_data_path', default='../wikipedia_chinese/output.json', type=str, required=False)
    parser.add_argument('--language', default='chinese', type=str, choices=['english', 'chinese'], required=False)
    return parser.parse_args()

def load_crawl_data(crawl_data_path, language):
    corpus = ""
    with open(crawl_data_path, 'r') as f:
        data = json.load(f)
        print("total data: ", len(data))
        for item in data:
            content = item['content']
            if language == 'chinese':
                content = traditional_to_simplified(content)
            corpus += content + " "
    return corpus.lower()

def stat_corpus_word(corpus):
    words = tokenize_english_word(corpus)
    word_counter = Counter(words)
    sorted_word_counts = word_counter.most_common(500)
    for item in sorted_word_counts:
        if item[0] == ' ':
            item[0] = 'space'
            break
    return sorted_word_counts

def stat_corpus_char(corpus, language):
    chars = tokenize_char(corpus, language)
    char_counter = Counter(chars)
    if language == 'chinese':
        sorted_char_counts = char_counter.most_common(100)
    else:
        sorted_char_counts = char_counter.most_common()
    for index, item in enumerate(sorted_char_counts):
        if item[0] == ' ':
            if language == 'chinese':
                sorted_char_counts.remove(item)
            else:
                sorted_char_counts[index] = ('space', item[1])
            break
    return sorted_char_counts

def plot_log_freq(counter, ax, title):
    ranks = range(1, len(counter) + 1)
    frequencies = [count for _, count in counter]
    expected_zipf = [counter[0][1] / i for i in ranks]
    
    ax.loglog(ranks, frequencies, 'bo', markersize=4, alpha=0.5, label='Actual Frequency')
    ax.loglog(ranks, expected_zipf, 'r--', linewidth=2.5, alpha=0.5, label='Expected Zipf Distribution')
    
    ax.set_xlabel('Word Frequency Rank (Log Scale)', fontsize=18)
    ax.set_ylabel('Frequency (Log Scale)', fontsize=18)
    ax.set_title(title, fontsize=20)
    ax.legend(fontsize=14)
    
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.tick_params(axis='both', which='major', labelsize=14)

def plot_freq(counter, ax, title):
    expected_zipf = [counter[0][1]/(i+1) for i in range(len(counter))]
    ax.bar(range(len(counter)), [count for _, count in counter], align='center', alpha=0.5)
    ax.plot(expected_zipf, label='Expected Zipf', color='red', linewidth=2.5, alpha=0.5)
    ax.set_xlabel('Rank', fontsize=18)
    ax.set_ylabel('Frequency', fontsize=18)
    ax.set_title(title, fontsize=20)
    ax.legend(fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=14)

def plot_zipf_law_graphs_english(word_counter, char_counter):
    # Plot the first graph (normal frequency)
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 16))
    plot_freq(word_counter, ax1, f"Zipf's Law ({language.capitalize()} Words): Frequency vs Rank")
    plot_freq(char_counter, ax2, f"Zipf's Law ({language.capitalize()} Characters): Frequency vs Rank")
    plt.tight_layout()
    plt.savefig(f'image/zipf_law_frequency_{language}.png')
    plt.close(fig1)

    # Plot the second graph (logarithmic frequency)
    fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(18, 16))
    plot_log_freq(word_counter, ax3, f"Zipf's Law ({language.capitalize()} Words): Frequency vs Rank (Log Scale)")
    plot_log_freq(char_counter, ax4, f"Zipf's Law ({language.capitalize()} Characters): Frequency vs Rank (Log Scale)")
    plt.tight_layout()
    plt.savefig(f'image/zipf_law_log_frequency_{language}.png')
    plt.close(fig2)

def plot_zipf_law_graphs_chinese(char_counter):
    # Plot the first graph (normal frequency)
    fig1, ax1 = plt.subplots(figsize=(18, 10))
    plot_freq(char_counter, ax1, f"Zipf's Law ({language.capitalize()} Characters): Frequency vs Rank")
    plt.tight_layout()
    plt.savefig(f'image/zipf_law_frequency_{language}.png')
    plt.close(fig1)

    # Plot the second graph (logarithmic frequency)
    fig2, ax2 = plt.subplots(figsize=(18, 10))
    plot_log_freq(char_counter, ax2, f"Zipf's Law ({language.capitalize()} Characters): Frequency vs Rank (Log Scale)")
    plt.tight_layout()
    plt.savefig(f'image/zipf_law_log_frequency_{language}.png')
    plt.close(fig2)



def compute_char_entropy(char_counter):
    total_chars = sum(count for _, count in char_counter)
    char_probabilities = [count / total_chars for _, count in char_counter]
    entropy = -sum(p * math.log2(p) for p in char_probabilities if p > 0)
    return entropy

def plot_entropy_vs_data_scale(corpus, language):
    data_scales = [int(len(corpus) * i / 18) for i in range(1, 19)]
    entropies = []

    for scale in data_scales:
        subset_corpus = corpus[:scale]
        char_counter = stat_corpus_char(subset_corpus, language)
        entropy = compute_char_entropy(char_counter)
        entropies.append(entropy)

    plt.figure(figsize=(10, 6))
    plt.plot(data_scales, entropies, marker='o')
    plt.xlabel('Data Scale (number of characters)/Million')
    plt.ylabel('Entropy (bits)')
    plt.title(f'Entropy of {language.capitalize()} Characters vs Data Scale')
    plt.grid(True)
    
    # Modify x-axis ticks
    xticks = [data_scales[i] for i in range(0, len(data_scales), 3)]  # Show every 3rd tick
    plt.xticks(xticks, [f'{x//1e6}' for x in xticks])  # Convert to millions and format
    
    plt.savefig(f'image/entropy_vs_data_scale_{language}.png')
    plt.close()

def output_statistics(char_counter, word_counter, language):
    print("Character and Word Statistics:")
    print("==============================")
    
    # Character probabilities
    total_chars = sum(count for _, count in char_counter)
    char_probabilities = [(char, count / total_chars) for char, count in char_counter]
    char_probabilities.sort(key=lambda x: x[1], reverse=True)
    
    if language == 'chinese':
        char_probabilities = char_probabilities[:30]
    
    print("\nCharacter Probabilities:")
    print("------------------------")
    for char, prob in char_probabilities:
        print(f"{char}& {prob:.6f}&")
    
    if language == 'english':
        # Top 30 words with probabilities
        total_words = sum(count for _, count in word_counter)
        top_30 = word_counter[:30]
        
        print("\nTop 30 Words with Probabilities:")
        print("--------------------------------")
        for i, (word, count) in enumerate(top_30, 1):
            probability = count / total_words
            print(f"{i}. {word}: {count} (Probability: {probability:.6f})")

    print("\n==============================")

if __name__ == '__main__':
    args = parse_args()
    crawl_data_path = args.crawl_data_path
    language = args.language
    if not os.path.exists(crawl_data_path):
        raise ValueError(f'File not found: {crawl_data_path}')
    corpus = load_crawl_data(crawl_data_path, language)
    if language == 'english':
        word_counter = stat_corpus_word(corpus)
        char_counter = stat_corpus_char(corpus, language)
    else:
        word_counter = None
        char_counter = stat_corpus_char(corpus, language)

    # Call the functions
    output_statistics(char_counter, word_counter, language)
    if language == 'english':
        plot_zipf_law_graphs_english(word_counter, char_counter)
    else:
        plot_zipf_law_graphs_chinese(char_counter)
    entropy = compute_char_entropy(char_counter)
    print(f"Entropy of {language.capitalize()} characters: {entropy:.2f} bits")

    plot_entropy_vs_data_scale(corpus, language)
    print(f"Entropy vs Data Scale plot saved as 'entropy_vs_data_scale_{language}.png'")

