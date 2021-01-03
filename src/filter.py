import itertools
import json
import nltk
import os
import re
import redis
import string
from typing import List
from pathlib import Path
from nltk import word_tokenize, wordpunct_tokenize, ngrams
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from src.utility import resolve_data_directory

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
twogram_features = list()
redis_client = redis.Redis(host='queue', port=6379, db=0)


def run():
    global twogram_features
    valid_comments = load_comments("training_set_valid")
    invalid_comments = load_comments("training_set_invalid")
    comments = valid_comments + invalid_comments
    preprocessed_words_without_stopwords = preprocess_comments(comments, True)
    preprocessed_words_with_stopwords = preprocess_comments(comments, False)
    all_words = nltk.FreqDist(preprocessed_words_without_stopwords)
    word_features = list(all_words)[:1]
    all_twograms = generate_twograms_for_comments(
        preprocessed_words_with_stopwords)
    twogram_features = [gram for gram in all_twograms if any(
        x in word_features for x in gram)]
    training_set_documents = create_documents(valid_comments, invalid_comments)
    classifier = nltk.NaiveBayesClassifier.train(training_set_documents)
    while True:
        comment_str = redis_client.lpop("queue:comments")
        if comment_str != None:
            comment = json.loads(comment_str)
            classification_prediction = classifier.classify(
                comment_features(comment['body']))
            if classification_prediction == 'valid':
                redis_client.rpush("queue:valid_comments", comment_str)


def create_documents(valid_comments, invalid_comments) -> List[tuple]:
    return ([(comment_features(comment), 'valid') for comment in valid_comments] + [(comment_features(comment), 'invalid') for comment in invalid_comments])


def load_comments(dir_indicator) -> List[str]:
    comments = list()
    data_directory = resolve_data_directory(dir_indicator)
    data_directory_path = Path(__file__).parent / \
        f"documents/{data_directory}"

    document_paths = [f'{data_directory_path}/{path}' for path in os.listdir(
        data_directory_path) if '.txt' in path]

    for p in document_paths:
        file = open(p)
        raw = file.read()
        comments.append(raw)
        file.close()

    return comments


def comment_features(comment: str):
    global twogram_features
    comment_twograms = generate_twograms_for_comments(
        preprocess_comments([comment], False))
    features = {}
    for twogram in twogram_features:
        features['contains({})'.format(twogram)] = (
            twogram in comment_twograms)
    return features


def preprocess_comments(comments: List[str], stopwords_remove: bool):
    comments_without_urls = remove_http_urls(comments)
    tokens = tokenize_and_merge_comments(comments_without_urls)
    words = lowercase_words(tokens)
    if stopwords_remove:
        words = remove_stopwords(words)
    words = remove_punctuations(words)
    words = stem_words(words)
    return words


def tokenize_and_merge_comments(comments: List[str]):
    "split up and merge all comment words into single list of single words/punctuations tokens"
    token_list = list(itertools.chain.from_iterable(
        [wordpunct_tokenize(comment) for comment in comments]))
    return token_list


def lowercase_words(words: List[str]):
    "lowercase and return all words"
    word_list = [word.lower() for word in words]
    return word_list


def remove_stopwords(words: List[str]):
    "remove english stopwords from list of words"
    word_list = [word for word in words if word not in stopwords]
    return word_list


def remove_punctuations(words: List[str]):
    "remove english stopwords from list of words"
    punc_set = set(string.punctuation)
    punc_set.add("’")
    word_list = [word for word in words if word not in punc_set]
    return word_list


def remove_http_urls(comments: List[str]):
    "remove english stopwords from list of words"
    comment_list = [re.sub(r"http\S+", "", comment) for comment in comments]
    return comment_list


def stem_words(words: List[str]):
    stemmer = SnowballStemmer('english')
    token_list = [stemmer.stem(word) for word in words]
    return token_list


def generate_twograms_for_comments(comments: List[str]):
    ngrams_total = list()
    for grams in ngrams(comments, 2):
        ngrams_total.append(grams)
    return ngrams_total


run()
