import os
import shutil
import traceback

from requests import get
from colorama import Fore, Back, Style

from fsociety.core.config import install_dir


class CommandNotFound(Exception):
    pass


class CommandCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def set_readline(items):
    try:
        import readline
    except ImportError:
        pass
    else:
        import rlcompleter
        if isinstance(items, list):
            readline.set_completer(CommandCompleter(items).complete)
        elif isinstance(items, dict):
            readline.set_completer(CommandCompleter(items.keys()).complete)
        else:
            readline.set_completer(CommandCompleter(list(items)).complete)
        readline.parse_and_bind("tab: complete")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_menu_item(item):
    return f"{Back.WHITE}{Fore.BLACK}{item}{Style.RESET_ALL}"


def format_tools(tools):
    if isinstance(tools, dict):
        tools = tools.keys()
    return "".join([f"\n\t{str(tool)}" for tool in tools])


def module_name(module):
    return module.__name__.split(".")[-1]


def prompt(path="", base_path="~"):
    return f"{Fore.RED}fsociety {os.path.join(base_path, path, '')}#{Fore.WHITE} "


def input_wait():
    input("\nPress [ENTER] to continue... ")


def tools_cli(name, tools):
    for tool in tools:
        print(f"{format_menu_item(str(tool))}\n")
    set_readline(tools)
    selected_tool = input(prompt(name.split(".")[-2])).strip()
    if not selected_tool in tools.keys():
        raise CommandNotFound(selected_tool)
    tool = tools.get(selected_tool)
    if not tool.installed():
        tool.install()
    try:
        response = tool.run()
        if response > 0:
            raise Exception
    except Exception as e:
        print(f"{Fore.RED + selected_tool} failed{Fore.RESET}")
        print(str(e))
        traceback.print_exc()
        if confirm("Do you want to reinstall?"):
            os.chdir(install_dir)
            shutil.rmtree(tool.full_path)
            tool.install()
    input_wait()


def confirm(message="Do you want to?"):
    response = input(f"{message} (y/n): ").lower()
    if response:
        return response[0] == "y"
    return False


def print_contributors():
    print(Fore.RED + """
8888b.  888888 Yb    dP .dP"Y8 
 8I  Yb 88__    Yb  dP  `Ybo." 
 8I  dY 88""     YbdP   o.`Y8b 
8888Y"  888888    YP    8bodP'
""")
    response = get(
        'https://api.github.com/repos/fsociety-team/fsociety/contributors')
    contributors = response.json()
    for contributor in sorted(contributors, key=lambda c: c['contributions'], reverse=True):
        username = contributor.get("login")
        print(f" {username} ".center(30, "-"))
    print(Fore.RESET)
    input_wait()