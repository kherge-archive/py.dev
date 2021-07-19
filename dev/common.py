from docker import DockerClient
from docker.models.containers import Container
from docker.models.images import Image
from docker.models.networks import Network
from docker.models.volumes import Volume
from typing import Final, Optional, Union

import docker
import logging

logger = logging.getLogger(__name__)

# The name of the managed label.
LABEL_NAME: Final[str] = 'io.github.kherge.py-dev.managed'

# The Docker object type.
DockerObject = Union[Container, Image, Network, Volume]

def get_docker(client: Optional[DockerClient]):
    '''Returns the given client, or creates one.

    If the given client is `None`, then `docker.from_env()` is used to create
    a new client which is then returned. Otherwise, the given client is simply
    returned.
    '''
    if client is None:
        logger.debug('using client from docker.from_env()')

        client = docker.from_env()
    else:
        logger.debug('using given client')

    return client

def is_managed(obj: DockerObject) -> bool:
    '''Checks if the given object is tagged for management.'''
    return (
        hasattr(obj, "labels")
        and LABEL_NAME in obj.labels
        and obj.labels[LABEL_NAME] == 'true'
    )

class NotManaged(Exception):
    '''An error raised when manipulating an unmanaged object.'''

    def __init__(self, *args):
        self.name = args[1]
        self.type = args[0]

    def __str__(self):
        return f"Docker {self.type} object, {self.name}, is not managed."
