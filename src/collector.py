import os
import sys
import time
from pathlib import Path
from src.stream import stream_generator

training_set_files_count = 0
testing_set_files_count = 0


def collector():
    global testing_set_files_count
    global training_set_files_count
    if len(sys.argv) <= 1:
        print('no keyword arguments provided.')
        return

    print(f'\nRunning collector with keywords: {", ".join(sys.argv[1:])}\n')
    keyword_set = set(sys.argv[1:])

    training_set_files_count = training_set_count()
    testing_set_files_count = testing_set_count()

    while True:
        stream = stream_generator()
        comment_count = 0
        for comment in stream:
            print(f'{training_set_files_count} file(s) in training dataset, {testing_set_files_count} files(s) in testing dataset, ({comment_count} comments searched)')
            sys.stdout.write("\033[F")  # Cursor up one line
            for keyword in keyword_set:
                if keyword in comment.body:
                    print(
                        "-----------------------------------------------------COMMENT-----------------------------------------------------")
                    highlighted_comment = highlight_keywords(
                        comment.body, keyword_set)
                    print(highlighted_comment, end="\n\n")
                    print(
                        f'link: https://www.reddit.com{comment.permalink}', end="\n\n")
                    response = input(
                        "Add comment to dataset? [Y/y or any key to continue search]. ")
                    if response.lower() == 'y':
                        create_data_file(comment.body, comment)
            comment_count += 1


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
        text = comment.replace(word, f'\033[31m{word}\033[0m')
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
