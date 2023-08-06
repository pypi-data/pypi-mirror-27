"""VirtuinBridge shall be used to launch Virtuin tests from Anduin."""

from __future__ import print_function
import json
import tempfile
import os

# pylint: disable=global-at-module-level
global station

try:
    from System.Diagnostics import Process
    __VIRT_ANDUIN_ENV__ = True
# pylint: disable=bare-except
except:
    __VIRT_ANDUIN_ENV__ = False
    from subprocess import Popen, PIPE

if __VIRT_ANDUIN_ENV__:
    def _runCommand(args, inputStr=None):
        """
        Runs child process using .NET Process.
        Args:
            args (list: str): Command arguments w/ first
            being executable.
            inputStr (str, None): Standard input to pass in.
        Returns:
            str: Standard output
            str: Standard error
            int: Process exit code
        """
        p = Process()
        have_stdin = inputStr is not None
        p.StartInfo.UseShellExecute = False
        p.StartInfo.RedirectStandardInput = have_stdin
        p.StartInfo.RedirectStandardOutput = True
        p.StartInfo.RedirectStandardError = True
        p.StartInfo.FileName = args[0]
        p.StartInfo.Arguments = " ".join(args[1:])
        p.Start()
        if have_stdin:
            p.StandardInput.Write(inputStr)
        p.WaitForExit()
        stdout = p.StandardOutput.ReadToEnd()
        stderr = p.StandardError.ReadToEnd()
        return stdout, stderr, p.ExitCode

else:
    def _runCommand(args, inputStr=None):
        """
        Runs child process using built-in subprocess.
        Args:
            args (list: str): Command arguments w/ first
            being executable.
            inputStr (str, None): Standard input to pass in.
        Returns:
            str: Standard output
            str: Standard error
            int: Process exit code
        """
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(inputStr)
        return stdout, stderr, p.returncode


def _net2dict(obj):
    """
    Converts .NET object public primitive attributes to python dict.
    .NET bool gets mapped to str due to IronPython compatibility issue.
    Function performs only shallow mapping (non-recursive).
    Args:
        obj (.Net object): .Net object
    Returns:
        dict: converted python dict
    """
    attrs = (name for name in dir(obj) if not name.startswith('_') and
             _isPrimitive(obj.__getattribute__(name)))
    objDict = dict()
    for attr in attrs:
        val = obj.__getattribute__(attr)
        # IronPython json uses incorrect boolean so change to string
        val = str(val) if isinstance(val, bool) else val
        objDict[attr] = val
    return objDict


def _isPrimitive(var):
    """
    Determines if supplied var is a primitive.
    (int, float, bool, str)
    Args:
        var: variable to check
    Returns:
        bool: True if primitive, False otherwise
    """
    return isinstance(var, (int, float, bool, str))


def getAnduinConfigs(anduinGlobals=None):
    """
    Extracts Anduin configs that are injected globally including
    slot, slot.Dut, station, and TestSpecs
    Args:
        anduinGlobals (dict): Injected global Anduin dict (.NET)
    Returns:
        dict: Python dict with keys dut, station, and specs.
    """
    configs = dict(dut={}, station={}, specs={})
    if __VIRT_ANDUIN_ENV__ and anduinGlobals:
        lclDut = _net2dict(anduinGlobals['slot'].Dut)
        configs['dut'].update(lclDut)
        lclStation = _net2dict(anduinGlobals['station'])
        kvKey = 'translateKeyValDictionary'
        stationConstants = anduinGlobals[kvKey](anduinGlobals['station'].Constants)
        lclStation.update(stationConstants)
        configs['station'].update(lclStation)
        for specName, specDict in anduinGlobals['TestSpecs'].iteritems():
            fullSpecDict = dict(lsl=None, usl=None, details='')
            fullSpecDict.update(specDict.copy())
            if "counts_in_result" in fullSpecDict:
                # IronPython json uses incorrect boolean so change to string
                fullSpecDict["counts"] = str(fullSpecDict["counts_in_result"])
            configs['specs'][specName] = fullSpecDict
    return configs


def getTotalConfigs(testConfigs, anduinGlobals=None):
    """
    Combines injected Anduin globals with supplied test config.
    Anduin globals override test config.
    Args:
        testConfigs (dict): Test configs {dut:{}, specs:{}, station:{}}
        anduinGlobals (dict): Injected global Anduin dict (.NET)
    Returns:
        dict: Merged dict with keys dut, station, and specs.
    """
    anduinConfigs = getAnduinConfigs(anduinGlobals)
    totalConfigs = testConfigs.copy()
    totalConfigs['dut'].update(anduinConfigs.get('dut', {}))
    totalConfigs['specs'].update(anduinConfigs.get('specs', {}))
    totalConfigs['station'].update(anduinConfigs.get('station', {}))
    return totalConfigs


def runVirtuinTest(testConfigs):
    """
    Runs Virtuin based test given supplied configs.
    Returns all results returned by test.
    Args:
        testConfigs (dict): Test configs {dut:{}, specs:{}, station:{}}
    Returns:
        str|None: Error message or None
        list: Results list of dict objects
    """
    # Create I/O files for Virtuin test
    tmpPath = testConfigs['station'].get("TEMP_PATH", None)
    testConfigPath = tempfile.mktemp(dir=tmpPath, suffix='.json')
    print(testConfigPath)
    testResultsPath = tempfile.mktemp(dir=tmpPath, suffix='.json')
    errcode = 0
    # pylint: disable=unused-variable
    stdout = ''
    stderr = ''
    # Write test configs to file
    with open(testConfigPath, 'w') as fp:
        json.dump(testConfigs, fp, skipkeys=True, ensure_ascii=True)
    # Run test and block until complete
    testCmd = ['VirtuinCore', testConfigPath, testResultsPath]
    stdout, stderr, errcode = _runCommand(args=testCmd, input=None)
    results = None
    error = None
    if errcode != 0:
        results = None
        error = 'Failed to spawn test. {:1} {:2}'.format(errcode, stderr)
    else:
        with open(testResultsPath, 'r') as fp:
            results = json.load(fp)
        error = None
    os.remove(testConfigPath)
    os.remove(testResultsPath)
    return error, results
