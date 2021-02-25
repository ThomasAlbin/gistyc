"""CLI for the GISTyc routines"""

# Import installed libraries
import click

# Import GISTyc
from . import GISTyc

# Set click commands
@click.command()
@click.option('-C', '--create', is_flag=True, help='Flag: Create GIST')
@click.option('-U', '--update', is_flag=True, help='Flag: Update GIST')
@click.option('-D', '--delete', is_flag=True, help='Flag: Delete GIST')

@click.option('-t', '--auth-token', help='GIST REST API token')

@click.option('-f', '--file-name', help='Absolute or relative file name path')
@click.option('-id', '--gist-id', default=None, help='GIST ID')
def run(create, update, delete, auth_token, file_name, gist_id):
    """
    CLI routine to call the GISTyc API to create, update and delete a GIST. Echos the response back
    to the terminal.

    Parameters
    ----------
    create : Bool
        Flag to trigger the create routine.
    update : Bool
        Flag to trigger the update routine.
    delete : Bool
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

    # Update GIST routine
    elif update:

        # If not GIST ID is provided: use only the file name
        if not gist_id:
            response_data = gist_api.update_gist(file_name=file_name)

        # Else, use the GIST ID
        else:
            response_data = gist_api.update_gist(file_name=file_name, gist_id=gist_id)

    # Delete GIST routine
    elif delete:

        # Create a GIST with the sample file
        response_data = gist_api.delete_gist(gist_id=gist_id)

    # Echo the resposen back to the terminal
    click.echo(str(response_data))