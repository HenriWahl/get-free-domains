#!/usr/bin/env python3

from argparse import ArgumentParser
from itertools import product
from pathlib import Path
from queue import Queue
from string import ascii_lowercase
from sys import exit
from threading import Thread

from dns.resolver import NoAnswer, \
    NXDOMAIN, \
    Resolver, \
    NoNameservers
from dns.exception import Timeout

class FileQueueThread(Thread):
    """
    Writing results to output file
    """
    def __init__(self, file_queue):
        super().__init__()
        self.file_queue = file_queue

    def run(self):
        while True:
            domain = self.file_queue.get()
            with open(config.file, 'a') as file_handle_free_domains:
                file_handle_free_domains.write(f'{domain}\n')
            # mark the job as done
            self.file_queue.task_done()


class ResolverQueueThread(Thread):
    """
    Doing the resolve work
    """
    def __init__(self, resolver_queue, file_queue):
        super().__init__()
        self.resolver_queue = resolver_queue
        self.file_queue = file_queue

    def run(self):
        while True:
            domain = self.resolver_queue.get()
            try:
                if not domain in free_domains:
                    try:
                        answer = resolver.resolve(domain, 'A')
                    except NXDOMAIN:
                        free_domains_a.append(domain)
                    if domain in free_domains_a:
                        free_domains.append(domain)
                        if use_free_domain_file:
                            self.file_queue.put(domain)
                        else:
                            print(domain)
            except NoAnswer:
                print('NoAnswer', domain)
            except NoNameservers:
                print('NoNameservers', domain)
            except Timeout:
                print('Timeout', domain)
            # mark the job as done
            self.resolver_queue.task_done()

parser = ArgumentParser(prog='get-free-domains')
parser.add_argument('--length', type=int, required=True)
parser.add_argument('--tld', type=str, required=True)
parser.add_argument('--nameserver', type=str, nargs='*', default='1.1.1.1 8.8.8.8 8.8.4.4')
parser.add_argument('--file', type=str)
parser.add_argument('--prefix', type=str, default='')
parser.add_argument('--threads', type=int, default=1)

config = parser.parse_args()

if len(config.prefix) > config.length-1:
    exit("Prefix's length can't be greater than length - 1.")

resolver = Resolver()
if config.nameserver:
    resolver.nameservers = config.nameserver.split(' ')

file_queue = Queue()
file_queue_thread = FileQueueThread(file_queue)
file_queue_thread.daemon = True
file_queue_thread.start()

resolver_queue = Queue()
for thread in range(config.threads):
    resolver_queue_thread = ResolverQueueThread(resolver_queue, file_queue)
    resolver_queue_thread.daemon = True
    resolver_queue_thread.start()

# for now only check for A-Records
free_domains = []
free_domains_a = []


use_free_domain_file = False
if config.file:
     if not Path(config.file).exists():
         Path(config.file).touch()
     if Path(config.file).exists() and \
        Path(config.file).is_file():
        with open(config.file, 'r') as file_handle_free_domains:
            free_domains = [line.rsplit('\n')[0] for line in file_handle_free_domains.readlines()]
        use_free_domain_file = True

for combo in product(ascii_lowercase, repeat=config.length-len(config.prefix)):
    domain = f"{config.prefix}{''.join(combo)}.{config.tld}"
    resolver_queue.put(domain)

# wait until the threads are finished
resolver_queue.join()
file_queue.join()
