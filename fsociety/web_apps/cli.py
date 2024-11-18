from fsociety.core.menu import tools_cli

from .photon import photon
from .xsstrike import xsstrike
from .gobuster import gobuster  # Import gobuster module

__tools__ = [xsstrike, photon, gobuster]  # Add gobuster to the tools list

def cli():
    tools_cli(__name__, __tools__)
