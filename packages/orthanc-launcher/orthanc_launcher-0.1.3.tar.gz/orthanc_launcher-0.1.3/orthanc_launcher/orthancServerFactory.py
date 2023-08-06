import json
import re
import platform, os, tempfile
from .orthancServerDockerContainer import OrthancServerDockerContainer
from .orthancServer import OrthancServer, OrthancServerVersion

class OrthancServerFactory:

    @staticmethod
    def getOrthancServer(name, aet, dicomPort = 4242, httpPort = 8042):
        if platform.system() == 'Linux':
            return OrthancServerDockerContainer(name, aet, dicomPort, httpPort)
        else:
            return OrthancServer(name, aet, dicomPort, httpPort)


    @staticmethod
    def loadExecutable(version = OrthancServerVersion.STABLE, targetFolder = None, overwriteExisting = False):
        if platform.system() == 'Linux':
            OrthancServerDockerContainer.loadExecutable(version)
        else:
            OrthancServer.loadExecutable(version = version,
                                         targetFolder = targetFolder,
                                         overwriteExisting = overwriteExisting)

