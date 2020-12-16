import nltk
import os
from typing import List
from pathlib import Path
from nltk import word_tokenize
from src.stream import stream_generator
from src.utility import resolve_data_directory

word_features = list()


def run():
    global word_features
    valid_comments = load_comments("training_set_valid")
    invalid_comments = load_comments("training_set_invalid")
    comments = valid_comments + invalid_comments
    comments_joined = " ".join(comments)
    comment_words = comments_joined.split()
    all_words = nltk.FreqDist(w.lower() for w in comment_words)
    word_features = list(all_words)[:2000]
    training_set_documents = create_documents(valid_comments, invalid_comments)

    classifier = nltk.NaiveBayesClassifier.train(training_set_documents)
    stream = stream_generator()
    while True:
        for comment in stream:
            classification_prediction = classifier.classify(
                comment_features(comment.body))
            print(f"classification_prediction {classification_prediction}")
            if classification_prediction == 'valid':
                print(comment.body)
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
    comment_words = set(comment.split())
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in comment_words)
    return features


def stream_comments():
    pass


run()
