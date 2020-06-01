# moti

Welcome to my Advanced System Design **FINAL!!!!** Project!

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:tomerguralnik/moti.git
    ...
    $ cd moti/
    ```
2. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```
3. Build the docker image:

    ```sh
    $ sudo docker build -t moti .
    ...
    ```
## Usage

To run the whole project:

1. Run the server-parser-saver-api-gui pipeline:
    
    ```sh
    $ ./scripts/run-pipeline.sh
    ...
    ```

2. In a seperate shell run a client to send some snapshots:

    ```sh
    $ python3 -m moti.client upload-sample <path-to-sample> -h 0.0.0.0 -p 8080
    ...
    ```

3. Visit the nice webpage you will find at 0.0.0.0:8080 where you will start to see the snapshots appearing

The `moti` packages provides the following Classes and Modules:

- `server`

    This module is a server that recieves connections, deserializes the data according to the protocol defined in the `protocol` module, and then publishes that data with a given publishing method. 
    
    The `server` cli contains the `run-server` funtion:

    ```sh
    $ python3 -m moti.server run-server <message-queue-url> -p/--port <port> -h/--host <host>\ 
    > -c/--config <path-to-config-file>
    ```
    The run-server that's in the cli recieves a url to a message queue and a few optional arguments:
   - **port** which defaults to 8000 
   - **host** which defaults to 127.0.0.1
   - **config** which defaults to `None`, if config is given then it overrides all the other variables with data from the config file
   
    The server also exposes the function `run_server`
    
    ```python
    >>> from moti.server import run_server
    >>> run_server(host = '127.0.0.1', port = 8000, publish = print)
    ... # listen on host:port and pass recieved messages to publish
    ```
- `client`

    This module is client that parses a sample file and sends it's data to the `server`.
    
    The `client` exposes the function upload-sample in it's cli:
    
    ```sh
    $ python3 -m moti.client upload-sample <sample-path> -p/--port <port> -h/--host <host>\ 
    > -c/--config <path-to-config-file>
    ```
    The upload-sample that's in the cli recieves a path to a `sample file` and a few optional arguments:
   - **port** which defaults to 8000 
   - **host** which defaults to 127.0.0.1
   - **path-to-config-file** which defaults to `None`, if config is given it overrides all the other variables with data from the config file
   
   The `client` also exposes `upload_sample` as a cli function: 

   ```python
    >>> from moti.client import upload_sample
    >>> upload_sample(host = '127.0.0.1', port = 8000, path = 'sample.mind.gz')
    ... # send snapshots from 'sample.mind.gz' to host:port
    ```

- `parsers`   

    This module consumes snapshots from a message queue parses them and publishes the results back to the message queue
    
    `parsers` exposes the following *cli* functions:
    
    ```sh
    $ python3 -m moti.parsers parse <field> <data>
    Parses the field of data with a parsers that can parse the field
    
    $ python3 -m moti.parsers run-parser <filed> <message-queue-url>\
    > -c/--config <path-to-config-file>
    Runs all the parsers of a certain field as a service,
    consumes messages from a message queue and publishes back the parsed results
    
    $ python3 -m moti.parsers run-all-parsers <message-queue-url>\
    > -c/--config <path-to-config-file>
    Runs all parsers as a service, consumes message from a message
    queue and publishes back the parsed results
    ```
    The arguments for the `parsers` cli function are:
    - **field** a field of the snapshot to parse
    - **data** a path to data that parsers can parse
    - **message-queue-url** a url of a message queue, format explained in `utils.publisher`
    - **path-to-config-file** which defaults to `None`, if config is given it overrides all the other variables with data from the config file
    
    `parsers` exposes the run_parser function
    ```python
    >>> from moti.parsers import run_parser
    >>> data = some_encoded_path_to_json #ascii encoded
    >>>run_parser('pose', data)
    Parsed 'pose' field from data
    ```
