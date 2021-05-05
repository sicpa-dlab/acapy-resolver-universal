FROM bcgovimages/aries-cloudagent:py36-1.16-0_0.7-pre.0

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

# Make site packages location more accessible (for use with volumes)
RUN ln -s $(pyenv prefix)/lib/python3.6/site-packages site-packages

USER root
COPY http_uniresolver aries-acapy-plugin-http-uniresolver/http_uniresolver
COPY README.md aries-acapy-plugin-http-uniresolver
COPY setup.py aries-acapy-plugin-http-uniresolver
COPY pyproject.toml aries-acapy-plugin-http-uniresolver
COPY poetry.lock aries-acapy-plugin-http-uniresolver
COPY docker/default.yml .
RUN chown -R indy:indy aries-acapy-plugin-http-uniresolver
USER $user

RUN cd aries-acapy-plugin-http-uniresolver; poetry install --no-dev

ENTRYPOINT ["/bin/bash", "-c", "aca-py \"$@\"", "--"]
CMD ["start", "--arg-file", "default.yml"]
