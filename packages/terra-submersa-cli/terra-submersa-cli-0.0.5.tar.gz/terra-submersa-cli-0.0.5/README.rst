# Terra Submersa - Command Line Interface

We propose a CLI toolbox to interact with the Terra Submersa data portal

## usage

   ts-cli tiles list
   ts-cli tiles list --id-only

## Development

Once in the cloned directory, the smoothest way to load the package in an interactive way (thus pursuing code creation)

    pip install -e .

### Dealing with dependencies
The Python package deals with its own dependences definition in the `setup.py`file.
Go check for more infromation https://packaging.python.org/tutorials/distributing-packages

#### Util dependencies
It is nonetheless possible to install devlopment utilities (for testing or such), in a virtual environment

    pip3 install virtualenv
    virtualenv ts-venv/
    #sets the correct paths
    . bin/activate

    pip install -r requirements-dev.txt

#### Save the libraries you install in your env

    pip freeze > requirements-dev.txt

### testing

