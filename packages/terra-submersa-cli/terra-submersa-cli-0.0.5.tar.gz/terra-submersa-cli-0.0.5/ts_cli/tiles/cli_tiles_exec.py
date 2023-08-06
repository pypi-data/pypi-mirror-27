from ts_cli.rest_cli import RestCli
from ts_cli.output import Output

class CLITilesExec:
    def __init__(self, url_backend):
        self.rest_cli = RestCli(url_backend)

    def list(self, output):
        l = self.rest_cli.get_json('api/systems')
        out = Output()
        if output == 'id':
            fields = ['id']
        else:
            fields = ['id', 'title', 'description']
        return out.to_text_column(l, fields, max_char={'title': 50, 'description': 50})

    def add(self, image, properties):
        params = self.rest_cli.params_from_file(properties)
        return rest_cli.post_json('api/system', files={'file_image': open(image, 'rb')}, data=params)


    def add_sensys(self, image, txt, id, title, description, copyright):
        params = {}
        if not id is None:
            params['id'] = id
        if not title is None:
            params['text_title'] = title
        if not description is None:
            params['text_description'] = description
        if not copyright is None:
            params['text_copyright'] = copyright
        return self.rest_cli.post_json('api/sensys2d',
                                  files={
                                      'file_image': open(image, 'rb'),
                                      'file_txt': open(txt, 'rb'),
                                  },
                                  data=params)

    def remove(self, id):
        return self.rest_cli.delete_json('api/system/' + id)


    def zip(self, id, output):
        return self.rest_cli.get_file('zip/system/' + id, output)

    def unzip(self, input):
        return self.rest_cli.post_json('unzip/system', files={'archive': open(input, 'rb')})

