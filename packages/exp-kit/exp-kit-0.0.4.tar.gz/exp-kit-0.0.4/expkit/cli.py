# coding: utf-8
import json
import os

import click

from . import new_cluster
from . import rm_cluster
from . import ls_cluster
from . import utils


@click.group()
@click.option('-u', '--user-config',
              type=click.Path(resolve_path=True, exists=True),
              help='Path to user configuration.',
              default=os.path.join(os.path.expanduser('~'), '.exp-kit/config.json'))
def main(user_config):
    """
    Entry point of cluster-operation commands.

    \b
    An example user config looks as follows.
    {
        "key_name": "key-pair-name",
        "iam_fleet_role": "something:like:this::<aws-id>:role/aws-ec2-spot-fleet-tagging-role",
        "public_keys": [ "ssh-rsa XXXX key-pair-name" ],
        "key_path": "/path/to/key-pair-name.pem"
    }
    """
    utils.load_user_config(user_config)

@main.command()
@click.option('-c', '--cluster-config',
              type=click.Path(resolve_path=True),
              help='Path to cluster configuration.')
def new(cluster_config):
    """
    Create a new cluster based on a configuration json.

    \b
    An example config.json looks as follows.
    {
        "name": "cluster-name",
        "size": 3,
        "instance": "m4.large",
        "image_id": "ami-xxxxxxxx",
        "snapshot_id": "snap-xxxxxxx",
        "disk_size": 20,
        "spot_price": 0.251
    }
    """
    default_config = {
        "name": "cluster",
        "size": 3,
        "instance": "m4.large",
        "image_id": "ami-091a3e69",
        "snapshot_id": "snap-58c483d9",
        "disk_size": 20,
        "spot_price": 0.251
    }
    if cluster_config is None:
        utils.warn('No config path given. Fall back to default settings.')
        config = {}
    else:
        config = utils.parse_json_file(cluster_config)
    default_config.update(config)
    default_config.update(utils.get_user_config())
    new_cluster.new(default_config)

@main.command()
@click.argument('cluster-name', type=str)
def rm(cluster_name):
    """
    Destroy a cluster by cancelling the spot request.
    """
    rm_cluster.rm(cluster_name)

@main.command()
def ls():
    """
    List all cluster information.
    """
    ls_cluster.ls()

if __name__ == '__main__':
    main()
