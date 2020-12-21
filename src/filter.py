import itertools
import nltk
import os
import re
import string
from typing import List
from pathlib import Path
from nltk import word_tokenize, wordpunct_tokenize, ngrams
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from src.stream import stream_generator
from src.utility import resolve_data_directory

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
word_features = list()
twogram_features = list()


def run():
    global word_features
    global twogram_features
    global stopwords
    valid_comments = load_comments("training_set_valid")
    invalid_comments = load_comments("training_set_invalid")
    comments = valid_comments + invalid_comments
    preprocessed_words = preprocess_comments(comments)
    all_words = nltk.FreqDist(preprocessed_words)
    all_2grams = generate_twograms_for_comments(comments)
    word_features = list(all_words)[:2]
    twogram_features = [gram for gram in all_2grams if any(x in word_features for x in gram)]
    training_set_documents = create_documents(valid_comments, invalid_comments)

    classifier = nltk.NaiveBayesClassifier.train(training_set_documents)
    stream = stream_generator()
    comment_count = 0
    while True:
        for comment in stream:
            print(f'comment {comment_count}')
            # if ' book ' in comment.body:
            classification_prediction = classifier.classify(
                comment_features(comment.body))
            print(f"classification_prediction {classification_prediction}")
            if classification_prediction == 'valid':
                print(comment.body)
                response = input("Any key to continue.")
            comment_count += 1
    # train classifier
    # start redis queue listener on all_comments queue
    # classify comments
    # push valid comment to valid_comments queue
    # script picks up valid comments and performs action


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
    global word_features
    global twogram_features
    comment_twograms = generate_twograms_for_comments([comment])
    features = {}
    for twogram in twogram_features:
        features['contains({})'.format(twogram)] = (twogram in comment_twograms)
    return features


def preprocess_comments(comments: List[str]):
    comments_without_urls = remove_http_urls(comments)
    tokens = tokenize_and_merge_comments(comments_without_urls)
    words = lowercase_words(tokens)
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
    for grams in ngrams(preprocess_comments(comments), 2):
      ngrams_total.append(grams)
    return ngrams_total

run()
