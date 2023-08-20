FROM python:3.10-alpine 


RUN adduser -D worker
USER worker

# Install dependencies only
WORKDIR /home/worker

ENV PATH="/home/worker/.local/bin:${PATH}"
COPY --chown=worker:worker Pipfile Pipfile Pipfile.lock ./

RUN pip install --user pipenv && \
    pipenv install --deploy


COPY --chown=worker:worker . /home/worker


CMD [ "pipenv", "run", "python", "main.py" ]