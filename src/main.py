import redis
from src.stream import stream_generator

redis_client = redis.Redis(host='localhost', port=6379, db=0)
def main():
    stream = stream_generator()
    for comment in stream:
        redis_client
        print(comment.body)

main()
