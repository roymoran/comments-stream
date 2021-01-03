import json
import redis

redis_client = redis.Redis(host='queue', port=6379, db=0)

def run_script():
    while True:
        comment = redis_client.lpop("queue:valid_comments")
        if comment != None:
            comment = json.loads(comment)
            # Add additonal custom logic to process valid comments
            print(
                "-----------------------------------COMMENT-----------------------------------")
            print(comment['body'], end="\n\n")
            print(f'link: {comment["link"]}', end="\n\n")
            
run_script()
