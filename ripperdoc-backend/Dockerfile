FROM python:3

RUN apt-get update
# RUN apt-get install tensorflow-model-server
# RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 libgl1-mesa-glx

RUN pip install numpy
# RUN pip install pandas
RUN pip install flask
RUN pip install flask-restx
# RUN pip install matplotlib
RUN pip install tensorflow
RUN pip install Pillow
# RUN pip install opencv-python
RUN pip install docker

EXPOSE 5000

COPY . .

CMD ["app.py"]
ENTRYPOINT ["python3"]