import datetime
import sys
import subprocess

def ExecuteCommand(command):
    '''Executes command given and exits if error is encountered'''

    # create subprocess object with passed command
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
    # get stdout and stderr from process object
    out, err = process.communicate()
    out = out[:-1].decode()
    err = err[:-1].decode()

    # if process.returncode is a non-zero value, report encountered error
    if process.returncode:
        errorMessage = (
            '{}: \'{}\' returned the following error: \'{}\''.format(
                datetime.datetime.now().strftime('%c'), command, err))
        print(errorMessage, file=sys.stderr)
        #sys.exit(process.returncode)

    # return captured stdout from executed command
    return out