"""HTTP Universal Resolver Plugin for ACA-Py"""

from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.resolver.did_resolver_registry import DIDResolverRegistry
import yaml
import os
from .http_universal import HTTPUniversalDIDResolver

CONFIG_FILE = "aries-acapy-plugin-http-uniresolver/http_uniresolver/default_config.yml"


async def setup(context: InjectionContext, endpoint: str = None, methods: list = None):
    """Setup the plugin."""
    # Load config
    if endpoint or methods:
        with open(CONFIG_FILE, 'r') as default_config:
            config = yaml.safe_load(default_config)
        if endpoint:
            config["endpoint"] = endpoint
        if methods:
            config["methods"] = methods
        with open(CONFIG_FILE, 'w') as default_config:
            default_config.write(yaml.safe_dump(config))

    # Inject plugin
    registry = context.inject(DIDResolverRegistry)
    resolver = HTTPUniversalDIDResolver()
    await resolver.setup(context)
    registry.register(resolver)
