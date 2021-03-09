"""CLI for the GISTyc routines."""

# Import standard libraries
import pathlib
import typing as t

# Import installed libraries
import click

# Import GISTyc
from . import GISTyc


# Set click commands
@click.command()
@click.option("-C", "--create", is_flag=True, help="Flag: Create GIST")
@click.option("-U", "--update", is_flag=True, help="Flag: Update GIST")
@click.option("-D", "--delete", is_flag=True, help="Flag: Delete GIST")
@click.option("-t", "--auth-token", help="GIST REST API token")
@click.option("-f", "--file-name", help="Absolute or relative file name path")
@click.option("-id", "--gist-id", default=None, help="GIST ID")
def run(
    create: bool, update: bool, delete: bool, auth_token: str, file_name: str, gist_id: str
) -> None:
    """CLI routine to call the GISTyc API to create, update and delete a GIST.

    All public functions echo the response back to the terminal.

    Parameters
    ----------
    create : bool
        Flag to trigger the create routine.
    update : bool
        Flag to trigger the update routine.
    delete : bool
        Flag to trigger the delete routine.
    auth_token : str
        GIST REST API token.
    file_name : str
        Absolute or relative file path. Required for create and update
    gist_id : str
        GIST ID for the update routine (if file name is ambiguous) and delete routine.

    Returns
    -------
    None.

    """
    # Set the GISTys class
    gist_api = GISTyc(auth_token=auth_token)

    # Create GIST routine
    if create:

        # Create a GIST with the sample file
        response_data = gist_api.create_gist(file_name=file_name)

        # Echo the resposen back to the terminal
        click.echo(str(response_data))

    # Update GIST routine
    elif update:

        # If not GIST ID is provided: use only the file name
        if not gist_id:
            response_data = gist_api.update_gist(file_name=file_name)

        # Else, use the GIST ID
        else:
            response_data = gist_api.update_gist(file_name=file_name, gist_id=gist_id)

        # Echo the resposen back to the terminal
        click.echo(str(response_data))

    # Delete GIST routine
    elif delete:

        # If not GIST ID is provided: use only the file name
        if not gist_id:
            response_int = gist_api.delete_gist(file_name=file_name)

        # Else, use the GIST ID
        else:
            response_int = gist_api.delete_gist(gist_id=gist_id)

        # Echo the resposen back to the terminal
        click.echo(str(response_int))


# A second CLI tool to parse directories
@click.command()
@click.option("-t", "--auth-token", help="GIST REST API token")
@click.option("-d", "--directory", help="Directory that contains Python scripts")
def dir_run(auth_token: str, directory: t.Union[pathlib.Path, str]) -> None:
    """CLI routine to create / update GitHub gists based on a given directory.

    This CLI routine takes a directory as an input and iterates recursively through it to determine
    all Python files. These files are then either created as a GIST or updated (if already
    present). Please note that GISTs must be unambiguous with respect to their file name. The
    update routine considers only the file name, since the directory input provides only a list
    of corresponding files.

    Parameters
    ----------
    auth_token : str
        GIST REST API token.
    directory : t.Union[pathlib.Path, str]
        Direcotry containing Python files.

    Returns
    -------
    None.

    """
    # Set the GISTys class
    gist_api = GISTyc(auth_token=auth_token)

    # Set the directory as a pathlib Path
    dir_path = pathlib.Path(directory)

    # Get a list of all gists
    gists = gist_api.get_gists()

    # Create a list of all file names (since gists may contain more than 1 file one needs to
    # flatten the list)
    gist_files_dictfiles = [list(gist_item["files"].keys()) for gist_item in gists]
    gist_files = [x for x in gist_files_dictfiles for x in x]

    # Create or update the GIST based on the Python file names within the given directory
    # Iterate through all Python files that are being found recursively within the directory.
    for python_filepath in dir_path.rglob("*.py"):

        # Echo the currently fetched file
        click.echo(python_filepath)

        # Get the filename
        python_filename = python_filepath.name

        # If the file name exists in the GIST list, update it, otherwise create one
        if python_filename in gist_files:
            click.echo("UPDATE")
            _ = gist_api.update_gist(file_name=python_filepath)
        else:
            click.echo("CREATE")
            _ = gist_api.create_gist(file_name=python_filepath)

    # Return a simple echo string
    click.echo("DONE")
