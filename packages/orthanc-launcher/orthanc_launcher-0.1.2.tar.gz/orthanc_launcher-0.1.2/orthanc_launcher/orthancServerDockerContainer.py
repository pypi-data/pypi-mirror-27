import os
import json
import tempfile
import sys
import traceback
import docker
from threading import Thread
from .orthancServer import OrthancServer, OrthancServerVersion
from osimis_logging import LogHelpers
from osimis_cmd_helpers import CmdHelpers


class OrthancServerDockerContainer(OrthancServer):

    dockerImage = 'osimis/osimis-webviewer-plugin:latest'

    def __init__(self, name, aet, dicomPort = 4242, httpPort = 8042):
        super().__init__(name, aet, dicomPort, httpPort)

        self._containerId = None
        self.trace = True

    @staticmethod
    def loadExecutable(version = OrthancServerVersion.STABLE):
        if version == OrthancServerVersion.STABLE:
            OrthancServerDockerContainer.dockerImage = 'osimis/orthanc-webviewer-plugin:1.0.0'
        elif version == OrthancServerVersion.STABLE_WITH_WVP:
            OrthancServerDockerContainer.dockerImage = 'osimis/osimis-webviewer-pro:1.0.0'
        elif version == OrthancServerVersion.NIGHTLY:
            OrthancServerDockerContainer.dockerImage = 'osimis/orthanc-webviewer-plugin:dev'
        else:
            OrthancServerDockerContainer.dockerImage = 'osimis/osimis-webviewer-pro:dev'
        return


    def _launch(self, configurationFilePath = None):
        # modify the config file actually references local path (where this script is executing).  These files should be in the container ...
        # => we might need to copy files and adapt the config file

        self._logInfo('configuration file before transformation: {0}'.format(json.dumps(self.config, indent = 4)))

        # check if an old container with same name already exist
        ret, output = CmdHelpers.run('Checking for old container',
                                     'docker ps -af name={containerName} -q'.format(
                                         containerName = self.config['DicomAet'].lower()
                                     ))
        if output is not None and len(output) > 0:
            CmdHelpers.run('Deleting old container', 'docker rm -f {containerId}'.format(containerId = output.strip()))

        # create a volume if it does not exist yet
        ret, output = CmdHelpers.run('Create Docker volume',
                                     'docker volume create --name=orthanc-storage-{volumeName}'.format(
                                         volumeName = self.config['DicomAet'].lower()
                                     ))

        # use the host network-mode so this is similar to Orthanc running on the host (127.0.0.1 points to the host and not to the container itself)
        ret, output = CmdHelpers.run('Create Docker container',
                                     'docker create --name={containerName} --net=host --volume orthanc-storage-{volumeName}:/var/lib/orthanc/db {image} {upgrade} {verbose} {trace} /tmp/orthanc.json'.format(
                                         containerName = self.config['DicomAet'].lower(),
                                         volumeName = self.config['DicomAet'].lower(),
                                         image = OrthancServerDockerContainer.dockerImage,
                                         upgrade = '--upgrade' if self.upgradeDb else '',
                                         verbose = '--verbose' if self.verbose else '',
                                         trace = '--trace' if self.trace else ''
                                     ))

        if ret != 0:
            raise Exception("Could not create docker container for Orthanc: {ret} + {output}".format(ret = ret, output = output))

        self._containerId = output.strip()

        # let's make a copy of the config since we are going to modify it
        config = dict(self.config)

        # we'll probably never access the files in the container, so let's use directory that are already there (we can't create directories with 'docker cp')
        config['StorageDirectory'] = '/var/lib/orthanc/db'
        config['IndexDirectory'] = '/var/lib/orthanc/db'
        config['LogsDirectory'] = '/var/lib/orthanc/logs'

        # add all plugins
        config["Plugins"] = ['/usr/share/orthanc/plugins']

        # when connecting from the host, we are actually connecting from 'remote' => allow remote access
        config['RemoteAccessAllowed'] = True

        # copy SSL certificate and adapt path
        if config.get('SslCertificate') is not None:
            CmdHelpers.run('Copying SSL certificate',
                           'docker cp {src} {containerId}:/tmp'.format(containerId = self._containerId,
                                                                       src = config['SslCertificate']))
            config['SslCertificate'] = os.path.join('/tmp', os.path.basename(config['SslCertificate']))

        # copy Lua scripts and adapt path
        if config.get('LuaScripts'):
            newLuaScripts = []
            for luaScript in config['LuaScripts']:
                CmdHelpers.run('Copying Lua script', 'docker cp {src} {containerId}:/tmp'.format(containerId = self._containerId,
                                                                                                 src = luaScript))
                newLuaScripts.append(os.path.join('/tmp', os.path.basename(luaScript)))
            config['LuaScripts'] = newLuaScripts

        # handle HttpsCACertificates
        if config.get('HttpsCACertificates') is not None:
            CmdHelpers.run('Copying HttpsCACertificates certificate',
                           'docker cp {src} {containerId}:/tmp'.format(containerId = self._containerId,
                                                                       src = config['HttpsCACertificates']))
            config['HttpsCACertificates'] = os.path.join('/tmp', os.path.basename(config['HttpsCACertificates']))

        # copy config file
        if configurationFilePath is None:
            self._temporaryConfigurationFile = tempfile.NamedTemporaryFile(delete = False)
            configurationFilePath = self._temporaryConfigurationFile.name
            self.generateConfigurationFile(configurationFilePath, config)

        CmdHelpers.run('Copying config file',
                       'docker cp {src} {containerId}:/tmp/orthanc.json'.format(containerId = self._containerId,
                                                                                src = configurationFilePath),
                       stdoutCallback = self._logInfo)

        self._process = CmdHelpers.start('docker start {containerId}'.format(containerId = self._containerId))
        self._isRunning = True

        # actually get the logs from 'docker logs' start a thread that will listen to Orthanc output and log it through the logging facility
        self._loggerProcess = CmdHelpers.start('docker logs --follow {containerId}'.format(containerId = self._containerId))
        self._loggerThread = Thread(target = self._logOrthancOutput,
                                    name = 'Orthanc Logger {0}'.format(self.config['Name']))
        self._loggerThread.start()

    def _stop(self):

        CmdHelpers.run('stoping container',
                       'docker stop {containerId}'.format(containerId = self._containerId))
        self._process.wait()  # wait the process actually exits

        CmdHelpers.run('removing container',
                       'docker rm {containerId}'.format(containerId = self._containerId))
