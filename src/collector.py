import os
import sys
import time
from pathlib import Path
from itertools import chain, combinations
from src.stream import stream_generator

training_set_files_count = 0
testing_set_files_count = 0
keyword_powerset = set()


def collector():
    global testing_set_files_count
    global training_set_files_count

    global keyword_powerset

    if len(sys.argv) <= 1:
        print('no keyword arguments provided.')
        return

    print(f'\nRunning collector with keywords: {", ".join(sys.argv[1:])}\n')

    keyword_powerset = sorted(
        set(powerset(sys.argv[1:])), key=len, reverse=True)
    keyword_search_set = set()

    if len(keyword_powerset) > 1:
        print('Select keyword combinations to include in search')
        for ks in keyword_powerset:
            response = input(
                f'Include {ks}? [Y/y or any key to exclude]. ')
            if response.lower() == 'y':
                keyword_search_set.add(ks)
    else:
        keyword_search_set = keyword_powerset

    training_set_files_count = training_set_count()
    testing_set_files_count = testing_set_count()

    while True:
        stream = stream_generator()
        comment_count = 0
        for comment in stream:
            print(f'{training_set_files_count} file(s) in training dataset, {testing_set_files_count} files(s) in testing dataset, ({comment_count} comments searched)')
            sys.stdout.write("\033[F")  # Cursor up one line
            matched = False
            for pset_set in keyword_search_set:
                if matched:
                    continue
                if all(x in comment.body for x in pset_set):
                    matched = True
                    print(
                        "-----------------------------------------------------COMMENT-----------------------------------------------------")
                    print(
                        f'keyword(s) present: {", ".join(pset_set)}', end="\n\n")
                    highlighted_comment = highlight_keywords(
                        comment.body, pset_set)
                    print(highlighted_comment, end="\n\n")
                    print(
                        f'link: https://www.reddit.com{comment.permalink}', end="\n\n")
                    response = input(
                        "Add comment to dataset? [Y/y or any key to continue search]. ")
                    if response.lower() == 'y':
                        create_data_file(comment.body, comment)
            comment_count += 1


def powerset(iterable):
    "generate and return powerset of list excluding empty set."
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def create_data_file(content, file_name):
    data_directory = resolve_data_directory()
    file_path = Path(__file__).parent / \
        f"documents/{data_directory}/{file_name}.txt"
    text_file = open(file_path, "w+")
    text_file.write(content)
    text_file.close()
    increment_files_count(data_directory)


def resolve_data_directory() -> str:
    global testing_set_files_count
    global training_set_files_count
    if training_set_files_count > testing_set_files_count:
        return 'testing_set'
    elif testing_set_files_count > training_set_files_count:
        return 'training_set'
    return 'training_set'


def increment_files_count(directory):
    if directory == 'testing_set':
        global testing_set_files_count
        testing_set_files_count += 1
    elif directory == 'training_set':
        global training_set_files_count
        training_set_files_count += 1


def highlight_keywords(comment, keywords):
    # TODO Consider portable way to highlight text via package
    text = comment
    for word in keywords:
        text = text.replace(word, f'\033[31m{word}\033[0m')
    return text


def training_set_count() -> int:
    directory_path = Path(__file__).parent / \
        f"documents/training_set/"

    return len([name for name in os.listdir(directory_path) if '.txt' in name])


def testing_set_count() -> int:
    directory_path = Path(__file__).parent / \
        f"documents/testing_set/"

    return len([name for name in os.listdir(directory_path) if '.txt' in name])


collector()
