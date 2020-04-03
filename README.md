![build status](https://travis-ci.org/dan-gittik/foobar.svg?branch=master)
![coverage](https://codecov.io/gh/dan-gittik/foobar/branch/master/graph/badge.svg)

# Moti



## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:tomerguralnik/Moti.git
    ...
    $ cd Moti/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [moti] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `moti` packages provides the following classes and subpackages:

- `Thought`

    This class is a representation of strings, 'thoughts', in the correct format
    which is a combination of user id, a timestamp and the thought 

    In addition, it provides the `serialize` method which returns a           representation of the thought object that fits the protocol of the package.
    And also a `deserialize` method wich recieves a string of packed byte data, unpacks it and if that data was in the package protocol then it returns a `Thought` object representing it.

    ```pycon
    >>> from thought import Thought
    >>> thought = Thought()
    >>> foo.run()
    'foo'
    >>> foo.inc(1)
    2
    >>> foo.add(1, 2)
    3
    ```

- `util`

    This subpackage provides the following classes: 

    - `Connection`   

       This class is a simplification of the socket class for the communication protocol of this package.

       This class provides the following methods:

       - `send` 
            
            This            

    ```pycon
    >>> from foobar import Bar
    >>> bar = Bar()
    >>> bar.run()
    'bar'
    ```

The `foobar` package also provides a command-line interface:

```sh
$ python -m foobar
foobar, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `foo` command, with the `run`, `add` and `inc`
subcommands:

```sh
$ python -m foobar foo run
foo
$ python -m foobar foo inc 1
2
$ python -m foobar foo add 1 2
3
```

The CLI further provides the `bar` command, with the `run` and `error`
subcommands.

Curiously enough, `bar`'s `run` subcommand accepts the `-o` or `--output`
option to write its output to a file rather than the standard output, and the
`-u` or `--uppercase` option to do so in uppercase letters.

```sh
$ python -m foobar bar run
bar
$ python -m foobar bar run -u
BAR
$ python -m foobar bar run -o output.txt
$ cat output.txt
BAR
```

Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `foobar`, not `foo` or
`bar`.

```sh
$ python -m foobar bar run -q # this doesn't work
ERROR: no such option: -q
$ python -m foobar -q bar run # this does work
```

To showcase these options, consider `bar`'s `error` subcommand, which raises an
exception:

```sh
$ python -m foobar bar error
ERROR: something went terribly wrong :[
$ python -m foobar -q bar error # suppress output
$ python -m foobar -t bar error # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```
