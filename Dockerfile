FROM python:2.7

MAINTAINER Neo <fallenangel0813@gmail.com>

ENV CASPERJS_VERSION=1.1.1

RUN pip install ordereddict

RUN pip install requests

RUN pip install BeautifulSoup4

RUN pip install surt

ADD ./docker /docker

RUN /docker/build && rm -rf docker

ADD . /carbon

WORKDIR /carbon

CMD python local.py wwww.youtube.com
