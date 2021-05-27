FROM tensorflow/serving

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install curl

ENV MODEL_NAME=ripperdoc

EXPOSE 8501

COPY . ./models/ripperdoc/