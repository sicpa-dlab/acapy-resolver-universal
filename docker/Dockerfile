FROM bcgovimages/aries-cloudagent:py36-1.16-0_0.6.0

USER root
COPY http_uniresolver aries-acapy-plugin-http-uniresolver/http_uniresolver
COPY requirements.txt aries-acapy-plugin-http-uniresolver
COPY README.md aries-acapy-plugin-http-uniresolver
COPY setup.py aries-acapy-plugin-http-uniresolver
COPY docker/default.yml .
RUN chown -R indy:indy aries-acapy-plugin-http-uniresolver
USER $user

# Make ACA-Py Install location more accessible
RUN ln -s /home/indy/.pyenv/versions/3.6.13/lib/python3.6/site-packages site-packages

RUN pip3 install -e ./aries-acapy-plugin-http-uniresolver

ENTRYPOINT ["/bin/bash", "-c", "aca-py \"$@\"", "--"]
CMD ["start", "--arg-file", "default.yml"]
