import re

from flake8_meiqia import core

_BLIND_EXCEPT_RE = re.compile(r'^except\s*:')


@core.flake8ext
def meiqia_except_format(logical_line, noqa):
    """Checks for blind except.

    Okay: try\n    pass\nexcept Exception:\n    pass
    Okay: try\n    pass\nexcept: # noqa\n    pass
    MQ201: try\n    pass\nexcept:\n    pass
    """
    if noqa:
        return

    m = _BLIND_EXCEPT_RE.search(logical_line)
    if not m:
        return

    msg = "MQ201: 'except:' is not allowed, at least use 'except Exception:'"
    yield (len('except'), msg)
