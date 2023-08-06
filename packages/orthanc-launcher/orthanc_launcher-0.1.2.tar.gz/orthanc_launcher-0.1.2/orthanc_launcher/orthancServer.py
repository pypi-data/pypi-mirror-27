import json
import tempfile
import signal
import os
import platform
import subprocess
import time
import zipfile
import shutil
import requests
from threading import Thread
from osimis_logging import LogHelpers
from osimis_file_helpers import FileHelpers
from osimis_timer import TimeOut
from .orthancMinimalClient import OrthancMinimalHttpClient


"""A set of utilities to configure and launch an OrthancServer"""


class OrthancServerVersion:
    STABLE = 'STABLE'
    NIGHTLY = 'NIGHTLY'
    STABLE_WITH_WVP = 'STABLE_WITH_WVP'
    NIGHTLY_WITH_WVP = 'NIGHTLY_WITH_WVP'


class OrthancServer:
    _logger = LogHelpers.getLogger('Orthanc Server')
    executableFolder = None

    plugins = {
        'DicomWeb': {
            'description': 'Enable Dicom WEB protocols',
            'win64': 'OrthancDicomWeb.dll',
            'osx': 'libOrthancDicomWeb.dylib'
        },
        'WebViewer': {
            'description': 'Enable DICOM viewer in the Orthanc explorer',
            'win64': 'OrthancWebViewer.dll',
            'osx': 'libOrthancWebViewer.dylib'
        },
        'OsimisWebViewer': {
            'description': 'Enable Osimis web viewer in the Orthanc explorer',
            'win64': 'OsimisWebViewer.dll',
            'osx': 'libOsimisWebViewer.dylib'
        },
        'OsimisWebViewerPro':
        {
            'description': 'WebviewerPro',
            'win64': 'OsimisWebViewerPro.dll',
            'osx': 'libOsimisWebViewerPro.dylib'
        },
        'ModalityWorklists': {
            'description': 'Enable worklist server',
            'win64': 'ModalityWorklists.dll',
            'osx': 'libModalityWorklists.dylib'
        },
        'WSI': {
            'description': 'Enable WSI Viewer',
            'win64': 'OrthancWSI.dll',
            'osx': 'libOrthancWSI.dylib'  # not available yet in packages
        },
    }

    def __init__(self, name = None, aet = None, dicomPort = 4242, httpPort = 8042, configurationFile = None):

        self.config = {}
        self._configurationFile = None

        if name is not None and aet is not None:

            self.config['Name'] = name
            self.config['DicomAet'] = aet
            self.config['DicomPort'] = dicomPort
            self.config['HttpPort'] = httpPort
            self.setStorageDirectory('Orthanc_' + name + '/storage')
            self.setLogsDirectory('Orthanc_' + name + '/logs')
        elif configurationFile is not None:
            self._configurationFile = configurationFile

        self._process = None          # the Orthanc process
        self._loggerProcess = None    # the process we get the logs from (usually, the Orthanc process itself)
        self._temporaryConfigurationFile = None

        self.verbose = True
        self.trace = False
        self.upgradeDb = False
        self._isRunning = False

        # by default, use the Orthanc server logger to log all info (however, you can override this with setStdoutCallback
        self._stdoutCallback = None
        self._logInfo = self._logger.info
        self._logWarning = self._logger.warning
        self._logError = self._logger.error

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._logger.debug("stopping Orthanc")
        self.stop()
        # TODO: there's some cleanup to do to avoid resource warnings (but the code belows leads to deadlocks !)
        # self._logger.debug("exiting Orthanc logger process")
        # self._loggerProcess.__exit__(exc_type, exc_val, exc_tb)
        # self._logger.debug("exiting Orthanc process")
        # self._process.__exit__(exc_type, exc_val, exc_tb)
        # self._logger.debug("done")

    @staticmethod
    def loadExecutable(targetFolder, version = OrthancServerVersion.STABLE, overwriteExisting = False):

        OrthancServer.executableFolder = targetFolder

        if not overwriteExisting and os.path.exists(OrthancServer.getPathForOrthancExecutable(targetFolder)):
            return

        # get the url depending on the platform and nightly/stable version
        if platform.system() == 'Windows':
            if platform.machine() == 'x86':
                if version == OrthancServerVersion.STABLE:
                    url = 'win32/stable/orthancAndPluginsWin32.stable.zip'
                else:
                    url = 'win32/nightly/orthancAndPluginsWin32.nightly.zip'
            else:
                if version == OrthancServerVersion.STABLE:
                    url = 'win64/stable/orthancAndPluginsWin64.stable.zip'
                else:
                    url = 'win64/nightly/orthancAndPluginsWin64.nightly.zip'
        elif platform.system() == 'Darwin':
            if version == OrthancServerVersion.STABLE:
                url = 'osx/stable/orthancAndPluginsOSX.stable.zip'
            else:
                url = 'osx/nightly/orthancAndPluginsOSX.nightly.zip'

        # download the zip, etract and copy content to the target folder
        with tempfile.TemporaryDirectory() as tempDirectory:
            tempZipFile = os.path.join(tempDirectory, 'orthanc.zip')
            response = requests.get('http://orthanc.osimis.io/' + url)
            with open(tempZipFile, 'wb') as downloadedFile:
                downloadedFile.write(response.content)

            # FIXME nondeterministic zipfile.BadZipFile: File is not a zip file.
            # Most likely a network transient error, make the request more
            # robust.
            # https://jenkins.osidev.net/job/osimis/job/pythontoolbox/job/master/35/
            # https://jenkins.osidev.net/blue/organizations/jenkins/osimis%2Fpythontoolbox/detail/master/35
            with zipfile.ZipFile(tempZipFile) as zip:
                zip.extractall(tempDirectory)

            # on osx, set executable permissions to unzipped files
            if platform.system() == 'Darwin':
                for root, dirs, files in os.walk(tempDirectory):
                    for file in files:
                        os.chmod(os.path.join(root, file), 0o755)

            FileHelpers.remove(tempZipFile)
            FileHelpers.makeSurePathDoesNotExists(targetFolder)  # empty target folder
            shutil.copytree(tempDirectory, targetFolder)

    # define a callback to capture the stdout of the Orthanc process
    # exemple of callback:
    # orthancServerOutput = []
    # def orthancServerStdoutCallback(message):
    #   orthancServerOutput.append(message)
    def setStdoutCallback(self, stdoutCallback):
        self._stdoutCallback = stdoutCallback

    def setLogger(self, logger):
        self._logInfo = logger.info
        self._logWarning = logger.warning
        self._logError = logger.error

    def addPeer(self, alias, url, login = None, password = None):
        if "OrthancPeers" not in self.config:
            self.config["OrthancPeers"] = {}

        if login is not None and password is not None:
            self.config['OrthancPeers'][alias] = [url, login, password]
        else:
            self.config['OrthancPeers'][alias] = [url]

    # only makes sense if you have enabled the DicomWeb plugin
    # note, the url you must provide is the url of the distant dicom-web plugin i.e: http://127.0.0.1:10001/dicom-web
    def addDicomWebServer(self, alias, url, login = None, password = None, caFile = None):
        if self._process is not None:
            self._logError("Unable to add peers while orthanc is running")
            return

        if 'DicomWeb' not in self.config:
            self.config['DicomWeb'] = {}
        if 'Servers' not in self.config['DicomWeb']:
            self.config['DicomWeb']['Servers'] = {}

        self.config['DicomWeb']['Servers'][alias] = {
            'Url': url
        }

        if login is not None and password is not None:
            self.config['DicomWeb']['Servers'][alias]['Username'] = login
            self.config['DicomWeb']['Servers'][alias]['Password'] = password

        if caFile is not None:
            self.config['DicomWeb']['Servers'][alias]['CertificateFile'] = caFile

    def addModality(self, alias, aet, ip, port):
        if self.config.get("DicomModalities") is None:
            self.config["DicomModalities"] = {}
        self.config['DicomModalities'][alias] = [aet, ip, port]

    def addLuaScript(self, luaScripPath):
        if self.config.get("LuaScripts") is None:
            self.config["DicomModalities"] = []
        self.config['LuaScripts'].append(luaScripPath)

    def enableSsl(self, certificatePath):
        self.config['SslEnabled'] = True
        self.config['SslCertificate'] = certificatePath

    def enablePeersHttpsVerification(self, enable, caFile):
        self.config['HttpsCACertificates'] = caFile
        self.config['HttpsVerifyPeers'] = enable

    def addPluginPath(self, dllPath):
        self.config["Plugins"].append(dllPath)

    def addPlugin(self, pluginName):
        if pluginName not in self.plugins:
            raise ValueError('plugin not found "%"' % pluginName)
        # plugins are assumed to reside next to the executable
        if platform.system() == 'Darwin':
            pluginPath = os.path.join(self.executableFolder, self.plugins[pluginName]['osx'])
        elif platform.system() == 'Windows':
            pluginPath = os.path.join(self.executableFolder, self.plugins[pluginName]['win64'])
        else:
            return  # in Linux, all plugins are in /usr/share/orthanc/plugins, no need to add them individually
        self.addPluginPath(pluginPath)

    def setStorageDirectory(self, path):
        self.config['StorageDirectory'] = path
        self.config['IndexDirectory'] = path

    def setLogsDirectory(self, path):
        self.config[
            'LogsDirectory'] = path  # note: 'LogsDirectory' is not a key in the Orthanc configuration file but we use it internally

    def addHttpUser(self, userName, password):
        if not self.config.get("RegisteredUsers"):
            self.config["RegisteredUsers"] = {}
        self.config['RegisteredUsers'][userName] = password
        self.config['AuthenticationEnabled'] = True

    def setUserMetadata(self, dict):
        self.config['UserMetadata'] = dict

    def generateConfigurationFile(self, path, config):
        jsonContent = json.dumps(config, indent = 4)
        with open(path, 'w') as f:
            f.write(jsonContent)

    def launch(self):
        name = 'Orthanc'
        if self.config is not None:
            name = self.config['Name']

        self._logInfo('Starting Orthanc Server {0}'.format(name))
        if self._process is not None:
            message = 'Unable to launch Orthanc Server {0}.  It is already running'.format(name)
            self._logWarning(message)
            raise Exception(message)

        self._launch(self._configurationFile)

        try:
            # we should wait until it has really started
            if self.config is None:
                self._logInfo("Can not check if Orthanc has started (we don't know it's configuration)")
                return

            if self.config.get('SslEnabled'):
                orthancClient = self.getMinimalOrthancClient(caFile = self.config['SslCertificate'])
            else:
                orthancClient = self.getMinimalOrthancClient()

            isAlive = TimeOut.waitUntilCondition(lambda: orthancClient.isAlive(), 30, 0.1)

            if not isAlive:
                raise Exception('Could not connect to Orthanc HTTP Server.  It probablly failed to start')
            self._logInfo('Orthanc Server {0} started'.format(self.config['Name']))
        except Exception as ex:
            self._logError('Could not check if Orthanc is running: {}'.format(str(ex)))
            # if we can't detect it has started, let's kill the process
            self.stop()

    def _launch(self, configurationFilePath):
        orthancExecutable = OrthancServer.getPathForOrthancExecutable()
        # if not os.path.exists(orthancExecutable):
        #     message = 'Could not find Orthanc executable: ' + orthancExecutable
        #     self._logError(message)
        #     raise Exception(message)

        if configurationFilePath is None and self.config is not None:  # generate a config file from the config object
            self._temporaryConfigurationFile = tempfile.NamedTemporaryFile(delete = False)
            configurationFilePath = self._temporaryConfigurationFile.name
            self.generateConfigurationFile(configurationFilePath, self.config)

        if self.config is not None:
            self._logInfo('configuration file: {0}'.format(json.dumps(self.config, indent = 4)))
            FileHelpers.makeSurePathExists(self.config['StorageDirectory'])
            FileHelpers.makeSurePathExists(self.config['LogsDirectory'])
        elif configurationFilePath is not None:
            self._logInfo('configuration file path: {0}'.format(configurationFilePath))
        else:
            self._logInfo('no configuration file provided')

        creationFlags = 0
        if platform.system() == 'Windows':
            creationFlags = subprocess.CREATE_NEW_PROCESS_GROUP  # the flag does not exist on OSX or Linux see (http://stefan.sofa-rockers.org/2013/08/15/handling-sub-process-hierarchies-python-linux-os-x/)
        # build Orthanc launch command
        cmd = [orthancExecutable]
        if self.verbose:
            cmd.append('--verbose')
        if self.upgradeDb: # we should upgrade only when required
            cmd.append('--upgrade')
        if self.trace:
            cmd.append('--trace')
        # cmd.append('--logdir="{0}"'.format(os.path.abspath(self.config['LogsDirectory'])))
        if configurationFilePath is not None:
            cmd.append(configurationFilePath)
        self._process = subprocess.Popen(cmd, creationflags = creationFlags, stdout = subprocess.PIPE,
                                         stderr = subprocess.STDOUT, bufsize = 1)
        self._isRunning = True

        # start a thread that will listen to Orthanc output and log it through the logging facility
        self._loggerProcess = self._process
        name = 'Orthanc'
        if self.config is not None:
            name = self.config['Name']
        self._loggerThread = Thread(target = self._logOrthancOutput,
                                    name = 'Orthanc Logger {0}'.format(name))
        self._loggerThread.start()

    def getMinimalOrthancClient(self, caFile = None):
        if self.config.get('SslEnabled'):
            scheme = 'https'
        else:
            scheme = 'http'

        if not self.config.get('AuthenticationEnabled'):
            return OrthancMinimalHttpClient(
                rootUrl = '{scheme}://127.0.0.1:{port}'.format(
                    scheme = scheme,
                    port = self.config['HttpPort']),
                caFile = caFile)
        else:
            firstUserName = list(self.config['RegisteredUsers'])[0]
            firstPassword = self.config['RegisteredUsers'][firstUserName]
            return OrthancMinimalHttpClient(
                rootUrl = '{scheme}://127.0.0.1:{port}'.format(
                    scheme = scheme,
                    port = self.config['HttpPort']),
                userName = firstUserName,
                password = firstPassword)

    # logger thread functions, log the stdout and forward it to the logger and stdoutCallback if any
    def _logOrthancOutput(self):
        try:
            while self._isRunning:
                out = self._loggerProcess.stdout.readline()  # get Orthanc output line by line
                if out is None or self._loggerProcess.poll() != None:  # is process still alive ?
                    break
                out = out.decode().rstrip()
                if out != '':  # when process stops, it might return an empty line, don't log it
                    self._logInfo(out)
                    if self._stdoutCallback is not None:
                        self._stdoutCallback(out)

            self._logInfo(
                'Orthanc Server {0} exited with return code {1}'.format(self.config['Name'], self._loggerProcess.poll()))
        except Exception:
            pass

    def stop(self):
        self._isRunning = False
        if self._process is not None:
            name = 'Orthanc'
            if self.config is not None:
                name = self.config['Name']

            self._logInfo('Stopping Orthanc server {0}'.format(name))
            self._stop()
            self._logInfo('Orthanc server {0} stopped'.format(name))
            self._loggerThread.join()

    def _stop(self):
        if platform.system() == 'Windows':
            self._process.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            self._process.terminate()

        self._process.wait()  # wait the process actually exits

    @classmethod
    def getPathForOrthancExecutable(cls, executableFolder = None):
        if executableFolder is None:
            executableFolder = cls.executableFolder

        if platform.system() == 'Windows':
            return os.path.abspath(os.path.join(executableFolder, 'Orthanc.exe'))
        elif platform.system() == 'Darwin':
            return os.path.abspath(os.path.join(executableFolder, 'Orthanc'))
        elif platform.system() == 'Linux':
            return 'Orthanc'  # on Linux, we consider Orthanc is installed and accessible from anywhere
        else:
            raise NotImplementedError()  # and, this is actually normal it's not implemented since Docker is used under Linux



if __name__ == "__main__":
    LogHelpers.configureLogging()
    test = OrthancServer()
    test.launch()
    while True:
        time.sleep(1.0)
