FROM tensorflow/serving

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install curl

ENV MODEL_NAME=ripperdoc

EXPOSE 8501

COPY . ./models/ripperdoc/