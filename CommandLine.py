import click
import Exceptions
from wit import wit
# !/usr/bin/env python3
@click.group()
def cli():
    """ Wit Version Control CLI """
    pass
@click.command()
def init():
    try:
        wit.init()
        print("Your project is initialized by wit")
    except Exceptions.FileExistsError as e:
        print(e)
    except Exception as e:
        print(e)
cli.add_command(init)
@click.command()
@click.argument('name', type=click.STRING)
def add(name):
    try:
        wit.add(name)
        print("The file/folder has been successfully added to watchlist by wit")
    except Exceptions.witNotExistsError as e:
        print(e)
    except Exceptions.notValidPathSpec as e:
        print(e)
    except Exceptions.InvalidFileExtension as e:
        print(e)
    except Exception as e:
        print(e)


cli.add_command(add)


@click.command()
@click.argument('message', type=click.STRING)
def commit_m_message(message):
    try:
        wit.commit_m_message(message)
        print("Your changes have been successfully saved and can be viewed in the commit history")

    except Exception as e:
        print(e)


cli.add_command(commit_m_message)


@click.command()
def log():
    try:
        wit.log()
    except Exception as e:
        print(e)


cli.add_command(log)


@click.command()
def status():
    try:
        wit.status()
    except Exception as e:
        print(e)
cli.add_command(status)


@click.command()
@click.argument('commit_id', type=click.STRING)
def check_out(commit_id):
    try:
        wit.check_out(commit_id)
        print("You are back to version " + commit_id)
    except Exceptions.InvalidCommitId as e:
        print(e)
    except Exception as e:
        print(e)

cli.add_command(check_out)

@click.command()
def push():
    try:
        wit.push()
    except Exceptions.witNotExistsError as e:
        print(e)
    except Exception as e:
       print(e)
cli.add_command(push)


if __name__ == '__main__':
    cli()
