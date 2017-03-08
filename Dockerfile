FROM kaixhin/theano
WORKDIR /src
ENTRYPOINT ["python", "src/app.py"]
COPY . /src
