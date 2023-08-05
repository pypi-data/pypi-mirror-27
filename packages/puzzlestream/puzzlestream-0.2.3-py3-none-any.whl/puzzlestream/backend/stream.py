import diskcache as dc

from puzzlestream.backend.reference import PSCacheReference


class PSStream(dc.Cache):

    def __init__(self, path, *args):
        super().__init__(path, *args)

    def getItem(self, id, key):
        item = super().__getitem__(str(id) + "-" + str(key))

        # delete item if it is a reference to something that no longer exists
        if (isinstance(item, PSCacheReference) and not
                super().__contains__(str(item.sectionID) + "-" + str(key))):
            super().__delitem__(str(id) + "-" + str(key))
            raise KeyError

        return item

    def setItem(self, id, key, data):
        super().__setitem__(str(id) + "-" + str(key), data)
