import click

from . import GISTyc

@click.command()
@click.option('-C', '--create', is_flag=True, help='Flag: Create GIST')
@click.option('-U', '--update', is_flag=True, help='Flag: Update GIST')
@click.option('-D', '--delete', is_flag=True, help='Flag: Delete GIST')

@click.option('-t', '--auth-token', help='GIST REST API token')

@click.option('-f', '--file-name', help='Absolute or relative file name path')
@click.option('-id', '--gist-id', default=None, help='GIST ID')

def run(create, update, delete, auth_token, file_name, gist_id):

    gist_api = GISTyc(auth_token=auth_token)

    if create:

        # Create a GIST with the sample file
        response_data = gist_api.create_gist(file_name=file_name)

    elif update:
        
        if not gist_id:
            response_data = gist_api.update_gist(file_name=file_name)
        else:
            response_data = gist_api.update_gist(file_name=file_name, gist_id=gist_id)

    elif delete:
    
        # Create a GIST with the sample file
        response_data = gist_api.delete_gist(gist_id=gist_id)
    
    click.echo(str(response_data))
