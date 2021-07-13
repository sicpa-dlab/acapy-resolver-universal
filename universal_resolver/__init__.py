"""HTTP Universal Resolver Plugin for ACA-Py"""

from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.resolver.did_resolver_registry import DIDResolverRegistry
from .resolver import UniversalResolver


async def setup(context: InjectionContext):
    """Setup the plugin."""

    # Inject plugin
    registry = context.inject(DIDResolverRegistry)
    resolver = UniversalResolver()
    await resolver.setup(context)
    registry.register(resolver)
