from .utils import Reader
import click

@click.group()
def reader():
    pass

@reader.command()
@click.option('--path', '-p', prompt='Path', help='Path of snapshot')
def read(path):
    count = 0
    reader = Reader(path, 'proto_reader')
    head = f'''Id: {reader.user_id}, User name: {reader.user_name}
Birth date: {reader.birth_date}, Gender: {reader.gender}'''
    print(head)
    for snapshot in reader:
        count += 1
        print("-----------new----------\n")
        print(snapshot)
        print(count)

if __name__ == '__main__':
    reader()