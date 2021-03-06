"""
Assists in executing tests with a client
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import shlex
import subprocess
import tempfile

import ga4gh.protocol as protocol
import tests.utils as utils


class ClientForTesting(object):
    """
    A test client
    """
    def __init__(self, serverUrl, flags=None):
        self.serverUrl = serverUrl
        self.outFile = None
        self.errFile = None
        if flags is None:
            self.flags = "-v -O"
        else:
            self.flags = flags
        self.cmdLine = ("python client_dev.py {flags} {command} "
                        "{serverUrl}/v{protocolVersion}")
        self._createLogFiles()

    def _createLogFiles(self):
        self.outFile = tempfile.TemporaryFile()
        self.errFile = tempfile.TemporaryFile()

    def cleanup(self):
        self.outFile.close()
        self.errFile.close()

    def getOutLines(self):
        return utils.getLinesFromLogFile(self.outFile)

    def getErrLines(self):
        return utils.getLinesFromLogFile(self.errFile)

    def runCommand(self, command):
        clientCmdLine = self.cmdLine.format(**{
            "flags": self.flags,
            "command": command,
            "serverUrl": self.serverUrl,
            "protocolVersion": protocol.version, })
        splits = shlex.split(clientCmdLine)
        try:
            subprocess.check_call(
                splits,
                stdout=self.outFile,
                stderr=self.errFile)
        except subprocess.CalledProcessError as error:
            self.printDebugInfo(command)
            raise error

    def printDebugInfo(self, command):
        outLines = self.getOutLines()
        errLines = self.getErrLines()
        className = self.__class__.__name__
        print('\n')
        print('*** {} CMD ***'.format(className))
        print(command)
        print('*** {} STDOUT ***'.format(className))
        print(''.join(outLines))
        print('*** {} STDERR ***'.format(className))
        print(''.join(errLines))
