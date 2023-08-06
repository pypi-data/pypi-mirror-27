__author__ = 'Viktor Kerkez <alefnula@gmail.com>'
__date__ = '01 January 2009'
__copyright__ = 'Copyright (c) 2009 Viktor Kerkez'

import io
import os
import re
import sys
import psutil
import tempfile
import win32api
import win32con
import win32pipe
import win32file
import win32event
import win32process
import win32security
from tea import shell
from tea.process import base
from tea.decorators import docstring


def _list_processes():
    for p in psutil.process_iter():
        try:
            try:
                cmdline = p.cmdline()
            except:
                cmdline = [p.exe()]
            yield WinProcess.immutable(p.pid, cmdline)
        except:
            pass


@docstring(base.doc_kill)
def kill(pid):
    process = WinProcess(
        os.path.join(os.environ['windir'], 'system32', 'taskkill.exe'),
        ['/PID', str(pid), '/F', '/T']
    )
    process.start()
    process.wait()
    return process.exit_code == 0


def create_file(filename, mode='rw'):
    if mode == 'r':
        desired_access = win32con.GENERIC_READ
    elif mode == 'w':
        desired_access = win32con.GENERIC_WRITE
    elif mode in ('rw', 'wr'):
        desired_access = win32con.GENERIC_READ | win32con.GENERIC_WRITE
    else:
        raise ValueError('Invalid access mode')
    share_mode = (win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE |
                  win32con.FILE_SHARE_DELETE)
    attributes = win32security.SECURITY_ATTRIBUTES()
    creation_disposition = win32con.OPEN_ALWAYS
    flags_and_attributes = win32con.FILE_ATTRIBUTE_NORMAL

    handle = win32file.CreateFile(filename, desired_access, share_mode,
                                  attributes, creation_disposition,
                                  flags_and_attributes, 0)
    return handle


def _get_cmd(command, arguments):
    if arguments is None:
        arguments = []
    if command.endswith('.py'):
        return [
            os.path.join(sys.prefix, 'python.exe'), command
        ] + list(arguments)
    elif command.endswith('.pyw'):
        return [
            os.path.join(sys.prefix, 'pythonw.exe'), command
        ] + list(arguments)
    else:
        return [command] + list(arguments)


def _escape(cmdline):
    return ' '.join([
        r'"%s"' % argument if re.search(r'\s', argument) else argument
        for argument in cmdline
    ])


class WinProcess(base.Process):
    def __init__(self, command, arguments=None, env=None, stdout=None,
                 stderr=None, redirect_output=True, working_dir=None):
        self._cmdline = _get_cmd(command, arguments)
        self._env = env
        self._stdout = os.path.abspath(stdout) if stdout else None
        self._stderr = os.path.abspath(stderr) if stderr else None
        self._redirect_output = redirect_output
        self._appName = None
        self._bInheritHandles = 1
        self._processAttributes = win32security.SECURITY_ATTRIBUTES()
        # TODO: Is this needed?
        # self._processAttributes.bInheritHandle = self._bInheritHandles
        self._threadAttributes = win32security.SECURITY_ATTRIBUTES()
        # TODO: Is this needed
        # self._threadAttributes.bInheritHandle = self._bInheritHandles
        self._dwCreationFlags = win32con.CREATE_NO_WINDOW
        # TODO: Which one of these is best?
        # self._dwCreationFlags=win32con.NORMAL_PRIORITY_CLASS
        self._currentDirectory = working_dir
        # This will be created during the start
        self._startupinfo = None
        self._hProcess = None
        self._hThread = None
        self._dwProcessId = None
        self._dwThreadId = None
        self._exit_code = None
        self._pid = None
        self._immutable = False

    @classmethod
    def immutable(cls, pid, command):
        p = cls(command[0], command[1:])
        p._immutable = False
        p._pid = pid
        return p

    def _create_pipes(self):
        sa = win32security.SECURITY_ATTRIBUTES()
        sa.bInheritHandle = 1
        self._stdin_read, self._stdin_write = win32pipe.CreatePipe(sa, 0)
        win32api.SetHandleInformation(self._stdin_write,
                                      win32con.HANDLE_FLAG_INHERIT, 0)
        if self._stdout:
            if os.path.isfile(self._stdout):
                shell.remove(self._stdout)
            shell.touch(self._stdout)
            self.stdout_reader = io.open(self._stdout, 'rb+')
        else:
            self._stdout_reader = tempfile.TemporaryFile()
        self._stdout_handle = create_file(self._stdout_reader.name)
        if self._stderr:
            if os.path.isfile(self._stderr):
                shell.remove(self._stderr)
            shell.touch(self._stderr)
            self._stderr_reader = io.open(self._stderr, 'rb+')
        else:
            self._stderr_reader = tempfile.TemporaryFile()
        self._stderr_handle = create_file(self._stderr_reader.name)

    @property
    def command(self):
        return self._cmdline[0]

    @property
    def arguments(self):
        return self._cmdline[1:]

    def start(self):
        if self._immutable:
            raise NotImplemented

        # Set up members of the STARTUPINFO structure.
        self._startupinfo = win32process.STARTUPINFO()
        if self._redirect_output:
            # Create pipes
            self._create_pipes()
            self._startupinfo.hStdInput = self._stdin_read
            self._startupinfo.hStdOutput = self._stdout_handle
            self._startupinfo.hStdError = self._stderr_handle
            self._startupinfo.dwFlags |= win32process.STARTF_USESTDHANDLES
        (
            self._hProcess, self._hThread, self._dwProcessId, self._dwThreadId
        ) = win32process.CreateProcess(
            self._appName, _escape(self._cmdline), self._processAttributes,
            self._threadAttributes, self._bInheritHandles,
            self._dwCreationFlags, self._create_env(self._env),
            self._currentDirectory, self._startupinfo
        )

    def kill(self):
        return kill(self.pid)

    def wait(self, timeout=None):
        if self._immutable:
            raise NotImplemented

        if timeout is None:
            while self.is_running:
                win32api.Sleep(1000)
        else:
            result = win32event.WaitForSingleObject(self._hProcess,
                                                    timeout * 1000)
            if result != win32event.WAIT_OBJECT_0:
                return False
        return True

    @property
    def is_running(self):
        if self._immutable:
            raise NotImplemented

        if self._hProcess is None or self._exit_code is not None:
            return False
        exit_code = win32process.GetExitCodeProcess(self._hProcess)
        if exit_code != 259:
            self._exit_code = exit_code
            return False
        return True

    @property
    def pid(self):
        return self._pid if self._immutable else self._dwProcessId

    @property
    def exit_code(self):
        if self._immutable:
            raise NotImplemented

        if self.is_running:
            return None
        return self._exit_code

    def write(self, string):
        if self._immutable:
            raise NotImplemented

        if self._redirect_output:
            if not string.endswith('\n'):
                string += '\n'
            win32file.WriteFile(self._stdin_write, string)
            win32file.FlushFileBuffers(self._stdin_write)

    def read(self):
        if self._immutable:
            raise NotImplemented

        if self._redirect_output:
            return self._stdout_reader.read()
        return ''

    def eread(self):
        if self._immutable:
            raise NotImplemented

        if self._redirect_output:
            return self._stderr_reader.read()
        return ''
