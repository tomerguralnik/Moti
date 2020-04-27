from pathlib import Path
import click
import re
from flask import Flask
#from .cli import cli
web_server = Flask(__name__)
data_directory = ''
_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''<li><a href="/users/{user_id}">user {user_id}</a></li>'''
_USER_ID_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {id}</title>
    </head>
    <body>
        <table>
            {text}
        </table>
    </body>
</html>
'''
_USER_ID_ENTRY_HTML = '''<tr>
    <td>{date}</td>
    <td>{thought}</td>
</tr>'''
_TIME_FORMAT = '{Y}-{M}-{D} {H}:{m}:{S}'

'''
@web_server.route('/')
def index_page():
    global data_directory
    p = Path(data_directory)
    users = []
    for stuff in p.iterdir():
        stuff = stuff.name.split("/")
        users.append(_USER_LINE_HTML.format(user_id=stuff[-1]))
    data = _INDEX_HTML.format(users='\n'.join(users))
    return data


@web_server.route('/users/<int:user_id>')
def user_pages(user_id):
    global data_directory
    p = Path(data_directory)
    p = p / f'{user_id}'
    if not p.exists():
        return
    thoughts = []
    for stuff in p.iterdir():
        stuff = stuff.name.split('/')
        s = re.split("[-,_,.]", stuff[-1])
        time = _TIME_FORMAT.format(Y=s[0], M=s[1], D=s[2],
                                   H=s[3], m=s[4], S=s[5])
        f = (p / stuff[-1]).open()
        for line in f:
            thoughts.append(_USER_ID_ENTRY_HTML.format(date=time,
                                                       thought=line))
        f.close()
    data = _USER_ID_HTML.format(text='\n'.join(thoughts), id=user_id)
    return data


@cli.command()
@click.option('--address', prompt='Address', help='Adress of server')
@click.option('--data', prompt='Data directory', help='Path to data directory')
def run_webserver(address, data):
    global data_directory
    data_directory = data
    address = address.split(':')
    address[1] = int(address[1])
    web_server.run(*address)
'''