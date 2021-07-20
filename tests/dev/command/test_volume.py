from dev.common import LABEL_NAME
from dev.command.volume import app, create, list, remove
from typer.testing import CliRunner
from unittest import mock

################################################################################
# Management                                                                   #
################################################################################

def test_create():
    mock_client = mock.MagicMock()

    create('test', mock_client)

    mock_client.volumes.create.assert_called_once_with(
        name='test',
        driver='local',
        labels={
            LABEL_NAME: 'true'
        }
    )

def test_list():
    mock_client = mock.MagicMock()
    mock_list = []

    mock_client.volumes.list.return_value = mock_list

    result = list(mock_client)

    mock_client.volumes.list.assert_called_once_with(filters={
        'label': f"{LABEL_NAME}=true"
    })

    assert result is mock_list

def test_remove():
    mock_client = mock.MagicMock()
    mock_volume = mock.MagicMock()

    mock_client.volumes.get.return_value = mock_volume
    mock_volume.labels = {
        LABEL_NAME: 'true'
    }

    remove('test', mock_client)

    mock_client.volumes.get.assert_called_once_with('test')
    mock_volume.remove.assert_called_once()

################################################################################
# Commands                                                                     #
################################################################################

runner = CliRunner()

@mock.patch('dev.command.volume.create')
def test_create_command(mock_create: mock.Mock):
    result = runner.invoke(app, ['create', 'test'])

    mock_create.assert_called_once_with('test')

    assert result.stdout.strip() == 'Volume created.'
    assert result.exit_code == 0

@mock.patch('dev.command.volume.tabulate')
@mock.patch('dev.command.volume.list')
def test_list_command(mock_list: mock.Mock, mock_tabulate: mock.Mock):
    mock_tabulate.return_value = 'tabulated'

    mock_volume = mock.MagicMock()
    mock_volume.attrs = {
        'CreatedAt': 'createdAt'
    }
    mock_volume.name = 'test'

    mock_list.return_value = [mock_volume]

    result = runner.invoke(app, ['list'])

    mock_list.assert_called_once()
    mock_tabulate.assert_called_once_with(
        [['test', 'createdAt']],
        headers=['Name', 'Created At']
    )

    assert result.stdout.strip() == 'tabulated'
    assert result.exit_code == 0

@mock.patch('dev.command.volume.remove')
def test_remove_command(mock_remove: mock.Mock):
    result = runner.invoke(app, ['remove', 'test'])

    mock_remove.assert_called_once_with('test')

    assert result.stdout.strip() == 'Volume removed.'
    assert result.exit_code == 0
