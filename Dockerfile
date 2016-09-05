FROM python:3-onbuild

MAINTAINER Neo <fallenangel0813@gmail.com>

CMD ["python", "local.py", "search", "www.youtube.com", "-e", "cdGetBacklinks"]
