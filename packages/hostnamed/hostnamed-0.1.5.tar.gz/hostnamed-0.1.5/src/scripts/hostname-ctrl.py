#!/usr/bin/env python
import os
import urllib
import yaml
import click
import hashlib
import requests
from hostnamed.utils import load_config
from hostnamed.utils import input_config
from hostnamed.utils import save_config
from hostnamed.utils import client_update
from hostnamed.utils import client_query

@click.group()
def hostnamed():
    pass


@hostnamed.command()
@click.option("-c", "--config", default="~/.hostnamed.conf")
def config(config):
    """Make settings."""
    settings = load_config(config)
    new_entry = input_config()
    settings.update(new_entry)
    save_config(settings, config)


@hostnamed.command()
@click.option("-c", "--config", default="~/.hostnamed.conf")
@click.argument("hostnames", nargs=-1)
def update(config, hostnames):
    """Do update."""
    settings = load_config(config)
    if not hostnames:
        hostnames = list(settings.keys())
    for hostname in hostnames:
        config = settings[hostname]
        update_url = urllib.parse.urljoin(config["server"], "update/")
        result = client_update(update_url, hostname, config["key"], config["use-local-ip"])
        if result:
            print("{} OK".format(hostname))
        else:
            print("{} FAILED".format(hostname))

@hostnamed.command()
@click.option("-c", "--config", default="~/.hostnamed.conf")
@click.argument("hostname", nargs=1)
def query(config, hostname):
    """Query host's ip by hostname."""
    settings = load_config(config)
    if not hostname in settings:
        print("No configuration for host: {}.".format(hostname))
        os.sys.exit(1)
    config = settings[hostname]
    query_url = urllib.parse.urljoin(config["server"], "query/")
    result = client_query(query_url, hostname, config["key"])
    print(result)

if __name__ == "__main__":
    hostnamed()
