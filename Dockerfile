FROM python:3.6.5-slim-stretch
LABEL maintainer="a.guillermo.guzman@gmail.com"

RUN groupadd --gid 999 appuser && \
    useradd --system --uid 999 --gid appuser appuser
USER appuser:appuser

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY --chown=appuser:appuser ./requirements.txt .

USER root:root
RUN pip install --no-cache-dir -r requirements.txt

USER appuser:appuser

#COPY --chown=appuser:appuser ./src ./src

COPY --chown=appuser:appuser ./entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 5000

CMD ["python"]
