FROM python:3.9.0
COPY . /app
RUN pip3 install pipenv
RUN pipenv install -e /app/
RUN pipenv run pytest -m "not network" /app/worker/tests/
#docker build ./worker -t worker:1.0.3
#docker run --name worker --net=mysubnet  --ip  192.168.54.130 -e MASTER_IP='192.168.54.120'    -e  MASTER_PORT='7790' -e POD_IP='192.168.54.130' -e POD_NAME='worker-1' -e NAMESPACE='default' -e POD_PORT=7799  -d -t worker:1.0.3
EXPOSE 7000-9000
CMD pipenv run python3  /app/worker/app/main.py
