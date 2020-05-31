from flask import Flask, render_template, request, redirect, flash, send_file
from .utils import Config_handler
import click


@click.group()
def gui():
    pass

app = Flask(__name__, template_folder = "moti_web/build", static_folder = "moti_web/build/static")

def make_server(api_port, api_host):
    @app.route("/")
    @app.route("/<path:dummy>")
    def serve(dummy = None):
        return render_template('index.html', api_host = api_host, api_port = api_port)

@gui.command(name = 'run-server')
@click.option('--host', '-h', help = 'Ip', default = '127.0.0.1')
@click.option('--port', '-p', help =  'Port', default = 3000)
@click.option('--api-port', '-P', help = 'Api port', default = 5000)
@click.option('--api-host', '-H', help = 'Api host', default = '127.0.0.1')
@click.option('--config', '-c', help = 'name of config file', default = None)
def run_server(host, port, api_port, api_host, config = None):
    if config:
        config = Config_handler(config, 'gui')
        host = config.host
        port = config.port
        api_port = config.api_port
        api_host = config.api_host
    make_server(api_port, api_host)
    app.run(host = host, port =int(port))

if __name__ == '__main__':
    gui()
