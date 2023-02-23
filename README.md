# Archived

This project has been contributed directly to ACA-Py starting from version
0.8.0/1.0.0 and can be used with the `--universal-resolver` flag.

See this PR for additional details: https://github.com/hyperledger/aries-cloudagent-python/pull/1866

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
