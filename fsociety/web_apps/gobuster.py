import os

from fsociety.core.menu import confirm, choose
from fsociety.core.repo import GitHubRepo


class GobusterRepo(GitHubRepo):
    def __init__(self):
        super().__init__(
            path="OJ/gobuster",
            install={"command": "apt-get install gobuster -y"},
            description="Gobuster - A Directory and DNS brute-forcing tool",
        )

    def run(self):
        # Define the predefined Gobuster options
        modes = {
            "1": {
                "description": "Directory brute-force",
                "command": lambda url, wordlist: f"gobuster dir -u {url} -w {wordlist} -x php,html,js"
            },
            "2": {
                "description": "DNS Subdomain brute-force",
                "command": lambda domain, wordlist: f"gobuster dns -d {domain} -w {wordlist}"
            },
            "3": {
                "description": "VHost brute-force",
                "command": lambda domain, wordlist: f"gobuster vhost -u {domain} -w {wordlist}"
            },
        }

        # Select mode
        print("\nChoose a Gobuster mode:")
        for key, option in modes.items():
            print(f"[{key}] {option['description']}")

        mode = input("\nEnter the mode number: ").strip()
        if mode not in modes:
            print("Invalid mode selected.")
            return

        # Select wordlist
        wordlist = self.choose_wordlist()

        # Gather target information
        target = input("\nEnter the target (URL or domain): ").strip()

        # Prepare and execute the command
        command = modes[mode]["command"](target, wordlist)
        print(f"\nRunning: {command}")
        os.system(command)

    def choose_wordlist(self):
        """Display a menu to select a wordlist."""
        print("\nChoose a wordlist:")
        wordlists = {
            "1": "/usr/share/wordlists/dirb/common.txt",
            "2": "/usr/share/wordlists/dirb/big.txt",
            "3": "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt",
            "4": "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt",
            "5": "Custom (enter your own path)"
        }

        for key, path in wordlists.items():
            print(f"[{key}] {path}")

        choice = input("\nEnter the wordlist number: ").strip()
        if choice not in wordlists:
            print("Invalid choice. Defaulting to common.txt.")
            return wordlists["1"]

        if choice == "5":
            custom_path = input("Enter the custom wordlist path: ").strip()
            if not os.path.exists(custom_path):
                print("Custom wordlist path does not exist. Defaulting to common.txt.")
                return wordlists["1"]
            return custom_path

        return wordlists[choice]


gobuster = GobusterRepo()
