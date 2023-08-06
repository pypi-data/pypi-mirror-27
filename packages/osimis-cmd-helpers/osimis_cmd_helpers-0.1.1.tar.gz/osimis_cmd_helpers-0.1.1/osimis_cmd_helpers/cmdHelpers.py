import subprocess
import os
import platform

import sys
class CmdHelpers:
    """Helper class to run executable and other python scripts"""

    logger = None

    @staticmethod
    def runPython(message, pythonScriptAndArgs, workingFolder = None, stdoutCallback = None):
        """Runs a python script with or without arguments and returns the script return value
        ex: ret = CmdHelpers.runPython('Running my script', 'script.py', '../binaries')
            ret = CmdHelpers.runPython('Running my script', ['script.py', '--argument'], '../binaries')
        """
        args = [sys.executable]
        if isinstance(pythonScriptAndArgs, list):
            args.extend(pythonScriptAndArgs)
        elif isinstance(pythonScriptAndArgs, str): #if the command is a string, check if it has arguments (if it contains a space to separate command and arguments)
            if ' ' in pythonScriptAndArgs:
                args.extend(pythonScriptAndArgs.split(' '))
            else:
                args.append(pythonScriptAndArgs)

        return CmdHelpers.run(message, args, workingFolder, stdoutCallback)

    @staticmethod
    def runPythonExitIfFails(message, pythonScriptAndArgs, workingFolder = None, stdoutCallback = None):
        """Runs a python script with or without arguments and returns the script return value.
        If the script returns something not zero, exit the program

        ex: ret = CmdHelpers.runPythonExitIfFails('Running my script', 'script.py', '../binaries')
            ret = CmdHelpers.runPythonExitIfFails('Running my script', ['script.py', '--argument'], '../binaries')
            ret = CmdHelpers.runPythonExitIfFails('Running my script', 'script.py --argument', '../binaries')
        """
        ret, output = CmdHelpers.runPython(message, pythonScriptAndArgs, workingFolder, stdoutCallback)
        endMessage = "process '{}' returned {}".format(message, ret)
        if CmdHelpers.logger is not None:
            CmdHelpers.logger.error(endMessage)
        if stdoutCallback is not None:
            stdoutCallback(endMessage)

        if ret != 0:
            if CmdHelpers.logger is not None:
                CmdHelpers.logger.error(message + ': FAILED')
            exit(ret)

    @staticmethod
    def run(message, cmdAndArgs, workingFolder = None, stdoutCallback = None):
        """Runs an executable with or without arguments and returns the executable return value
        ex: ret = CmdHelpers.run('Running my app', 'app.exe', '../binaries')
            ret = CmdHelpers.run('Running my app', ['app.exe', '--argument'], '../binaries')
            ret = CmdHelpers.run('Running my app', 'app.exe --argument', '../binaries')
        """
        if CmdHelpers.logger is not None:
            CmdHelpers.logger.info("---" + message + "---")
        elif stdoutCallback is not None:
            stdoutCallback("---" + message + "---")

        #save current working folder
        if workingFolder is not None:
            previousCurrentWorkingDirectory = os.getcwd()
            os.chdir(workingFolder)

        if isinstance(cmdAndArgs, list):
            args = cmdAndArgs
        elif isinstance(cmdAndArgs, str): #if the command is a string, check if it has arguments (if it contains a space to separate command and arguments)
            if ' ' in cmdAndArgs:
                args = cmdAndArgs.split(' ')
            else:
                args = [cmdAndArgs]

        # remove empty args
        cmdAndArgs = list(filter(lambda x: x.strip() != "", cmdAndArgs))

        creationFlags = 0
        if platform.system() == 'Windows':
            creationFlags = subprocess.CREATE_NEW_PROCESS_GROUP #the flag does not exist on OSX or Linux see (http://stefan.sofa-rockers.org/2013/08/15/handling-sub-process-hierarchies-python-linux-os-x/)

        #create and launch the process
        with subprocess.Popen(args, creationflags = creationFlags, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, bufsize=1) as process:

            output = ''
            outLine = None
            while process.poll() is None:
                outLine = process.stdout.readline() #get output line by line
                outLine = outLine.decode('utf-8', 'replace')
                if stdoutCallback is not None and outLine != '':
                    stdoutCallback(outLine.rstrip())
                output = output + outLine

            #once the process completes, there might still be some output to read (once the whole output has been read, readline() will return '')
            while outLine != '':
                outLine = process.stdout.readline() #get output line by line
                if outLine is not None:
                    outLine = outLine.decode('utf-8', 'replace')
                    if stdoutCallback is not None and outLine != '':
                        stdoutCallback(outLine.rstrip())
                    output = output + outLine

            ret = process.returncode
            endMessage = "process '{}' returned {}".format(message, ret)
            if CmdHelpers.logger is not None:
                CmdHelpers.logger.error(endMessage)
            if stdoutCallback is not None:
                stdoutCallback(endMessage)
            #restore previous working folder
            if workingFolder is not None:
                os.chdir(previousCurrentWorkingDirectory)
            return ret, output


    @staticmethod
    def runExitIfFails(message, cmdAndArgs, workingFolder = None, stdoutCallback = None):
        """Runs an executable with or without arguments and returns the script return value.
        If the exe returns something not zero, exit the program

        ex: ret = CmdHelpers.runExitIfFails('Running my app', 'app.exe', '../binaries')
            ret = CmdHelpers.runExitIfFails('Running my app', ['app.exe', '--argument'], '../binaries')
        """
        ret, output = CmdHelpers.run(message, cmdAndArgs, workingFolder, stdoutCallback)
        if ret != 0:
            errorMessage = "{}: FAILED ({})".format(message, ret)
            if CmdHelpers.logger is not None:
                CmdHelpers.logger.error(errorMessage)
            if stdoutCallback is not None:
                stdoutCallback(errorMessage)
            exit(ret)


    @staticmethod
    def start(cmdAndArgs):

        if isinstance(cmdAndArgs, list):
            args = cmdAndArgs
        elif isinstance(cmdAndArgs, str): #if the command is a string, check if it has arguments (if it contains a space to separate command and arguments)
            if ' ' in cmdAndArgs:
                args = cmdAndArgs.split(' ')
            else:
                args = [cmdAndArgs]

        # remove empty args
        cmdAndArgs = list(filter(lambda x: x.strip() != "", cmdAndArgs))

        creationFlags = 0
        if platform.system() == 'Windows':
            creationFlags = subprocess.CREATE_NEW_PROCESS_GROUP #the flag does not exist on OSX or Linux see (http://stefan.sofa-rockers.org/2013/08/15/handling-sub-process-hierarchies-python-linux-os-x/)

        #create and launch the process
        return subprocess.Popen(args, creationflags = creationFlags, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, bufsize=1)
