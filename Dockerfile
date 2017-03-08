FROM kaixhin/theano
RUN pip install keras
ENV KERAS_BACKEND theano
WORKDIR /src
ENTRYPOINT ["python", "src/app.py"]
COPY . /src
