# License: Please refer to <https://unlicense.org>

'''
detect_dotnet execution module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reads the Windows registry trying to detect installed .NET Frameworks

.. versionadded:: 1.0

:configuration:

    .. code-block:: yaml
        salt '*' detect_dotnet.get_installed

'''
import logging

import salt.utils.compat
import salt.utils.platform

try:
    #  Import libs...
    #{% if depending_libraries %}
    #import {{depending_libraries}}
    #{% endif %}
    HAS_LIBS = True
    MISSING_PACKAGE_REASON = None
except ImportError as ie:
    HAS_LIBS = False
    MISSING_PACKAGE_REASON = ie.message

log = logging.getLogger(__name__)

__virtualname__ = 'win_dotnet'

def __virtual__():
    '''
    Only load this module if dependencies is installed on this minion.
    '''
    if HAS_LIBS:
        return __virtualname__
    return (False,
            'The {{module_name}} execution module failed to load:'
            'import error - {0}.'.format(MISSING_PACKAGE_REASON))

def __init__(opts):
    #  Put logic here to instantiate underlying jobs/connections
    pass

# https://docs.microsoft.com/en-us/dotnet/framework/migration-guide/how-to-determine-which-versions-are-installed
frameworks=[]
frameworks.append({ "fw_version":".NET Framework 1.0", "path":r"Software\Microsoft\.NETFramework\Policy\v1.0\3705", "key":"Install","vdata":1})
frameworks.append({ "fw_version":".NET Framework 1.1", "path":r"Software\Microsoft\NET Framework Setup\NDP\v1.1.4322", "key":"Install","vdata":1})
frameworks.append({ "fw_version":".NET Framework 2.0", "path":r"Software\Microsoft\NET Framework Setup\NDP\v2.0.50727", "key":"Install","vdata":1})
frameworks.append({ "fw_version":".NET Framework 3.0", "path":r"Software\Microsoft\NET Framework Setup\NDP\v3.0\Setup", "key":"InstallSuccess","vdata":1})
frameworks.append({ "fw_version":".NET Framework 3.5", "path":r"Software\Microsoft\NET Framework Setup\NDP\v3.5", "key":"Install","vdata":1})
frameworks.append({ "fw_version":".NET Framework 4.0 Client Profile", "path":r"Software\Microsoft\NET Framework Setup\NDP\v4\Client", "key":"Install","vdata":1})
frameworks.append({ "fw_version":".NET Framework 4.0 Full Profile", "path":r"Software\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Install","vdata":1})
frameworks.append({ "fw_version":".NET Framework 4.5", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":378389})
# On Windows 8.1 and Windows Server 2012 R2: 378675
frameworks.append({ "fw_version":".NET Framework 4.5.1", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":378675})
# On all other Windows operating systems: 378758
frameworks.append({ "fw_version":".NET Framework 4.5.1", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":378758})
frameworks.append({ "fw_version":".NET Framework 4.5.2", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":379893})
# On Windows 10: 393295
frameworks.append({ "fw_version":".NET Framework 4.6", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":393295})
# On all other Windows operating systems: 393297
frameworks.append({ "fw_version":".NET Framework 4.6", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":393297})
# On Windows 10 November Update systems: 394254
frameworks.append({ "fw_version":".NET Framework 4.6.1", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":394254})
# On all other Windows operating systems (including Windows 10): 394271
frameworks.append({ "fw_version":".NET Framework 4.6.1", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":394271})
# On Windows 10 Anniversary Update and Windows Server 2016: 394802
frameworks.append({ "fw_version":".NET Framework 4.6.2", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":394802})
# On all other Windows operating systems (including other Windows 10 operating systems): 394806
frameworks.append({ "fw_version":".NET Framework 4.6.2", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":394806})
# On Windows 10 Creators Update: 460798
frameworks.append({ "fw_version":".NET Framework 4.7", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":460798})
# On all other Windows operating systems (including other Windows 10 operating systems): 460805
frameworks.append({ "fw_version":".NET Framework 4.7", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":460805})
# On Windows 10 Fall Creators Update and Windows Server, version 1709: 461308
frameworks.append({ "fw_version":".NET Framework 4.7.1", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":461308})
# On all other Windows operating systems (including other Windows 10 operating systems): 461310
frameworks.append({ "fw_version":".NET Framework 4.7.1", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":461310})
# On Windows 10 April 2018 Update and Windows Server, version 1803: 461808
frameworks.append({ "fw_version":".NET Framework 4.7.1", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":461808})
# On all Windows operating systems other than Windows 10 April 2018 Update and Windows Server, version 1803: 461814
frameworks.append({ "fw_version":".NET Framework 4.7.1", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":461814})
# On Windows 10 May 2019 Update and Windows 10 November 2019 Update: 528040
frameworks.append({ "fw_version":".NET Framework 4.8", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":528040})
# On Windows 10 May 2020 Update and Windows 10 October 2020 Update: 528372
frameworks.append({ "fw_version":".NET Framework 4.8", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":528372})
# On all other Windows operating systems (including other Windows 10 operating systems): 528049
frameworks.append({ "fw_version":".NET Framework 4.8", "path":r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full", "key":"Release","vdata":528049})

def get_installed():
    list=[]
    if salt.utils.platform.is_windows():
        try:
            for item in frameworks:
                result=[]
                if __salt__["reg.read_value"]('HKLM',item['path'],item['key']).get('vdata') == item['vdata']:
                    result.append(item["fw_version"])
                    list.append(result)
        except Exception as e:
            list.append(repr(e))
    return list
