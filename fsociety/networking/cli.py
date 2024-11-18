from fsociety.core.menu import tools_cli

# Import tools
from .bettercap import bettercap
from .nmap import nmap

# Define tools
__tools__ = [nmap, bettercap]

def cli():
    """
    Launches the CLI for the registered tools.
    Dynamically adds tools for extensibility.
    """
    try:
        tools_cli(__name__, __tools__)
    except ImportError as e:
        print(f"Error importing tools: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    cli()
