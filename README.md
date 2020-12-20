## Comment Stream

Stream comments posted on social platforms in near-real time and persist them to queue for processing.

## Currently Supported

- Reddit

## Setup Environment Variable

- TODO: Add information about creating a reddit app (for now credentials are provided in `docker-compose.env.example`)

```bash
# from repo root, create docker-compose.env file
$ cp ci/docker-compose.env.example ci/docker-compose.env
```
May have to do this manually on windows. Copy contents of docker-compose.env.example into a new file named docker-compose.env in ci directory.

## Collect Comments for Training/Testing Dataset

```bash
# from repo root
# build collector image
$ docker build -t comments-collector -f ci/collector.Dockerfile .

# run container and pass keywords
$ docker run -it --name comments-collector -v $(pwd)/documents:/usr/src/app/src/documents --env-file ci/docker-compose.env comments-collector key_word1 key_word2 key_word3

# remove image done
$  docker rm -f comments-collector
```

## Build and Run

```bash
# from repo root
# docker compose up
$ docker-compose --file ci/docker-compose.yml up -d

# rebuild images on changes
$ docker-compose --file ci/docker-compose.yml build

# when done
$ docker-compose --file ci/docker-compose.yml down
```
