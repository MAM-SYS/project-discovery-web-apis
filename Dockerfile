FROM python:3.9.1-slim-buster

RUN apt-get update -y; apt-get install -y curl build-essential; add-apt-repository ppa:longsleep/golang-backports; apt install golang-go; curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

RUN go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest; go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

RUN mkdir -p /app/logs

WORKDIR /app

ADD . /app/

RUN $HOME/.poetry/bin/poetry config virtualenvs.create false

RUN $HOME/.poetry/bin/poetry install

RUN apt-get purge -y build-essential && apt-get -y autoremove && apt-get autoclean

CMD ["python", "main.py"]