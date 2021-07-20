from dev.common import LABEL_NAME, NotManaged, get_docker, is_managed
from docker.models.volumes import Volume
from tabulate import tabulate
from typing import Optional

import docker
import logging
import typer

app = typer.Typer(
    help='''Manages volumes.

    Volumes are used to persist the files in the home directory across different
    containers. This allows for iterative changes to be made to container images
    without losing any configuration settings persisted to the home folder.
    ''',
    name='volume'
)

builtin_list = list
logger = logging.getLogger(__name__)

################################################################################
# Management                                                                   #
################################################################################

def create(name: str, client: Optional[docker.DockerClient] = None):
    '''Creates a new managed volume.'''
    logger.debug(f"creating volume, {name}...")

    client = get_docker(client)

    client.volumes.create(
        name=name,
        driver='local',
        labels={
            LABEL_NAME: 'true'
        }
    )

def list(client: Optional[docker.DockerClient] = None):
    '''Lists the managed volumes.'''
    logger.debug('listing volumes...')

    client = get_docker(client)

    return client.volumes.list(filters={
        'label': f"{LABEL_NAME}=true"
    })

def remove(name: str, client: Optional[docker.DockerClient] = None):
    '''Removes a managed volume.'''
    logger.debug(f"removing volume, {name}...")

    client = get_docker(client)
    volume = _find(name, client)

    if volume is not None:
        volume.remove()

def _find(name: str, client: docker.DockerClient) -> Optional[Volume]:
    '''Find a managed volume by the given name.

    If no volume is found, None is returned. If a volume is found, but it is
    not labeled for management, `dev.common.NotManaged` is raised. Otherwise,
    the volume object is returned.
    '''
    logger.debug(f"finding volume, {name}...")

    try:
        volume = client.volumes.get(name)

        logger.debug('volume found')

        if is_managed(volume):
            logger.debug('and is managed')

            return volume
        else:
            raise NotManaged('volume', name)
    except docker.errors.NotFound:
        logger.debug('volume not found')

        return None

################################################################################
# Commands                                                                     #
################################################################################

@app.command(name='create')
def create_command(
    name: str = typer.Argument(..., help='The name of the new volume.')
):
    '''Creates a new managed volume.

    The new volume is created using the "local" driver.
    '''
    create(name)

    typer.echo('Volume created.')

@app.command(name='list')
def list_command():
    '''Lists the managed volumes.'''
    def to_tuple(volume: Volume):
        return [volume.name, volume.attrs['CreatedAt']]

    volumes = builtin_list(map(to_tuple, list()))

    typer.echo(tabulate(volumes, headers=['Name', 'Created At']))

@app.command(name='remove')
def remove_command(
    name: str = typer.Argument(..., help='The name of the volume.')
):
    '''Removes a managed volume.'''
    remove(name)

    typer.echo('Volume removed.')
