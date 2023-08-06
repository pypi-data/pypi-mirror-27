"""
Witty Command Line Interface
"""
# Python packages
import os
import json
from urllib.parse import quote

# Third-party packages
import click
import requests


# Variables
ENDPOINT = 'https://api.wit.ai/{}'
SERVER_ACCESS_TOKEN = os.environ.get('SERVER_ACCESS_TOKEN')


# Cli functions
@click.group()
def cli():
    """
    Witty-Cli instance.
    """
    click.echo('Welcome to Fiboot console!')


@cli.command()
@click.option('--text', prompt=True)
def message(text):
    """
    Network request to wit.ai to the messages endpoint
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(SERVER_ACCESS_TOKEN)
    }
    params = {
        "q": quote(text)
    }
    response = requests.post(
        ENDPOINT.format('message'), params=params, headers=headers).json()
    click.echo(response)


@cli.group()
def entities():
    """
    Wit.ai entities endpoint
    """
    pass


@entities.command()
def get():
    """
    Request a GET method to entities endpoint
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(SERVER_ACCESS_TOKEN)
    }
    response = requests.get(
        ENDPOINT.format('entities'), headers=headers).json()
    click.echo(response)


@entities.command()
@click.option('--entityid', prompt=True)
@click.option('--doc', prompt=True)
def post(entityid, doc):
    """
    Request a POST method to entities endpoint
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(SERVER_ACCESS_TOKEN)
    }
    payload = {
        'id': entityid,
        'doc': doc
    }
    response = requests.post(
        ENDPOINT.format('entities'), json=payload, headers=headers).json()
    click.echo(response)


@cli.command()
def samples():
    """
    Network request to wit.ai to the samples endpoint
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(SERVER_ACCESS_TOKEN)
    }
    payload = json.load(open('data.json'))
    response = requests.post(ENDPOINT.format('samples'), json=payload, headers=headers).json()
    click.echo(response)
