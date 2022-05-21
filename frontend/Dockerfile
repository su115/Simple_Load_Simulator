FROM python:3.9.0
COPY . /app
RUN pip3 install pipenv
RUN pipenv install -e /app/
#docker build ./frontend -t frontend:1.0.0
#docker run --name frontend --net=mysubnet  --ip  192.168.54.140 -e MASTER_IP='192.168.54.120'    -e  MASTER_PORT='7790'   -d -t frontend:1.0.0
EXPOSE  5000
CMD pipenv run python3  /app/frontend/app/main.py
