import click

from . import GISTyc

@click.command()
@click.option('-C', '--create', is_flag=True, help='Flag: Create GIST')
@click.option('-U', '--update', is_flag=True, help='Flag: Update GIST')
@click.option('-D', '--delete', is_flag=True, help='Flag: Delete GIST')

@click.option('-f', '--file-name', help='Absolute or relative file name path')
@click.option('-id', '--gist-id', help='GIST ID')

def run(create, update, delete, file_name, gist_id):
    
    pass