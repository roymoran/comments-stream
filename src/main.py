import redis
import json
from src.stream import stream_generator

redis_client = redis.Redis(host='queue', port=6379, db=0)


def main():
    stream = stream_generator()
    for comment in stream:
        redis_client.rpush("queue:comments", json.dumps(
            {'id': comment.id, 'body': comment.body, 'link': f'https://reddit.com{comment.permalink}'}))


main()
