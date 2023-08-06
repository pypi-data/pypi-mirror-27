import click
from ts_cli.rest_cli import CannotParseJsonException, ResponseError
from ts_cli.tiles.cli_tiles_exec import CLITilesExec
import sys


class CLITiles:
    """
    ts-tiles command.
    each cmd_xyz command, parsing out cmmand line is associated with a RestCliExec method, doing the actual execution
    """

    def __init__(self):
        pass

    @staticmethod
    def exec_and_out(rest_url, f_call):
        try:
            rex = CLITilesExec(rest_url)
            out = f_call(rex)
            print(out)
        except (CannotParseJsonException, ResponseError) as e:
            click.echo('ERROR: ' + str(e), err=True)
            sys.exit(1)


    @click.group()
    def cli():
        """Process tile system in and out from a terra submersa portal backend
    \b
        Check the possible commands with ts-tiles COMMAND --help
    """
        pass

    @click.command(name='list')
    @click.argument('rest_url')
    @click.option('--output', type=click.Choice(['id', 'full']), default='full',
                  help="output format for column defintion (default is 'full')")
    def cmd_list(rest_url, output):
        """
        list all tile systems from a given repository

        \b
        REST_URL: the backend REST root url (such as 'http://Localhost:9000' or 'http://terra-submersa.demo.octo.ch/tiles')

        \b
        Examples:
            ts-tiles list http://localhost:9000
            ts-tiles list http://localhost:9000 --output=id
        """
        def f_call(rex):
            return rex.list_txt(output)

        CLITiles.exec_and_out(rest_url, f_call)

    @click.command(name='add')
    @click.argument('rest_url')
    @click.argument('image')
    @click.argument('properties')
    def cmd_add(rest_url, image, properties):
        """
        Create a tile system based on on a png image and a properties file.

        \b
        REST_URL: the backend REST root url (such as 'http://Localhost:9000' or 'http://terra-submersa.demo.octo.ch/tiles')
        IMAGE: path to a png file
        PROPERTIES: path to a properties file, with id, description, coordinate boundaries etc. See https://gitlab.com/terra-submersa/data-kilada/tree/master/misc for examples
        """
        def f_call(rex):
            return rex.add(image, properties)

        CLITiles.exec_and_out(rest_url, f_call)

    @click.command(name='add-sensys')
    @click.argument('rest_url')
    @click.argument('image')
    @click.argument('txt')
    @click.option('--id', help="tile system id (default is based on filename)")
    @click.option('--title', help="tile system title  (default is based on filename)")
    @click.option('--description', help="a longer description")
    @click.option('--copyright', help="the copyright field")
    def cmd_add_sensys(rest_url, image, txt, id, title, description, copyright):
        """
        Create a tile system based on on a sensys png and a tif.txt file.

        \b
        REST_URL: the backend REST root url (such as 'http://Localhost:9000' or 'http://terra-submersa.demo.octo.ch/tiles')
        IMAGE: path to a png file
        TXT: path to the SENSYS tif.txt file
        """
        def f_call(rex):
            return rex.add_sensys(image, txt, id, title, description, copyright)

        CLITiles.exec_and_out(rest_url, f_call)

    @click.command(name='remove')
    @click.argument('rest_url')
    @click.argument('id')
    def cmd_delete(rest_url, id):
        """
        Delete a tile system and the relative png tile.

        \b
        REST_URL: the backend REST root url (such as 'http://Localhost:9000' or 'http://terra-submersa.demo.octo.ch/tiles')
        ID: the tile system id, such as reported by the list command
        """
        def f_call(rex):
            return rex.remove(id)

        CLITiles.exec_and_out(rest_url, f_call)

    @click.command(name='zip')
    @click.argument('rest_url')
    @click.argument('id')
    @click.argument('output')
    def cmd_zip(rest_url, id, output):
        """
        DDownload a zip archive for a cmplete tile system, with png tiles and annotations.

        \b
        REST_URL: the backend REST root url (such as 'http://Localhost:9000' or 'http://terra-submersa.demo.octo.ch/tiles')
        ID: the tile system id, such as reported by the list command
        OUTPUT: the output file name (will be erased if already exits)

        \b
        Example:
            ts-tiles zip http://localhost:9000 sensys-JULY_18_B /tmp/sensys-JULY_18_B.zip
        """
        def f_call(rex):
            return rex.zip(id, output)

        CLITiles.exec_and_out(rest_url, f_call)

    @click.command(name='unzip')
    @click.argument('rest_url')
    @click.argument('input')
    def cmd_unzip(rest_url, input):
        """
        Upload a zip archive to create a complete tile system, with png tiles and annotations.
        This operation is the mirror of the zip command

        \b
        REST_URL: the backend REST root url (such as 'http://Localhost:9000' or 'http://terra-submersa.demo.octo.ch/tiles')
        INTPUT: the zip archive file name

        \b
        Example:
            ts-tiles unzip http://localhost:9000 /tmp/sensys-JULY_18_B.zip
        """
        def f_call(rex):
            return rex.unzip(input)

        CLITiles.exec_and_out(rest_url, f_call)

    cli.add_command(cmd_list)
    cli.add_command(cmd_add)
    cli.add_command(cmd_add_sensys)
    cli.add_command(cmd_zip)
    cli.add_command(cmd_unzip)
    cli.add_command(cmd_delete)


def main():
    cli = CLITiles()
    cli.cli()
