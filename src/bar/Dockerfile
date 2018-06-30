FROM python:3.6.5-slim-stretch
LABEL maintainer="a.guillermo.guzman@gmail.com"

RUN groupadd --gid 999 appuser && \
    useradd --system --uid 999 --gid appuser appuser

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY --chown=appuser:appuser ./src/bar/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser ./src/bar/entrypoint.sh .

USER appuser:appuser

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python"]
