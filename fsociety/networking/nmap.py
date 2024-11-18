import os
import json
from shutil import which

from fsociety.core.hosts import InvalidHost, add_host, get_hosts
from fsociety.core.menu import set_readline
from fsociety.core.repo import GitHubRepo

premade_args = {
    "simple": "{host}",
    "common_ports": "-F {host}",
    "all_ports": "-p- {host}",
    "detect_os": "-A {host}",
    "tcp_syn_scan": "-sS {host}",
    "tcp_connect": "-sT {host}",
    "nse_standard": "-sV -sC {host}",
    "vuln_scan": "-Pn --script vuln {host}",
    "google_malware": "-p80 --script http-google-malware {host}",
    "aggressive_scan": "-A -T4 {host}",
    "detect_web_app": "--script=http-enum {host}",
    "subdomain_enumeration": "-sn --script hostmap-crtsh {host}",
    "heartbleed_test": "-sV -p 443 --script=ssl-heartbleed {host}",
    "slowloris": "-max-parallelism 800 -Pn --script http-slowloris --script-args http-slowloris.runforever=true {host}",
    "dns_brute_force": "-p53 --script dns-brute {host}",
    "ftp_anon_scan": "-p21 --script ftp-anon {host}",
    "ssh_brute_force": "-p22 --script ssh-brute --script-args userdb=users.txt,passdb=pass.txt {host}",
    "http_methods": "-p80 --script http-methods {host}",
    "banner_grabbing": "-sV {host}",
    "os_detection": "-O {host}",
    "all_protocols": "-sO {host}",
    "trace_route": "--traceroute {host}",
    "http_robots": "-p80 --script http-robots.txt {host}",
    "smtp_enum": "-p25 --script smtp-enum-users {host}",
    "http_headers": "-p80 --script http-headers {host}",
    "ssl_poodle": "-p443 --script ssl-poodle {host}",
    "script_scan": "-sC {host}",
    "version_detection": "-sV {host}",
    "ip_id_sequence": "--ip-options {host}",
    "icmp_echo_scan": "-PE {host}",
    "udp_scan": "-sU {host}",
    "arp_ping_scan": "-PR {host}",
    "tcp_ack_scan": "-sA {host}",
    "service_scan": "-sV {host}",
    "stealth_scan": "-sS {host}",
    "full_udp_scan": "-sU -p- {host}",
    "custom_script": "--script={custom_script} {host}",
}


class NmapRepo(GitHubRepo):
    def __init__(self):
        super().__init__(
            path="nmap/nmap",
            install={
                "arch": "sudo pacman -Sy nmap",
                "brew": "install nmap",
                "linux": "sudo apt-get install nmap",
            },
            description="the Network Mapper",
        )

    def installed(self):
        return which("nmap")

    def install(self):
        super().install(clone=False)

    def scan_host(self, host, selected_arg):
        try:
            args = premade_args[selected_arg].format(host=host)
            print(f"\nRunning: nmap {args}")
            result = os.popen(f"nmap {args}").read()
            with open("scan_results.json", "a") as logfile:
                json.dump({"host": host, "scan_type": selected_arg, "result": result}, logfile, indent=4)
                logfile.write("\n")
            print("\nScan complete! Results saved to 'scan_results.json'.")
        except KeyError:
            print("Invalid scan type selected. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def batch_scan(self, filepath, selected_arg):
        try:
            with open(filepath, "r") as file:
                hosts = [line.strip() for line in file.readlines()]
            for host in hosts:
                print(f"\nScanning host: {host}")
                self.scan_host(host, selected_arg)
        except FileNotFoundError:
            print(f"File not found: {filepath}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def run(self):
        hosts = get_hosts()
        set_readline(hosts)
        host = input("\nEnter a host or 'batch' for multiple hosts: ").strip()

        if host == "batch":
            filepath = input("Enter the file path containing hostnames/IPs: ").strip()
            selected = input("\nSelect a scan type: ")
            if selected in premade_args:
                self.batch_scan(filepath, selected)
            else:
                print("Invalid scan type selected.")
        else:
            if not host:
                raise InvalidHost
            if host not in hosts:
                add_host(host)
            print("\nName".ljust(25) + "| Args")
            print("-" * 50)
            for name, args in premade_args.items():
                print(f"{name.ljust(25)}: {args.format(host=host)}")
            set_readline(premade_args.keys())
            selected = input("\nMake a selection: ")
            if selected in premade_args:
                self.scan_host(host, selected)
            else:
                print("Invalid selection.")
            self.run()


nmap = NmapRepo()
