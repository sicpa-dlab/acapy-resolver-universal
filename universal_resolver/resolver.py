"""HTTP Universal DID Resolver."""

import logging
import json
import re
from typing import Optional, Pattern, cast

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
DEFAULT_ENDPOINT = "https://dev.uniresolver.io"


async def _fetch_resolver_props(endpoint: str) -> dict:
    """Retrieve universal resolver properties."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{endpoint}/1.0/properties/") as resp:
            if resp.status >= 200 and resp.status < 400:
                return await resp.json()
            raise ValueError(await resp.text())


async def _get_supported_methods_pattern(endpoint: str) -> Pattern:
    props = await _fetch_resolver_props(endpoint)
    return re.compile(
        r"(?:" + "|".join(driver["http"]["pattern"] for driver in props.values()) + ")"
    )


class UniversalResolver(BaseDIDResolver):
    """Universal DID Resolver with HTTP bindings."""

    def __init__(self):
        """Initialize UniversalResolver."""
        super().__init__(ResolverType.NON_NATIVE)
        self._endpoint = None
        self._supported_methods = None

    async def setup(self, context: InjectionContext):
        """Preform setup, populate supported method list, configuration."""
        endpoint = (
            cast(dict, context.settings.get("plugin_config", {}))
            .get("http_uniresolver", {})
            .get("endpoint", DEFAULT_ENDPOINT)
        )
        await self.configure(endpoint)

    async def configure(
        self,
        endpoint: Optional[str] = None,
        supported_methods_pattern: Optional[Pattern] = None,
    ):
        """Do configuration."""
        self._endpoint = endpoint or DEFAULT_ENDPOINT
        self._supported_methods_pattern = (
            supported_methods_pattern
            or await _get_supported_methods_pattern(self._endpoint)
        )

    @property
    def supported_did_regex(self) -> Pattern:
        """Return supported methods regex."""
        return self._supported_methods_pattern

    async def _resolve(self, _profile: Profile, did: str) -> dict:
        """Resolve DID through remote universal resolver."""

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._endpoint}/1.0/identifiers/{did}") as resp:
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
