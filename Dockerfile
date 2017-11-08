FROM python:3.4-alpine
MAINTAINER john@neetgroup.net
ADD . /blog
WORKDIR /blog
RUN pip install -r requirements.txt
CMD ["python", "-m", "blog"]
