from puzzlestream.backend.dict import PSDict
from puzzlestream.backend.reference import PSCacheReference


class PSStreamSection:

    def __init__(self, sectionID, stream):
        self.__stream = stream
        self.__id = sectionID
        self.changelog = {}

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    @property
    def id(self):
        return self.__id

    def updateData(self, lastStreamSectionID, moduleID,
                   data, log, clean=False):
        for key in data:
            if key in self.changelog and key not in log:
                ref = PSCacheReference(lastStreamSectionID)
                if key in data:
                    del data[key]
                data[key] = ref

        for key in data:
            self.__stream.setItem(self.__id, key, data[key])

        self.__logChanges(moduleID, log)
        if clean:
            self.__cleanStream(self.changelog)

    def __cleanStream(self, log):
        for key in self.__stream:
            ID = key.split("-")[0]
            keyn = key.replace(ID + "-", "")

            if keyn not in log and int(ID) == self.__id:
                del self.__stream[key]

    def __logChanges(self, moduleID, log):
        for item in log:
            if item in self.changelog:
                self.changelog[item].append(moduleID)
            else:
                self.changelog[item] = [moduleID]
        self.data.resetChangelog()

    @property
    def data(self):
        return PSDict(self.__id, self.__stream)

    def addSection(self, streamSection):
        for key in streamSection.changelog:
            ref = PSCacheReference(streamSection.id)
            self.__stream.setItem(self.__id, key, ref)
        self.changelog.update(streamSection.changelog)

    def copy(self, sectionID):
        new = PSStreamSection(sectionID, self.__stream)
        new.addSection(self)
        return new
