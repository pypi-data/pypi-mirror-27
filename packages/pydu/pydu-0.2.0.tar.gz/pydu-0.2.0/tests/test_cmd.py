import sys
from pydu.compat import string_types
from pydu.string import safeunicode
from pydu.cmd import run, cmdline_argv


def test_execute():
    retcode, output = run('echo hello')
    assert retcode == 0
    assert safeunicode(output).rstrip('\r\n') == 'hello'

    p = run('echo hello', wait=False)
    assert p.wait() == 0

    retcode, output = run('{} -c "import time; time.sleep(1)"'.format(sys.executable),
                          timeout=0.2, timeinterval=0.05)
    assert retcode != 0
    assert 'timeout' in output


def test_cmdline_argv():
    argv = cmdline_argv()
    for s in argv[1:]:
        assert isinstance(s, string_types)
