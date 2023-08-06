class Output:
    def __init__(self):
        pass

    def select_fields(self, objects, fields):
        return [{f: x[f] for f in fields} for x in objects]

    def to_text_column(self, objects, keys, max_char={}):
        """"
        output a list of objects, aligning text column to the longet of each field
        Let's assume they all have the same fields, so we can take the first
        :param objects a list of object dictionaries
        :param keys the list of key to be output
        :param max_char (optional) the maximum number of character to be output for the defined keys: truncating and adding "..."
        """
        max_per_fields = {f: max([len(str(x[f])) for x in objects]) for f in keys}
        for k, v in max_char.items():
            if k in max_per_fields:
                max_per_fields[k] = min(max_per_fields[k], v)

        str_out = ""
        for x in objects:
            for f in keys:
                s = str(x[f])
                if (len(s) > max_per_fields[f]):
                    s = s[0:(max_per_fields[f] - 3)] + '...'
                str_out = str_out + s
                if f != keys[-1]:
                    str_out = str_out + (' ' * (max_per_fields[f] - len(s) + 1))
            str_out = str_out + "\n"

        return str_out