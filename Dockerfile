FROM python:3

LABEL maintainer="Grant Atkins <gatki001@odu.edu>"

COPY requirements.txt /usr/src/app/
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

CMD ["./main.py", "-h"]
