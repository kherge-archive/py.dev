from dev.common import LABEL_NAME, NotManaged, get_docker, is_managed
from docker.models.networks import Network
from tabulate import tabulate
from typing import List, Optional

import docker
import logging
import typer

app = typer.Typer(
    help='''Manages networks.

    Networks are used to provide Internet access to containers, as well as allow
    the host to access services running in containers using managed networks (via
    the "host" driver).
    ''',
    name='network'
)

builtin_list = list
logger = logging.getLogger(__name__)

################################################################################
# Management                                                                   #
################################################################################

def create(name: str, client: Optional[docker.DockerClient] = None):
    '''Creates a managed network.'''
    logger.debug(f"creating network, {name}...")

    client = get_docker(client)

    client.networks.create(
        attachable=True,
        check_duplicate=True,
        driver='host',
        labels={
            LABEL_NAME: 'true'
        },
        name=name,
        scope='global'
    )

def list(client: Optional[docker.DockerClient] = None) -> List[Network]:
    '''Lists the managed networks.'''
    logger.debug('listing networks...')

    client = get_docker(client)

    return client.networks.list(filters={
        'label': f"{LABEL_NAME}=true"
    })

def remove(name: str, client: Optional[docker.DockerClient] = None):
    '''Removes a managed network.'''
    logger.debug(f"removing network, {name}...")

    client = get_docker(client)
    network = _find(name, client)

    if network is not None:
        network.remove()

def _find(name: str, client: docker.DockerClient) -> Optional[Network]:
    '''Find a managed network by the given name.

    If no network is found, None is returned. If a network is found, but it is
    not labeled for management, `dev.common.NotManaged` is raised. Otherwise,
    the network object is returned.
    '''
    logger.debug(f"finding networking, {name}...")

    try:
        network = client.networks.get(name)

        logger.debug('network found')

        if is_managed(network):
            logger.debug('and managed')

            return network
        else:
            raise NotManaged('network', name)
    except docker.errors.NotFound:
        logger.debug('network not found')

        return None

################################################################################
# Commands                                                                     #
################################################################################

@app.command(name='create')
def create_command(
    name: str = typer.Argument(..., help='The name of the new network.')
):
    '''Creates a new managed network.

    The new network is created globally using the "host" driver. This will allow
    containers to be attached to the network as well as access services running
    in those containers without port mapping.
    '''
    create(name)

    typer.echo('Network created.')

@app.command(name='list')
def list_command():
    '''Lists the managed networks.'''
    def to_tuple(network: Network):
        return [network.name, network.attrs['Created']]

    networks = builtin_list(map(to_tuple, list()))

    typer.echo(tabulate(networks, headers=['Name', 'Created At']))

@app.command(name='remove')
def remove_command(
    name: str = typer.Argument(..., help='The name of the network.')
):
    '''Removes a managed network.'''
    remove(name)

    typer.echo('Network removed.')
