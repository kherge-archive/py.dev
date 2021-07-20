from dev.common import LABEL_NAME
from dev.command.network import app, create, list, remove
from typer.testing import CliRunner
from unittest import mock

################################################################################
# Management                                                                   #
################################################################################

def test_create():
    mock_client = mock.MagicMock()

    create('test', mock_client)

    mock_client.networks.create.assert_called_once_with(
        attachable=True,
        check_duplicate=True,
        driver='host',
        labels={
            LABEL_NAME: 'true'
        },
        name='test',
        scope='global'
    )

def test_list():
    mock_client = mock.MagicMock()
    mock_list = []

    mock_client.networks.list.return_value = mock_list

    result = list(mock_client)

    mock_client.networks.list.assert_called_once_with(filters={
        'label': f"{LABEL_NAME}=true"
    })

    assert result is mock_list

def test_remove():
    mock_client = mock.MagicMock()
    mock_network = mock.MagicMock()

    mock_client.networks.get.return_value = mock_network
    mock_network.attrs = {
        'Labels': {
            LABEL_NAME: 'true'
        }
    }

    remove('test', mock_client)

    mock_client.networks.get.assert_called_once_with('test')
    mock_network.remove.assert_called_once()

################################################################################
# Commands                                                                     #
################################################################################

runner = CliRunner()

@mock.patch('dev.command.network.create')
def test_create_command(mock_create: mock.Mock):
    result = runner.invoke(app, ['create', 'test'])

    mock_create.assert_called_once_with('test')

    assert result.stdout.strip() == 'Network created.'
    assert result.exit_code == 0

@mock.patch('dev.command.network.tabulate')
@mock.patch('dev.command.network.list')
def test_list_command(mock_list: mock.Mock, mock_tabulate: mock.Mock):
    mock_tabulate.return_value = 'tabulated'

    mock_network = mock.MagicMock()
    mock_network.attrs = {
        'Created': 'createdAt'
    }
    mock_network.name = 'test'

    mock_list.return_value = [mock_network]

    result = runner.invoke(app, ['list'])

    mock_list.assert_called_once()
    mock_tabulate.assert_called_once_with(
        [['test', 'createdAt']],
        headers=['Name', 'Created At']
    )

    assert result.stdout.strip() == 'tabulated'
    assert result.exit_code == 0

@mock.patch('dev.command.network.remove')
def test_remove_command(mock_remove: mock.Mock):
    result = runner.invoke(app, ['remove', 'test'])

    mock_remove.assert_called_once_with('test')

    assert result.stdout.strip() == 'Network removed.'
    assert result.exit_code == 0
