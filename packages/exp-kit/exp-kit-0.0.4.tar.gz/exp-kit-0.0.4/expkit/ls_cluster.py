# coding: utf-8
from halo import Halo
from tabulate import tabulate
import click

from . import utils


def doc2entry(doc):
    return [ doc['name'], len(doc['instance_id_list']), doc['request_id'] ]

def ls():
    with Halo(text='Loading cluster information ...', spinner='dots'):
        clusters = utils.load_all_clusters()
    table = tabulate([ [ 'name', 'size', 'request-id' ] ] + list(map(doc2entry, clusters)))
    click.echo(table)
