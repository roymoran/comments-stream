## Comment Stream

Find comments of interests on social platforms by using a classifier trained on data that you collect.

## Platforms Currently Supported

- Reddit

## Setup Reddit App Variables

Start by creating a new reddit app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).

```bash
# from repo root, create docker-compose.env 
$ cp ci/docker-compose.env.example ci/docker-compose.env
```
Now update `docker-compose.env` with reddit app credentials generated 
## Collect Comments for Training/Testing Dataset

```bash
# from repo root
# build collector image
$ docker build -t comments-collector -f ci/collector.Dockerfile .

# run container and pass keywords (on windows replace $(pwd) with %cd%)
$ docker run -it --name comments-collector -v $(pwd)/documents:/usr/src/app/src/documents --env-file ci/docker-compose.env comments-collector key_word1 key_word2 key_word3

# remove image when done
$ docker rm -f comments-collector
```
### Demo
![Collector Demo](./docs/collector_demo.gif)
## Build and Run Filter

```bash
# from repo root
# docker compose up
$ docker-compose --file ci/docker-compose.yml up -d
# tail valid comment predictions from running filter container
$ docker container logs filter -f
# rebuild images on changes
$ docker-compose --file ci/docker-compose.yml build
# when done
$ docker-compose --file ci/docker-compose.yml down
```

### Demo
![Filter Demo](./docs/filter_demo.gif)