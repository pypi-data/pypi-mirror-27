"""The target command."""
import queue
import re
import signal
import socket
import sys
import threading
from io import StringIO
from threading import Thread
from urllib.parse import urlsplit

from anubis.scanners.anubis_db import search_anubisdb, send_to_anubisdb
from anubis.scanners.brute_force import brute_force
from anubis.scanners.crt import search_crtsh
from anubis.scanners.dnsdumpster import search_dnsdumpster
from anubis.scanners.dnssec import dnssecc_subdomain_enum
from anubis.scanners.hackertarget import subdomain_hackertarget
from anubis.scanners.netcraft import search_netcraft
from anubis.scanners.nmap import scan_host
from anubis.scanners.pkey import search_pkey
from anubis.scanners.shodan import search_shodan
from anubis.scanners.ssl import search_subject_alt_name, ssl_scan
from anubis.scanners.virustotal import search_virustotal
from anubis.scanners.zonetransfer import dns_zonetransfer
from anubis.utils.ColorPrint import ColorPrint
from anubis.utils.search_worker import SearchWorker
from anubis.utils.signal_handler import SignalHandler
from .base import Base


class Target(Base):
  """Main enumeration module"""
  domains = list()
  ip = str()
  dedupe = set()

  stdout = sys.stdout

  def handle_exception(self, e, message=""):
    if self.options["--verbose"]:
      print(e)
    if message:
      ColorPrint.red(message)

  def init(self):
    url = self.options["TARGET"]

    if not re.match(r'http(s?):', url):
      url = 'http://' + url

    parsed = urlsplit(url)
    host = parsed.netloc

    if host.startswith('www.'):
      host = host[4:]

    self.options["TARGET"] = host

    try:
      self.ip = socket.gethostbyname(self.options["TARGET"])
    except Exception as e:
      self.handle_exception(e,
                            "Error connecting to target! Make sure you spelled it correctly and it is a reachable address")

  def run(self):
    # Retrieve IP of target and run initial configurations
    self.init()

    ColorPrint.green(
      "Searching for subdomains for " + self.ip + " (" + self.options[
        "TARGET"] + ")\n")

    # Default scans that run every time
    threads = [Thread(target=dns_zonetransfer(self, self.options["TARGET"])),
               Thread(
                 target=search_subject_alt_name(self, self.options["TARGET"])),
               Thread(
                 target=subdomain_hackertarget(self, self.options["TARGET"])),
               Thread(target=search_virustotal(self, self.options["TARGET"])),
               Thread(target=search_pkey(self, self.options["TARGET"])),
               Thread(target=search_netcraft(self, self.options["TARGET"])),
               Thread(target=search_crtsh(self, self.options["TARGET"])),
               Thread(target=search_dnsdumpster(self, self.options["TARGET"])),
               Thread(target=search_anubisdb(self, self.options["TARGET"]))]
    # Additional options - ssl cert scan
    if self.options["--ssl"]:
      threads.append(Thread(target=ssl_scan(self, self.options["TARGET"])))

    # Additional options - shodan.io scan
    if self.options["--additional-info"]:
      threads.append(Thread(target=search_shodan(self)))

    # Additional options - nmap scan of dnssec script and a host/port scan
    if self.options["--with-nmap"]:
      threads.append(
        Thread(target=dnssecc_subdomain_enum(self, self.options["TARGET"])))
      threads.append(Thread(target=scan_host(self)))

    # Additional options - brute force common subdomains
    if self.options["--brute-force"]:
      threads.append(Thread(target=brute_force(self, self.options["TARGET"])))

    # Start all threads
    for x in threads:
      x.start()

    # Wait for all of them to finish
    for x in threads:
      x.join()

    # remove duplicates and clean up

    if self.options["--recursive"]:
      self.recursive_search()

    self.domains = self.clean_domains(self.domains)
    self.dedupe = set(self.domains)

    print("Found", len(self.dedupe), "subdomains")
    print("----------------")

    if self.options["--ip"]:
      self.resolve_ips()
    else:
      for domain in self.dedupe:
        ColorPrint.green(domain.strip())

    if not self.options["--no-anubis-db"]:
      send_to_anubisdb(self, self.options["TARGET"])

  def clean_domains(self, domains):
    cleaned = []
    for subdomain in domains:
      subdomain = subdomain.lower()
      # TODO move to regex matching for (.*)://
      subdomain = subdomain.replace("http://", "")
      subdomain = subdomain.replace("https://", "")
      subdomain = subdomain.replace("ftp://", "")
      subdomain = subdomain.replace("sftp://", "")
      # Some pkey return instances like example.com. - remove the final .
      if subdomain.endswith('.'):
        subdomain = subdomain[:-1]
      # If it's an email address, only take the domain part
      if "@" in subdomain:
        subdomain = subdomain.split("@")[1]
      cleaned.append(subdomain.strip())
    return cleaned

  def resolve_ips(self):
    unique_ips = set()
    for domain in self.dedupe:
      try:
        resolved_ip = socket.gethostbyname(domain)
        # TODO - Align domains and ips in stdout
        ColorPrint.green(domain + ": " + resolved_ip)
        unique_ips.add(resolved_ip)
      except Exception as e:
        self.handle_exception(e)
    print("Found %s unique IPs" % len(unique_ips))
    for ip in unique_ips:
      ColorPrint.green(ip)

  def recursive_search(self):
    print("Starting recursive search - warning, might take a long time")
    domains = self.clean_domains(self.domains)
    domains_unique = set(domains)

    num_workers = 10

    if self.options["--queue-workers"]:
      num_workers = int(self.options["--queue-workers"])

    stopper = threading.Event()
    url_queue = queue.Queue()
    for domain in domains_unique:
      url_queue.put(domain)

    # we need to keep track of the workers but not start them yet
    workers = [SearchWorker(url_queue, self.domains, stopper, self) for _ in
               range(num_workers)]

    # create our signal handler and connect it
    handler = SignalHandler(stopper, workers)
    signal.signal(signal.SIGINT, handler)

    if not self.options["--verbose"]:
      # catch stdout and replace it with our own
      self.stdout, sys.stdout = sys.stdout, StringIO()

    # start the threads!
    for worker in workers:
      worker.start()

    # wait for the queue to empty
    url_queue.join()

    sys.stdout = self.stdout
