FROM ubuntu:18.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirror.kakao.com/g" /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y netcat curl
ADD requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

ADD app.py /app.py
ADD flag.txt /what_is_this77777777
ADD run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
