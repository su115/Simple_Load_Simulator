FROM python:3.9.0
COPY . /app
RUN pip3 install pipenv
RUN pipenv install -e /app/
RUN pipenv run pytest -m "not network" /app/worker/tests/
EXPOSE 7799 
CMD pipenv run python3  /app/worker/app/main.py
