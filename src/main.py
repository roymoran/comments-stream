from src.stream import stream_generator


def main():
    stream = stream_generator()
    for comment in stream:
        print(comment.body)
    # stream comments
    # push comment to redis queue

main()
