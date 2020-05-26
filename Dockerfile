FROM python:3

ADD . /app
WORKDIR /app

# install selenium
RUN pip install selenium==3.8.0


#RUN pip install selenium

CMD ["python", "./be.py"]


