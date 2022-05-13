FROM python:3.9.0
COPY ./ /app
RUN pip3 install pipenv
RUN pipenv install -e /app/
#docker network create --driver=bridge --subnet=192.168.54.0/24 --gateway=192.168.54.100 mysubnet
#docker build ./master -t master:1.0.0
#docker run --name master --net=mysubnet  --ip 192.168.54.120 -d -t master:1.0.0
EXPOSE 7000-9000
CMD pipenv run python3  /app/master/app/main.py
