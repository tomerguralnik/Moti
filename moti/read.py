from .utils import Reader
import click

@click.group()
def reader():
	pass

@reader.command()
@click.option('--path', prompt='Path', help='Path of snapshot')
def read(path):
    reader = Reader(path, 'proto_reader')
    head = f'''Id: {reader.user_id}, User name: {reader.user_name}
Birth date: {reader.birth_date}, Gender: {reader.gender}'''
    print(head)
    for snapshot in reader:
        print("-----------new----------\n")
        print(snapshot)
