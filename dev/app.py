from typing import NoReturn

import logging
import sys
import typer

# Configure the root logger.
def config_logger(verbosity: int):
    levels = {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG
    }

    if verbosity > 3:
        verbosity = 3

    logging.basicConfig(
        format='%(name)s: %(message)s',
        level=levels[verbosity]
    )

    return logging.getLogger(__name__)

# Improve error handling.
def handle_error(type, error: BaseException, trace) -> NoReturn:
    '''Displays the error before exiting.

    By default, any error that is handled will simply have its string
    representation printed to stderr and the script will exit with a status
    code of 1 (one). However, if the logging level for the root logger is set
    to DEBUG, the default exception hook will be used to render the complete
    error.
    '''
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        sys.__excepthook__(type, error, trace)
    else:
        typer.secho(str(error), fg=typer.colors.RED, file=sys.stderr)

        sys.exit(1)

sys.excepthook = handle_error

# Configure Typer.
app = typer.Typer(
    context_settings={
        'help_option_names': ['-h', '--help']
    },
    add_completion=False
)

# Run the requested command.
@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    verbosity: int = typer.Option(
        0,
        '-v',
        '--verbose',
        count=True,
        help='Increase logging verbosity.'
    )
):
    '''Creates and manages containerized development environments.'''
    logger = config_logger(verbosity)

    if context.invoked_subcommand is not None:
        return

    logger.debug('invoking default')

if __name__ == '__main__':
    app()
