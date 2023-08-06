

class dicto(dict):

    def __init__(self, *args, **kwargs):
        super(DictO, self).__init__(*args, **kwargs)

        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DictO(value)

            elif hasattr(value, "__iter__"):
                self[key] = [ DictO(e) if isinstance(e, dict) else e for e in value ]


    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value



    def merge(self, merge_dct):
        """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
        updating only top-level keys, dict_merge recurses down into dicts nested
        to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
        ``self``.
        :param self: dict onto which the merge is executed
        :param merge_dct: self merged into self
        :return: None
        """

        for k, v in merge_dct.iteritems():
            if (k in self and isinstance(self[k], dict) and isinstance(merge_dct[k], collections.Mapping)):
                self[k].merge(DictO(merge_dct[k]))
            else:
                self[k] = merge_dct[k]
