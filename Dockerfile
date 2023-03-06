FROM python:3.10
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
# Installing FFMpeg to play music
RUN apt-get update && apt-get -y upgrade
RUN apt install -y ffmpeg
COPY . /bot
RUN mkdir -p /saved
CMD python main.py
