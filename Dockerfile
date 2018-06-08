FROM python:3.6.5-slim-stretch
LABEL maintainer="a.guillermo.guzman@gmail.com"

RUN apt-get update

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python"]