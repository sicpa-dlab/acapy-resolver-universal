"""Run Universal Resolver HTTP Plugin Demo."""

import json
import os
from colorama import Fore, Style, init
from collections import namedtuple
from . import Agent


init(autoreset=True)


def info(*args):
    """Print info styled text."""
    print("{}{}".format(Fore.BLUE + Style.BRIGHT, " ".join(args)))


def success(*args):
    """Print success styled text."""
    print("{}{}".format(Fore.GREEN + Style.BRIGHT, " ".join(args)))


def fail(*args):
    """Print failure styled text."""
    print("{}{}".format(Fore.RED + Style.BRIGHT, " ".join(args)))


def cont():
    """Prompt for continuation"""
    print("{}{}".format(Fore.BLUE, "Press Enter to continue..."), end="")
    input()


def env_or_input(var, prompt):
    """Return the value of env var or prompt for input."""
    value = os.environ.get(var)
    if not value:
        value = input(prompt)
    return value


Inputs = namedtuple("Input", ("dids", "vcs"))


def get_inputs() -> Inputs:
    """Load inputs for demo."""
    with open("runner/inputs.json") as inputs_file:
        inputs = json.load(inputs_file)

    return Inputs(inputs["dids"], inputs["vcs"])


def resolve(requester: Agent, did: str):
    """Resolve a did."""
    info(f"Resolving: {did}")
    try:
        result = requester.resolve(did)
    except Exception as error:
        fail(f"Failed to resolve {did}: {error}")
    else:
        success("Resolved document:")
        print(json.dumps(result, indent=2))


def jsonld_verify(requester, vc: dict):
    """Verify example VC."""
    info("Verifying JSON-LD credential:")
    print(json.dumps(vc, indent=2))

    try:
        result = requester.post(
            "/jsonld/verify",
            return_json=True,
            fail_with="Failed to verify jsonld",
            json={"doc": vc},
        )
    except Exception as error:
        fail(f"Failed to verify cred: {error}")
    else:
        if result["valid"]:
            success("Verified.")
        else:
            fail("Verification failed: {}".format(result["error"]))


def main():
    """Run the demo."""

    resolver = Agent("http://resolver:3001")

    inputs = get_inputs()

    success("The demo will resolve some DID IDs and verified some DID Documents.")
    cont()

    for did in inputs.dids:
        resolve(resolver, did)
        cont()

    for vc in inputs.vcs:
        jsonld_verify(resolver, vc)
        cont()


if __name__ == "__main__":
    main()
