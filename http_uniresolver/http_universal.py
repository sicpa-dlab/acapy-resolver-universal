"""HTTP Universal DID Resolver."""

import logging
import json
from typing import Sequence

import aiohttp

from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.core.profile import Profile
from aries_cloudagent.resolver.base import (
    BaseDIDResolver,
    DIDNotFound,
    ResolverError,
    ResolverType,
)

LOGGER = logging.getLogger(__name__)
DEFAULT_CONFIGURATION = {
    "endpoint": "https://dev.uniresolver.io/1.0/identifiers",
    "methods": [
        "sov",
        "abt",
        "btcr",
        "erc725",
        "dom",
        "stack",
        "ethr",
        "web",
        "v1",
        "key",
        "ipid",
        "jolo",
        "hacera",
        "elem",
        "seraphid",
        "github",
        "ccp",
        "work",
        "ont",
        "kilt",
        "evan",
        "echo",
        "factom",
        "dock",
        "trust",
        "io",
        "bba",
        "bid",
        "schema",
        "ion",
        "ace",
        "gatc",
        "unisot",
        "icon",
        "vaa",
        "cy",
        "nacl",
        "sirius",
        "mpg",
        "trustbloc",
        "hcr",
        "neoid",
    ],
}


class HTTPUniversalDIDResolver(BaseDIDResolver):
    """Universal DID Resolver with HTTP bindings."""

    def __init__(self):
        """Initialize HTTPUniversalDIDResolver."""
        super().__init__(ResolverType.NON_NATIVE)
        self._endpoint = None
        self._supported_methods = None

    async def setup(self, _context: InjectionContext):
        """Preform setup, populate supported method list, configuration."""
        plugin_conf = _context.settings.get("plugin_config", {}).get("http_uniresolver")

        configuration = DEFAULT_CONFIGURATION
        if plugin_conf:
            configuration.update(plugin_conf)

        self.configure(configuration)

    def configure(self, configuration: dict):
        """Configure this instance of the resolver from configuration dict."""
        try:
            self._endpoint = configuration["endpoint"]
            self._supported_methods = configuration["methods"]
        except KeyError as err:
            raise ResolverError(
                f"Failed to configure {self.__class__.__name__}, "
                "missing attribute in configuration: {err}"
            ) from err

    @property
    def supported_methods(self) -> Sequence[str]:
        """Return supported methods.

        By determining methods from config file, we preserve the ability to not
        use the universal resolver for a given method, even if the universal
        is capable of resolving that method.
        """
        return self._supported_methods

    async def _resolve(self, _profile: Profile, did: str) -> dict:
        """Resolve DID through remote universal resolver."""

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._endpoint}/{did}") as resp:
                if resp.status == 200:
                    doc = await resp.json()
                    did_doc = doc["didDocument"]
                    LOGGER.info("Retrieved doc: %s", json.dumps(did_doc, indent=2))
                    return did_doc
                if resp.status == 404:
                    raise DIDNotFound(f"{did} not found by {self.__class__.__name__}")

                text = await resp.text()
                raise ResolverError(
                    f"Unexecpted status from universal resolver ({resp.status}): {text}"
                )
