ACA-Py Plugin - HTTP Universal Resolver
=======================================

This plugin provides an ACA-Py DID Resolver interface to a Universal
Resolver instance over HTTP.

## Installation and Usage

First, install this plugin into your environment.

```sh
$ pip install git+https://github.com/sicpa-dlab/acapy-resolver-universal.git
```

When starting up ACA-Py, load the plugin along with any other startup
parameters.

```sh
$ aca-py start --arg-file my_config.yml --plugin universal_resolver
```
