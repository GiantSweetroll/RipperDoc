FROM python:3

RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev

RUN pip install numpy
RUN pip install pandas
RUN pip install flask
RUN pip install flask-restx
RUN pip install matplotlib
RUN pip install tensorflow
RUN pip install opencv-python

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]