- `saver`

    The saver reads parsed data from the messsage queue and saves it to a database
    
    The `saver` exposes the following *cli* functions:
    ```sh
    $ python3 -m moti.saver save <field> <data> -d/--database <database_url>
    This saves the data in path_to_data to the database pointed to in database_url
    $ python3 -m moti.saver run-saver <database_url> <queue_url>\
    > -c/--config <path-to-config-file>
    ```
    The arguments for the `saver` cli function are:
    - **field** a field of the snapshot to save
    - **data** a path to data that saver can save
    - **queue-url** a url of a message queue, format explained in`utils.consumer`
    - **database_url** a url of a database, format explained in `utils.savers`
    - **path-to-config-file** which defaults to `None`, if config is given it overrides all the other variables with data from the config file

    `saver` also exposes the class `Saver`:
    ```python
    >>> from moti.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = ...
    >>> saver.save('pose' ,data)
    ... # saves data as pose of a snapshot
    ```
- `api`

    This module runs an api server that serves data inside a database
    The `api` handles `GET` requests to specific endpoints, these endpoints are described in the documentation of `moti.api` and `moti.cli`
    The `api` exposes the `run-server` *cli* function:
    ```sh
    $ python3 -m moti.api run-server -h/--host <host> -p/--port <port> -d/--database <database_url>\
    > -c/--config <path_to_config_file>
    ```
    The arguments for the `api` cli function are:
   - **port** which defaults to 5000 
   - **host** which defaults to 127.0.0.1
    - **database_url** a url of a database, format explained in `utils.database_reader`
    - **path-to-config-file** which defaults to `None`, if config is given it overrides all the other variables with data from the config file

    The `api` also exposes the `run_api_server` api function:
    ```python
    >>> form moti.api import run_api_server
    >>> run_api_server(host, port, database)
    ... # runs the pai server on host:port and exposes the data in the database
    ```
    
- `cli`

    The `cli` consumes the api with the following *cli* functions:
    ```python
    $ python3 -m cortex.cli get-users
    ... # gets a list of all users 
    $ python3 -m cortex.cli get-user <user_id>
    ... # gets a user's details
    $ python3 -m cortex.cli get-snapshots <user_id>
    ... # get all snapshots of a certain user
    $ python3 -m cortex.cli get-snapshot <user_id> <snapshot_id>
    ... # get information of a chosen snapshot
    $ python3 -m cortex.cli get-result <user_id>  <snapshot_id> <field>
    ... # get a selected field of a snapshot
    ```
- `gui`

    The `gui` consumes the `api` and displays the snapshots in a nice and fun way
    Run the gui with the cli function:
    ```sh
    $ python3 -m moti.gui run-server -h/--host <host> -p/--port <port> -P/--api-port <api-port>\
    > -H/--api-host <api-host> -c/--config <path-to-config-file> 
    ```
    The arguments for the `api` cli function are:
    - **port** which defaults to 8080
    - **host** which defaults to 127.0.0.1
    - **api-port** which defaults to 5000 
    - **api-host** which defaults to 127.0.0.1
    - **path-to-config-file** which defaults to `None`, if config is given it overrides all the other variables with data from the config file
    
    The `gui` can also be run with an api function:
    ```python
    >>> from moti.gui import run_server
    >>> run_server(host, port, api_host, api_port)
    ... # runs the gui server on host:port and consumes the api at api_host:api_port
    ```

## Drivers
This project has many generic classes which can be defined or modified by creating drivers
These classes are:
- `Reader` which is defined and documented in `moti.utils.reader.py`
- `Parser` which is defined and documented in `moti.utils.parser.py`
- `Publisher` which is defined and documented in `moti.utils.publisher.py`
- `Consumer` which is defined and documented in `moti.utils.consumer.py`
- `Saver` which is defined and documented in `moti.saver.py`
- `DatabaseReader` which is defined and documented in `moti.utils.database_reader.py`
- `Config_handler` which is defined and documented in `moti.utils.handle_config.py`