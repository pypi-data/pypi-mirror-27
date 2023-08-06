import requests
import re


class RestCli:
    def __init__(self, url_root):
        self.url_root = url_root

    def json_resp(self, resp):
        if resp.status_code == requests.codes.ok:
            try:
                return resp.json()
            except ValueError:
                raise Exception("Cannot parse json: " + resp.content)
        try:
            l = resp.json()
            raise Exception(l)
        except ValueError:
            raise Exception(resp.content)

    def post_json(self, uri_relative, files={}, data={}):
        r = requests.post(self.url_root + '/' + uri_relative,
                          files=files,
                          data=data
                          )
        return self.json_resp(r)

    def get_json(self, uri_relative):
        url = self.url_root + '/' + uri_relative
        r = requests.get(url)
        return self.json_resp(r)

    def get_file(self, uri_relative, output):
        url = self.url_root + '/' + uri_relative
        r = requests.get(url, stream=True)

        with open(output, 'wb') as fd:
            fd.write(r.content)

        return "file saved %s"%(output)

    def delete_json(self, uri_relative):
        url = self.url_root + '/' + uri_relative
        r = requests.delete(url)
        return self.json_resp(r)

    @staticmethod
    def params_from_file(parameter_file):
        """from each line of parameter_file, break by the '=' sign and build a dictionary"""
        re_param = re.compile("([^#].*?)=(.*)")
        ret = {}
        with open(parameter_file) as fp:
            for line in fp:
                res = re_param.match(line)
                if res:
                    ret[res.group(1)] = res.group(2)
        return ret
