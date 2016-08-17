FROM python:2.7

MAINTAINER Neo <fallenangel0813@gmail.com>

RUN pip install ordereddict

RUN pip install requests

RUN pip install BeautifulSoup4

RUN pip install surt

RUN pip install tornado

ADD . /carbon

WORKDIR /carbon

CMD python local.py search wwww.youtube.com -e cdGetBacklinks
