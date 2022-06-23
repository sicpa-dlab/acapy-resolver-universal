"""Integration tests: Test resolution."""

import asyncio
import json
import logging
from pathlib import Path
from aries_cloudagent.config.injection_context import InjectionContext

import pytest

from universal_resolver import UniversalResolver
from aries_cloudagent.resolver.base import ResolverError

CONFIG_PATH = Path(__file__).parent / "uniresolver_config.json"
TEST_CONFIG = json.loads(CONFIG_PATH.read_text())
TEST_DIDS = [
    did for driver in TEST_CONFIG.values() for did in driver["http"]["testIdentifiers"]
]


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def context():
    yield InjectionContext(
        settings={
            "plugin_config": {
                "http_uniresolver": {"endpoint": "http://dev.uniresolver.io"}
            }
        }
    )


@pytest.fixture(scope="module")
async def resolver(context: InjectionContext):
    resolver = UniversalResolver()
    await resolver.setup(context)
    yield resolver


@pytest.mark.int
@pytest.mark.asyncio
@pytest.mark.parametrize("did", TEST_DIDS)
async def test_resolve_and_load(resolver, did, caplog):
    """Test resolution and schema parsing."""
    caplog.set_level(logging.INFO)
    try:
        await asyncio.wait_for(resolver.resolve(None, did), timeout=10)
    except asyncio.TimeoutError:
        pytest.xfail("Resolver took too long.")
    except ResolverError:
        pytest.xfail("Could not resolve a DID that should be resolvable.")
