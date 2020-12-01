FROM python:3.8

WORKDIR /usr/src/app

COPY ./src/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "-m", "src.main.py" ]