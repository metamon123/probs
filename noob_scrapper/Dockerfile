FROM ubuntu:18.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirror.kakao.com/g" /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python3.6 python3-pip

RUN mkdir /noob_scrapper
WORKDIR /noob_scrapper

ADD requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt
ADD src ./src
WORKDIR ./src
RUN rm -rf __pycache__
RUN rm -rf mydb.db
RUN python3 flag_setting.py
RUN rm flag_setting.py

CMD ["python3", "app.py", "8080"]
