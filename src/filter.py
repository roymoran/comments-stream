import nltk
import os
from typing import List
from pathlib import Path
from nltk import word_tokenize
from nltk.corpus import stopwords
from src.stream import stream_generator
from src.utility import resolve_data_directory

nltk.download('stopwords')
word_features = list()

def run():
    global word_features
    stopwords = nltk.corpus.stopwords.words('english')
    valid_comments = load_comments("training_set_valid")
    invalid_comments = load_comments("training_set_invalid")
    comments = valid_comments + invalid_comments
    comments_joined = " ".join(comments)
    comment_words = comments_joined.split()
    all_words = nltk.FreqDist(w.lower() for w in comment_words if w.lower() not in stopwords)
    word_features = list(all_words)[:5]
    training_set_documents = create_documents(valid_comments, invalid_comments)

    classifier = nltk.NaiveBayesClassifier.train(training_set_documents)
    stream = stream_generator()
    comment_count = 0
    while True:
        for comment in stream:
            print(f'comment {comment_count}')
            # if ' book ' in comment.body:
            classification_prediction = classifier.classify(comment_features(comment.body))
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
    comment_words = set(comment.split())
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in comment_words)
    return features


def stream_comments():
    pass


run()
