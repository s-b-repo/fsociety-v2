import os
import re
from fsociety.core.menu import confirm, menu
from fsociety.core.repo import GitHubRepo

class XsstrikeRepo(GitHubRepo):
    def __init__(self):
        super().__init__(
            path="s0md3v/XSStrike",
            install={"pip": "requirements.txt"},
            description="Advanced XSS Detection Suite",
        )

    def is_valid_url(self, url):
        """
        Validate the URL format using regex.
        """
        url_regex = re.compile(
            r'^(https?://)?([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})+)(:\d+)?(/.*)?$'
        )
        return url_regex.match(url) is not None

    def get_scan_arguments(self):
        """
        Present a menu to the user for predefined or custom argument selection.
        """
        # Predefined scan configurations
        options = {
            "Quick Scan": ["--crawl"],
            "Comprehensive Scan": ["--crawl", "--params", "--fuzzer"],
            "Custom Scan": None,  # Allows the user to enter custom arguments
        }

        # Display menu to user
        print("\nSelect a scanning mode:")
        choice = menu(list(options.keys()))
        
        if choice == "Custom Scan":
            custom_args = input("Enter custom arguments (space-separated): ").strip()
            return custom_args.split() if custom_args else []
        else:
            return options[choice]

    def run(self):
        try:
            os.chdir(self.full_path)  # Change directory to the repository path
        except FileNotFoundError:
            print("Error: Repository path not found. Ensure XSStrike is installed correctly.")
            return

        user_url = input("\nEnter a URL to scan: ").strip()

        if not self.is_valid_url(user_url):
            print("Error: Invalid URL format. Please provide a valid URL.")
            return

        scan_args = self.get_scan_arguments()
        args_str = " ".join(scan_args)

        command = f"python3 xsstrike.py --url {user_url} {args_str}"
        print(f"Executing command: {command}")
        
        result = os.system(command)

        if result != 0:
            print(f"Error: Command execution failed with exit code {result}.")
        else:
            print("Scan completed successfully.")

# Instantiate and run the XSStrike repository module
xsstrike = XsstrikeRepo()
