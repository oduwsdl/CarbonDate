FROM python:2-onbuild

MAINTAINER Sawood Alam <ibnesayeed@gmail.com>

CMD ["python", "local.py", "search", "www.youtube.com", "-e", "cdGetBacklinks"]
