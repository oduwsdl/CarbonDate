FROM python:3.9

LABEL maintainer="Grant Atkins <gatki001@odu.edu>"
LABEL org.opencontainers.image.source=https://github.com/oduwsdl/carbondate

RUN apt install python3
COPY requirements.txt /usr/src/app/
WORKDIR /usr/src/app
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

CMD ["./main.py", "-h"]
