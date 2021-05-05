FROM python:3.6-alpine

WORKDIR /usr/src/app/

COPY __init__.py runner/
COPY __main__.py runner/
COPY requirements.txt runner/
COPY inputs.json runner/
RUN pip3 install --no-cache-dir -r runner/requirements.txt

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD sh -c "/wait && python -m runner"
# CMD tail -f /dev/null --------------- use this to keep container running to copy reports
